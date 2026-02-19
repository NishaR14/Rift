from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import openai
from vcf_parser import VCFParser
from pharmacogenomics import PharmacogenomicAnalyzer
from drug_risk_predictor import DrugRiskPredictor
from llm_explainer import LLMExplainer

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {'vcf'}

# Ensure upload directory exists
upload_path = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER)
os.makedirs(upload_path, exist_ok=True)

app.config['UPLOAD_FOLDER'] = upload_path
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize components
vcf_parser = VCFParser()
pgx_analyzer = PharmacogenomicAnalyzer()
drug_predictor = DrugRiskPredictor()
llm_explainer = LLMExplainer()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'PharmaGuard API'})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        # Validate request
        if 'vcf_file' not in request.files:
            return jsonify({'error': 'No VCF file provided'}), 400
        
        file = request.files['vcf_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only .vcf files are allowed'}), 400
        
        # Get drug names
        drug_names = request.form.get('drugs', '').strip()
        if not drug_names:
            return jsonify({'error': 'No drug names provided'}), 400
        
        drug_list = [d.strip().upper() for d in drug_names.split(',')]
        
        # Validate drug names
        valid_drugs = ['CODEINE', 'WARFARIN', 'CLOPIDOGREL', 'SIMVASTATIN', 'AZATHIOPRINE', 'FLUOROURACIL']
        invalid_drugs = [d for d in drug_list if d not in valid_drugs]
        if invalid_drugs:
            return jsonify({'error': f'Invalid drug names: {", ".join(invalid_drugs)}'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
        except Exception as e:
            return jsonify({'error': f'File save failed: {str(e)}'}), 500
        
        # Parse VCF file
        vcf_data = vcf_parser.parse_vcf(filepath)
        
        if not vcf_data['success']:
            return jsonify({'error': f'VCF parsing failed: {vcf_data.get("error", "Unknown error")}'}), 400
        
        # Process each drug
        results = []
        patient_id = vcf_data.get('patient_id', f'PATIENT_{datetime.now().strftime("%Y%m%d%H%M%S")}')
        
        for drug_name in drug_list:
            # Analyze pharmacogenomic variants
            pgx_profile = pgx_analyzer.analyze_variants(vcf_data['variants'], drug_name)
            
            # Predict drug risk
            risk_assessment = drug_predictor.predict_risk(drug_name, pgx_profile)
            
            # Generate clinical recommendation
            clinical_rec = drug_predictor.generate_recommendation(drug_name, pgx_profile, risk_assessment)
            
            # Generate LLM explanation
            llm_explanation = llm_explainer.generate_explanation(
                drug_name, pgx_profile, risk_assessment, clinical_rec
            )
            
            # Build result JSON matching exact schema
            result = {
                "patient_id": patient_id,
                "drug": drug_name,
                "timestamp": datetime.now().isoformat(),
                "risk_assessment": {
                    "risk_label": risk_assessment['risk_label'],
                    "confidence_score": risk_assessment['confidence_score'],
                    "severity": risk_assessment['severity']
                },
                "pharmacogenomic_profile": {
                    "primary_gene": pgx_profile['primary_gene'],
                    "diplotype": pgx_profile['diplotype'],
                    "phenotype": pgx_profile['phenotype'],
                    "detected_variants": pgx_profile['detected_variants']
                },
                "clinical_recommendation": clinical_rec,
                "llm_generated_explanation": llm_explanation,
                "quality_metrics": {
                    "vcf_parsing_success": vcf_data['success'],
                    "variants_analyzed": len(vcf_data['variants']),
                    "pgx_variants_found": len(pgx_profile['detected_variants']),
                    "coverage_quality": pgx_profile.get('coverage_quality', 'good')
                }
            }
            
            results.append(result)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'results': results if len(results) > 1 else results[0]
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
