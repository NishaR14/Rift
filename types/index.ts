export interface Variant {
  rsid: string
  gene: string
  chromosome?: string
  position?: number
  reference?: string
  alternate?: string
  star_allele?: string
  genotype?: string
  clinical_significance?: string
}

export interface RiskAssessment {
  risk_label: 'Safe' | 'Adjust Dosage' | 'Toxic' | 'Ineffective' | 'Unknown'
  confidence_score: number
  severity: 'none' | 'low' | 'moderate' | 'high' | 'critical'
}

export interface PharmacogenomicProfile {
  primary_gene: string
  diplotype: string
  phenotype: 'PM' | 'IM' | 'NM' | 'RM' | 'URM' | 'Unknown'
  detected_variants: Variant[]
}

export interface ClinicalRecommendation {
  action: string
  dosing_adjustment?: string
  monitoring?: string
  alternative_drugs?: string[]
  rationale?: string
}

export interface LLMExplanation {
  summary: string
  biological_mechanism?: string
  clinical_significance?: string
  variant_citations: string[]
  evidence_level: string
  full_explanation?: string
}

export interface QualityMetrics {
  vcf_parsing_success: boolean
  variants_analyzed: number
  pgx_variants_found: number
  coverage_quality?: string
}

export interface AnalysisResult {
  patient_id: string
  drug: string
  timestamp: string
  risk_assessment: RiskAssessment
  pharmacogenomic_profile: PharmacogenomicProfile
  clinical_recommendation: ClinicalRecommendation
  llm_generated_explanation: LLMExplanation
  quality_metrics: QualityMetrics
}
