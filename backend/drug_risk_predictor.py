from typing import Dict

class DrugRiskPredictor:
    """Predicts drug-specific risks based on pharmacogenomic profile"""
    
    # CPIC-aligned risk predictions
    RISK_RULES = {
        'CODEINE': {
            'PM': {'risk_label': 'Ineffective', 'severity': 'moderate', 'confidence': 0.9},
            'IM': {'risk_label': 'Adjust Dosage', 'severity': 'low', 'confidence': 0.7},
            'NM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.9},
            'RM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'URM': {'risk_label': 'Toxic', 'severity': 'high', 'confidence': 0.9},
            'Unknown': {'risk_label': 'Unknown', 'severity': 'low', 'confidence': 0.3},
        },
        'WARFARIN': {
            'PM': {'risk_label': 'Toxic', 'severity': 'high', 'confidence': 0.9},
            'IM': {'risk_label': 'Adjust Dosage', 'severity': 'moderate', 'confidence': 0.8},
            'NM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'RM': {'risk_label': 'Adjust Dosage', 'severity': 'low', 'confidence': 0.7},
            'URM': {'risk_label': 'Ineffective', 'severity': 'moderate', 'confidence': 0.8},
            'Unknown': {'risk_label': 'Unknown', 'severity': 'low', 'confidence': 0.3},
        },
        'CLOPIDOGREL': {
            'PM': {'risk_label': 'Ineffective', 'severity': 'critical', 'confidence': 0.95},
            'IM': {'risk_label': 'Adjust Dosage', 'severity': 'moderate', 'confidence': 0.8},
            'NM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.9},
            'RM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'URM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'Unknown': {'risk_label': 'Unknown', 'severity': 'low', 'confidence': 0.3},
        },
        'SIMVASTATIN': {
            'PM': {'risk_label': 'Toxic', 'severity': 'high', 'confidence': 0.9},
            'IM': {'risk_label': 'Adjust Dosage', 'severity': 'moderate', 'confidence': 0.8},
            'NM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.9},
            'RM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'URM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'Unknown': {'risk_label': 'Unknown', 'severity': 'low', 'confidence': 0.3},
        },
        'AZATHIOPRINE': {
            'PM': {'risk_label': 'Toxic', 'severity': 'critical', 'confidence': 0.95},
            'IM': {'risk_label': 'Adjust Dosage', 'severity': 'high', 'confidence': 0.9},
            'NM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.9},
            'RM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'URM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'Unknown': {'risk_label': 'Unknown', 'severity': 'moderate', 'confidence': 0.5},
        },
        'FLUOROURACIL': {
            'PM': {'risk_label': 'Toxic', 'severity': 'critical', 'confidence': 0.95},
            'IM': {'risk_label': 'Adjust Dosage', 'severity': 'high', 'confidence': 0.9},
            'NM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.9},
            'RM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'URM': {'risk_label': 'Safe', 'severity': 'none', 'confidence': 0.8},
            'Unknown': {'risk_label': 'Unknown', 'severity': 'moderate', 'confidence': 0.5},
        },
    }
    
    # Dosing recommendations aligned with CPIC guidelines
    DOSING_RECOMMENDATIONS = {
        'CODEINE': {
            'PM': {
                'recommendation': 'Avoid codeine. Use alternative analgesic (e.g., morphine, oxycodone)',
                'alternative_drugs': ['Morphine', 'Oxycodone', 'Hydromorphone'],
                'rationale': 'CYP2D6 poor metabolizers cannot convert codeine to active morphine metabolite'
            },
            'IM': {
                'recommendation': 'Reduce initial dose by 25-50%',
                'dosing_adjustment': '25-50% reduction',
                'monitoring': 'Monitor for reduced efficacy'
            },
            'URM': {
                'recommendation': 'Avoid codeine or use reduced dose',
                'dosing_adjustment': '50% reduction or avoid',
                'monitoring': 'Monitor for increased adverse effects (respiratory depression)'
            },
        },
        'WARFARIN': {
            'PM': {
                'recommendation': 'Reduce initial dose by 30-50%',
                'dosing_adjustment': '30-50% reduction',
                'monitoring': 'Frequent INR monitoring (daily initially)'
            },
            'IM': {
                'recommendation': 'Reduce initial dose by 20-30%',
                'dosing_adjustment': '20-30% reduction',
                'monitoring': 'Frequent INR monitoring'
            },
        },
        'CLOPIDOGREL': {
            'PM': {
                'recommendation': 'Use alternative antiplatelet agent (prasugrel or ticagrelor)',
                'alternative_drugs': ['Prasugrel', 'Ticagrelor'],
                'rationale': 'CYP2C19 poor metabolizers have reduced clopidogrel activation'
            },
            'IM': {
                'recommendation': 'Consider alternative agent or increased dose',
                'dosing_adjustment': 'Consider 150mg daily (if alternative not available)',
                'monitoring': 'Monitor platelet function'
            },
        },
        'SIMVASTATIN': {
            'PM': {
                'recommendation': 'Reduce dose by 50% or use alternative statin',
                'dosing_adjustment': '50% reduction',
                'alternative_drugs': ['Pravastatin', 'Rosuvastatin'],
                'monitoring': 'Monitor for myopathy (CK levels)'
            },
            'IM': {
                'recommendation': 'Reduce dose by 25-50%',
                'dosing_adjustment': '25-50% reduction',
                'monitoring': 'Monitor for myopathy'
            },
        },
        'AZATHIOPRINE': {
            'PM': {
                'recommendation': 'Reduce dose by 90% or use alternative immunosuppressant',
                'dosing_adjustment': '90% reduction (10% of standard dose)',
                'alternative_drugs': ['Mercaptopurine (at reduced dose)', 'Mycophenolate'],
                'monitoring': 'Monitor for severe myelosuppression',
                'rationale': 'TPMT poor metabolizers have severe toxicity risk'
            },
            'IM': {
                'recommendation': 'Reduce dose by 30-50%',
                'dosing_adjustment': '30-50% reduction',
                'monitoring': 'Monitor for myelosuppression'
            },
        },
        'FLUOROURACIL': {
            'PM': {
                'recommendation': 'Avoid fluorouracil or reduce dose by 50% with close monitoring',
                'dosing_adjustment': '50% reduction or avoid',
                'alternative_drugs': ['Capecitabine (with caution)', 'Alternative chemotherapy'],
                'monitoring': 'Monitor for severe toxicity (mucositis, diarrhea, neutropenia)',
                'rationale': 'DPYD poor metabolizers have life-threatening toxicity risk'
            },
            'IM': {
                'recommendation': 'Reduce dose by 25-50%',
                'dosing_adjustment': '25-50% reduction',
                'monitoring': 'Monitor for toxicity'
            },
        },
    }
    
    def predict_risk(self, drug_name: str, pgx_profile: Dict) -> Dict:
        """Predict drug-specific risk based on pharmacogenomic profile"""
        phenotype = pgx_profile.get('phenotype', 'Unknown')
        drug_upper = drug_name.upper()
        
        if drug_upper not in self.RISK_RULES:
            return {
                'risk_label': 'Unknown',
                'confidence_score': 0.0,
                'severity': 'low'
            }
        
        rules = self.RISK_RULES[drug_upper]
        risk_data = rules.get(phenotype, rules['Unknown'])
        
        return {
            'risk_label': risk_data['risk_label'],
            'confidence_score': risk_data['confidence'],
            'severity': risk_data['severity']
        }
    
    def generate_recommendation(self, drug_name: str, pgx_profile: Dict, risk_assessment: Dict) -> Dict:
        """Generate clinical recommendation based on CPIC guidelines"""
        phenotype = pgx_profile.get('phenotype', 'Unknown')
        drug_upper = drug_name.upper()
        risk_label = risk_assessment.get('risk_label', 'Unknown')
        
        if drug_upper not in self.DOSING_RECOMMENDATIONS:
            return {
                'action': 'Consult clinical pharmacogenomics specialist',
                'dosing_adjustment': 'None specified',
                'monitoring': 'Standard monitoring recommended'
            }
        
        dosing_rules = self.DOSING_RECOMMENDATIONS[drug_upper]
        
        # Get phenotype-specific recommendation
        if phenotype in dosing_rules:
            rec = dosing_rules[phenotype].copy()
            rec['action'] = rec.get('recommendation', 'Standard dosing')
            return rec
        
        # Default recommendations based on risk
        if risk_label == 'Safe':
            return {
                'action': 'Standard dosing recommended',
                'dosing_adjustment': 'None',
                'monitoring': 'Standard monitoring'
            }
        elif risk_label == 'Adjust Dosage':
            return {
                'action': 'Consider dose adjustment',
                'dosing_adjustment': 'Consult dosing guidelines',
                'monitoring': 'Enhanced monitoring recommended'
            }
        elif risk_label in ['Toxic', 'Ineffective']:
            return {
                'action': 'Consider alternative therapy',
                'dosing_adjustment': 'Not recommended',
                'monitoring': 'If used, close monitoring required'
            }
        else:
            return {
                'action': 'Insufficient data for recommendation',
                'dosing_adjustment': 'Standard dosing',
                'monitoring': 'Standard monitoring'
            }
