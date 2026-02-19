'use client'

import { useState } from 'react'
import FileUpload from '@/components/FileUpload'
import DrugInput from '@/components/DrugInput'
import ResultsDisplay from '@/components/ResultsDisplay'
import { AnalysisResult } from '@/types'

export default function Home() {
  const [vcfFile, setVcfFile] = useState<File | null>(null)
  const [drugs, setDrugs] = useState<string>('')
  const [results, setResults] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyze = async () => {
    if (!vcfFile) {
      setError('Please upload a VCF file')
      return
    }

    if (!drugs.trim()) {
      setError('Please enter at least one drug name')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const formData = new FormData()
      formData.append('vcf_file', vcfFile)
      formData.append('drugs', drugs)

      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5000'
      const response = await fetch(`${backendUrl}/api/analyze`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Analysis failed')
      }

      const data = await response.json()
      setResults(data.results)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            PharmaGuard
          </h1>
          <p className="text-xl text-gray-600">
            AI-Powered Pharmacogenomic Risk Assessment
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Analyze patient genetic data and predict personalized drug risks
          </p>
        </header>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="space-y-6">
            <FileUpload 
              file={vcfFile} 
              onFileSelect={setVcfFile}
              maxSize={5 * 1024 * 1024}
            />

            <DrugInput 
              value={drugs}
              onChange={setDrugs}
            />

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={loading || !vcfFile || !drugs.trim()}
              className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Analyzing...' : 'Analyze Pharmacogenomic Risk'}
            </button>
          </div>
        </div>

        {results && (
          <ResultsDisplay results={results} />
        )}
      </div>
    </main>
  )
}
