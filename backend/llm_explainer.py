import os
import openai
from typing import Dict, List

class LLMExplainer:
    """Generates clinical explanations using LLM"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
    
    def generate_explanation(self, drug_name: str, pgx_profile: Dict, 
                            risk_assessment: Dict, clinical_rec: Dict) -> Dict:
        """
        Generate LLM-powered clinical explanation
        
        Returns explanation with summary, biological mechanism, and variant citations
        """
        if not self.client:
            # Fallback explanation if LLM not available
            return self._fallback_explanation(drug_name, pgx_profile, risk_assessment, clinical_rec)
        
        try:
            # Build prompt with context
            prompt = self._build_prompt(drug_name, pgx_profile, risk_assessment, clinical_rec)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a clinical pharmacogenomics expert. Provide clear, evidence-based explanations of pharmacogenomic test results for healthcare providers."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            explanation_text = response.choices[0].message.content
            
            # Parse and structure explanation
            return self._structure_explanation(explanation_text, pgx_profile, risk_assessment)
            
        except Exception as e:
            # Fallback on error
            return self._fallback_explanation(drug_name, pgx_profile, risk_assessment, clinical_rec)
    
    def _build_prompt(self, drug_name: str, pgx_profile: Dict, 
                     risk_assessment: Dict, clinical_rec: Dict) -> str:
        """Build prompt for LLM"""
        variants = pgx_profile.get('detected_variants', [])
        variant_citations = []
        
        for variant in variants[:5]:  # Limit to top 5 variants
            rsid = variant.get('rsid', 'unknown')
            gene = variant.get('gene', 'unknown')
            star = variant.get('star_allele', 'unknown')
            clinical_sig = variant.get('clinical_significance', 'unknown')
            
            variant_citations.append(
                f"- {rsid} in {gene} (star allele: {star}, significance: {clinical_sig})"
            )
        
        prompt = f"""
Analyze this pharmacogenomic test result and provide a clinical explanation:

DRUG: {drug_name}
PRIMARY GENE: {pgx_profile.get('primary_gene', 'Unknown')}
DIPLOTYPE: {pgx_profile.get('diplotype', 'Unknown')}
PHENOTYPE: {pgx_profile.get('phenotype', 'Unknown')}
RISK ASSESSMENT: {risk_assessment.get('risk_label', 'Unknown')} (Severity: {risk_assessment.get('severity', 'unknown')})

DETECTED VARIANTS:
{chr(10).join(variant_citations) if variant_citations else 'No specific variants detected'}

CLINICAL RECOMMENDATION: {clinical_rec.get('action', 'Standard dosing')}

Provide a structured explanation with:
1. A 2-3 sentence summary of the finding
2. Biological mechanism explaining how the genetic variant affects drug metabolism
3. Clinical significance and why this matters for patient safety/efficacy
4. Specific variant citations (rsIDs) mentioned above

Be concise, clinically accurate, and cite specific variants when possible.
"""
        return prompt
    
    def _structure_explanation(self, explanation_text: str, pgx_profile: Dict, 
                              risk_assessment: Dict) -> Dict:
        """Structure LLM response into required format"""
        variants = pgx_profile.get('detected_variants', [])
        variant_citations = [v.get('rsid') for v in variants if v.get('rsid')]
        
        return {
            'summary': explanation_text[:300] + '...' if len(explanation_text) > 300 else explanation_text,
            'biological_mechanism': self._extract_section(explanation_text, 'mechanism', 'metabolism'),
            'clinical_significance': self._extract_section(explanation_text, 'significance', 'clinical'),
            'variant_citations': variant_citations[:5],  # Top 5 variants
            'evidence_level': 'CPIC Guidelines',
            'full_explanation': explanation_text
        }
    
    def _extract_section(self, text: str, *keywords) -> str:
        """Extract relevant section from explanation text"""
        # Simple extraction - in production, use more sophisticated NLP
        sentences = text.split('.')
        relevant = [s.strip() for s in sentences 
                   if any(kw.lower() in s.lower() for kw in keywords)]
        return '. '.join(relevant[:2]) + '.' if relevant else text[:200]
    
    def _fallback_explanation(self, drug_name: str, pgx_profile: Dict, 
                             risk_assessment: Dict, clinical_rec: Dict) -> Dict:
        """Generate fallback explanation without LLM"""
        phenotype = pgx_profile.get('phenotype', 'Unknown')
        gene = pgx_profile.get('primary_gene', 'Unknown')
        diplotype = pgx_profile.get('diplotype', 'Unknown')
        risk_label = risk_assessment.get('risk_label', 'Unknown')
        
        variants = pgx_profile.get('detected_variants', [])
        variant_citations = [v.get('rsid') for v in variants if v.get('rsid') and v.get('rsid') != 'unknown']
        
        # Generate summary based on phenotype and risk
        if phenotype == 'PM':
            summary = f"Patient is a {phenotype} ({diplotype}) for {gene}. This results in {risk_label.lower()} risk for {drug_name}."
        elif phenotype == 'IM':
            summary = f"Patient is an {phenotype} ({diplotype}) for {gene}. Dose adjustment may be needed for {drug_name}."
        elif phenotype in ['RM', 'URM']:
            summary = f"Patient is a {phenotype} ({diplotype}) for {gene}. Enhanced metabolism may affect {drug_name} efficacy."
        else:
            summary = f"Pharmacogenomic analysis for {drug_name} based on {gene} ({diplotype}). Risk assessment: {risk_label}."
        
        biological_mechanism = f"{gene} encodes an enzyme involved in {drug_name} metabolism. The {diplotype} diplotype results in a {phenotype} phenotype, affecting drug clearance and response."
        
        clinical_significance = f"This finding is clinically significant because {risk_label.lower()} risk requires {clinical_rec.get('action', 'clinical consideration')}."
        
        return {
            'summary': summary,
            'biological_mechanism': biological_mechanism,
            'clinical_significance': clinical_significance,
            'variant_citations': variant_citations[:5],
            'evidence_level': 'CPIC Guidelines',
            'full_explanation': f"{summary} {biological_mechanism} {clinical_significance}"
        }
