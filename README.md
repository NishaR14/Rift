# PharmaGuard - AI-Powered Pharmacogenomic Risk Assessment
# Deployement link:https://rift-2026-copy-pi.vercel.app/login
## 🎯 Project Overview

PharmaGuard is an AI-powered web application that analyzes patient genetic data (VCF files) and drug names to predict personalized pharmacogenomic risks and provide clinically actionable recommendations with LLM-generated explanations.

**Problem Statement**: Adverse drug reactions kill over 100,000 Americans annually. Many of these deaths are preventable through pharmacogenomic testing — analyzing how genetic variants affect drug metabolism.

## 🔗 Live Demo

- **Live Application URL**: [Deploy to Vercel/Netlify and add URL here]
- **LinkedIn Video**: [Add LinkedIn video link after posting]

## 🏗️ Architecture Overview

PharmaGuard consists of two main components:

1. **Backend API** (Flask/Python): Handles VCF file parsing, pharmacogenomic variant detection, drug risk prediction, and LLM-powered explanation generation
2. **Frontend Web App** (Next.js/React): Provides an intuitive interface for file upload, drug input, and results visualization

### System Flow

```
User Uploads VCF → Backend Parses Variants → PGx Analysis → Risk Prediction → LLM Explanation → JSON Output
```

## 🛠️ Tech Stack

### Backend
- **Flask**: Python web framework for API endpoints
- **OpenAI API**: GPT-4 for generating clinical explanations
- **Custom VCF Parser**: Parses Variant Call Format files
- **Pharmacogenomic Engine**: Analyzes variants in 6 critical genes (CYP2D6, CYP2C19, CYP2C9, SLCO1B1, TPMT, DPYD)

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Modern, responsive styling
- **React Dropzone**: File upload component

## 📋 Features

- ✅ VCF file parsing (Variant Call Format v4.2)
- ✅ Pharmacogenomic variant detection across 6 critical genes
- ✅ Drug-specific risk prediction (Safe, Adjust Dosage, Toxic, Ineffective, Unknown)
- ✅ CPIC-aligned dosing recommendations
- ✅ LLM-generated clinical explanations with variant citations
- ✅ Structured JSON output matching exact schema requirements
- ✅ Color-coded risk visualization
- ✅ Downloadable results and copy-to-clipboard functionality

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key (for LLM explanations)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r ../requirements.txt
```

4. Set environment variables:
```bash
cp ../.env.example ../.env
# Edit .env and add your OPENAI_API_KEY
```

5. Run Flask server:
```bash
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Set environment variables:
```bash
cp .env.example .env.local
# Edit .env.local and set BACKEND_URL if needed
```

3. Run development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📖 API Documentation

### POST `/api/analyze`

Analyzes VCF file and drug names to generate pharmacogenomic risk assessment.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `vcf_file`: VCF file (max 5MB)
  - `drugs`: Comma-separated drug names (e.g., "CODEINE, WARFARIN")

**Response:**
```json
{
  "success": true,
  "results": {
    "patient_id": "PATIENT_XXX",
    "drug": "CODEINE",
    "timestamp": "2026-02-19T12:00:00",
    "risk_assessment": {
      "risk_label": "Safe",
      "confidence_score": 0.9,
      "severity": "none"
    },
    "pharmacogenomic_profile": {
      "primary_gene": "CYP2D6",
      "diplotype": "*1/*1",
      "phenotype": "NM",
      "detected_variants": [...]
    },
    "clinical_recommendation": {...},
    "llm_generated_explanation": {...},
    "quality_metrics": {...}
  }
}
```

### GET `/api/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "PharmaGuard API"
}
```

## 💡 Usage Examples

### Example 1: Single Drug Analysis

1. Upload a VCF file using the file upload interface
2. Enter drug name: `CODEINE`
3. Click "Analyze Pharmacogenomic Risk"
4. View results with risk assessment, phenotype, and recommendations

### Example 2: Multiple Drugs

1. Upload VCF file
2. Enter multiple drugs: `WARFARIN, CLOPIDOGREL, SIMVASTATIN`
3. Analyze to get results for all drugs

### Supported Drugs

- CODEINE
- WARFARIN
- CLOPIDOGREL
- SIMVASTATIN
- AZATHIOPRINE
- FLUOROURACIL

## 🧪 Test Cases

Sample VCF files are provided in the `test_data/` directory. These can be used to test the application.

### Expected Output Schema

The application generates JSON output matching this exact schema:

```json
{
  "patient_id": "PATIENT_XXX",
  "drug": "DRUG_NAME",
  "timestamp": "ISO8601_timestamp",
  "risk_assessment": {
    "risk_label": "Safe|Adjust Dosage|Toxic|Ineffective|Unknown",
    "confidence_score": 0.0,
    "severity": "none|low|moderate|high|critical"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "GENE_SYMBOL",
    "diplotype": "*X/*Y",
    "phenotype": "PM|IM|NM|RM|URM|Unknown",
    "detected_variants": [
      {
        "rsid": "rsXXXX",
        "gene": "GENE",
        "chromosome": "chr",
        "position": 12345,
        "reference": "A",
        "alternate": "G",
        "star_allele": "*2",
        "genotype": "0/1",
        "clinical_significance": "Loss of function"
      }
    ]
  },
  "clinical_recommendation": {
    "action": "Recommendation text",
    "dosing_adjustment": "Dose adjustment details",
    "monitoring": "Monitoring requirements",
    "alternative_drugs": ["Drug1", "Drug2"],
    "rationale": "Explanation"
  },
  "llm_generated_explanation": {
    "summary": "Brief summary",
    "biological_mechanism": "Mechanism explanation",
    "clinical_significance": "Clinical importance",
    "variant_citations": ["rs123", "rs456"],
    "evidence_level": "CPIC Guidelines",
    "full_explanation": "Complete explanation"
  },
  "quality_metrics": {
    "vcf_parsing_success": true,
    "variants_analyzed": 1000,
    "pgx_variants_found": 5,
    "coverage_quality": "good"
  }
}
```

## 🧬 Pharmacogenomic Genes Analyzed

1. **CYP2D6**: Codeine metabolism
2. **CYP2C19**: Clopidogrel activation
3. **CYP2C9**: Warfarin metabolism
4. **SLCO1B1**: Simvastatin transport
5. **TPMT**: Azathioprine metabolism
6. **DPYD**: Fluorouracil metabolism

## 📊 Risk Assessment Categories

- **Safe**: Standard dosing recommended
- **Adjust Dosage**: Dose modification needed
- **Toxic**: High risk of adverse effects
- **Ineffective**: Drug unlikely to be effective
- **Unknown**: Insufficient data for assessment

## 🔒 Error Handling

The application handles:
- Invalid VCF file formats
- Missing annotations
- File size limits (5MB)
- Invalid drug names
- LLM API failures (falls back to rule-based explanations)

## 🚢 Deployment

### Backend Deployment

Deploy Flask backend to:
- **Render**: Connect GitHub repo, set Python environment
- **Heroku**: Use Procfile and requirements.txt
- **AWS/GCP/Azure**: Use container services

### Frontend Deployment

Deploy Next.js frontend to:
- **Vercel**: Connect GitHub repo, auto-deploy
- **Netlify**: Connect GitHub repo, set build command: `npm run build`

### Environment Variables

Set these in your deployment platform:
- `OPENAI_API_KEY`: Your OpenAI API key
- `BACKEND_URL`: Backend API URL (for frontend)

## 👥 Team Members

[Add team member names and roles here]

## 📝 License

[Add license information]

## 🙏 Acknowledgments

- CPIC (Clinical Pharmacogenomics Implementation Consortium) guidelines
- PharmGKB for pharmacogenomic variant databases
- OpenAI for LLM capabilities

## 📧 Contact

[Add contact information]

---

**Built for RIFT 2026** | #RIFT2026 #PharmaGuard #Pharmacogenomics #AIinHealthcare
