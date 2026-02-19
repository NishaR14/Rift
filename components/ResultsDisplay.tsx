'use client'

import { useState } from 'react'
import { AnalysisResult } from '@/types'

interface ResultsDisplayProps {
  results: AnalysisResult | AnalysisResult[]
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const resultsArray = Array.isArray(results) ? results : [results]
  const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set([0]))

  const toggleSection = (index: number) => {
    const newExpanded = new Set(expandedSections)
    if (newExpanded.has(index)) {
      newExpanded.delete(index)
    } else {
      newExpanded.add(index)
    }
    setExpandedSections(newExpanded)
  }

  const getRiskColor = (riskLabel: string) => {
    const risk = riskLabel.toUpperCase()
    if (risk === 'SAFE') return 'bg-green-100 text-green-800 border-green-300'
    if (risk === 'ADJUST DOSAGE') return 'bg-yellow-100 text-yellow-800 border-yellow-300'
    if (risk === 'TOXIC' || risk === 'INEFFECTIVE') return 'bg-red-100 text-red-800 border-red-300'
    return 'bg-gray-100 text-gray-800 border-gray-300'
  }

  const getSeverityColor = (severity: string) => {
    const sev = severity.toLowerCase()
    if (sev === 'critical') return 'text-red-700 font-bold'
    if (sev === 'high') return 'text-red-600 font-semibold'
    if (sev === 'moderate') return 'text-orange-600'
    if (sev === 'low') return 'text-yellow-600'
    return 'text-gray-600'
  }

  const downloadJSON = (result: AnalysisResult, index: number) => {
    const dataStr = JSON.stringify(result, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `pharmaguard_result_${result.drug}_${index + 1}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  const copyToClipboard = (result: AnalysisResult) => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2))
    alert('JSON copied to clipboard!')
  }

  return (
    <div className="space-y-6">
      {resultsArray.map((result, index) => (
        <div key={index} className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-1">
                {result.drug} Analysis
              </h2>
              <p className="text-sm text-gray-500">
                Patient ID: {result.patient_id} | {new Date(result.timestamp).toLocaleString()}
              </p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => downloadJSON(result, index)}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm"
              >
                Download JSON
              </button>
              <button
                onClick={() => copyToClipboard(result)}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 text-sm"
              >
                Copy JSON
              </button>
            </div>
          </div>

          {/* Risk Assessment */}
          <div className="mb-6">
            <div className={`border-2 rounded-lg p-4 ${getRiskColor(result.risk_assessment.risk_label)}`}>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold mb-1">
                    Risk Assessment: {result.risk_assessment.risk_label}
                  </h3>
                  <p className="text-sm">
                    Confidence: {(result.risk_assessment.confidence_score * 100).toFixed(1)}% | 
                    Severity: <span className={getSeverityColor(result.risk_assessment.severity)}>
                      {result.risk_assessment.severity.toUpperCase()}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Pharmacogenomic Profile */}
          <div className="mb-6">
            <button
              onClick={() => toggleSection(index)}
              className="w-full text-left flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100"
            >
              <h3 className="font-semibold text-gray-900">Pharmacogenomic Profile</h3>
              <span>{expandedSections.has(index) ? '−' : '+'}</span>
            </button>
            {expandedSections.has(index) && (
              <div className="mt-2 p-4 bg-gray-50 rounded-lg space-y-2">
                <p><strong>Primary Gene:</strong> {result.pharmacogenomic_profile.primary_gene}</p>
                <p><strong>Diplotype:</strong> {result.pharmacogenomic_profile.diplotype}</p>
                <p><strong>Phenotype:</strong> {result.pharmacogenomic_profile.phenotype}</p>
                <div>
                  <strong>Detected Variants:</strong>
                  <ul className="list-disc list-inside mt-1 space-y-1">
                    {result.pharmacogenomic_profile.detected_variants.length > 0 ? (
                      result.pharmacogenomic_profile.detected_variants.map((variant, vIdx) => (
                        <li key={vIdx} className="text-sm">
                          {variant.rsid} ({variant.gene})
                          {variant.star_allele && ` - Star allele: ${variant.star_allele}`}
                        </li>
                      ))
                    ) : (
                      <li className="text-sm text-gray-500">No specific variants detected</li>
                    )}
                  </ul>
                </div>
              </div>
            )}
          </div>

          {/* Clinical Recommendation */}
          <div className="mb-6">
            <h3 className="font-semibold text-gray-900 mb-2">Clinical Recommendation</h3>
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="font-medium text-blue-900 mb-2">
                {result.clinical_recommendation.action}
              </p>
              {result.clinical_recommendation.dosing_adjustment && (
                <p className="text-sm text-blue-800 mb-1">
                  <strong>Dosing Adjustment:</strong> {result.clinical_recommendation.dosing_adjustment}
                </p>
              )}
              {result.clinical_recommendation.monitoring && (
                <p className="text-sm text-blue-800 mb-1">
                  <strong>Monitoring:</strong> {result.clinical_recommendation.monitoring}
                </p>
              )}
              {result.clinical_recommendation.alternative_drugs && (
                <p className="text-sm text-blue-800">
                  <strong>Alternative Drugs:</strong> {result.clinical_recommendation.alternative_drugs.join(', ')}
                </p>
              )}
            </div>
          </div>

          {/* LLM Explanation */}
          <div className="mb-6">
            <h3 className="font-semibold text-gray-900 mb-2">Clinical Explanation</h3>
            <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
              <p className="text-sm text-gray-800 mb-3">
                {result.llm_generated_explanation.summary}
              </p>
              {result.llm_generated_explanation.variant_citations && result.llm_generated_explanation.variant_citations.length > 0 && (
                <div className="mt-3 pt-3 border-t border-purple-300">
                  <p className="text-xs font-medium text-purple-900 mb-1">Variant Citations:</p>
                  <p className="text-xs text-purple-800">
                    {result.llm_generated_explanation.variant_citations.join(', ')}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Quality Metrics */}
          <div className="text-xs text-gray-500">
            <p>VCF Parsing: {result.quality_metrics.vcf_parsing_success ? '✓ Success' : '✗ Failed'}</p>
            <p>Variants Analyzed: {result.quality_metrics.variants_analyzed}</p>
            <p>PGx Variants Found: {result.quality_metrics.pgx_variants_found}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
