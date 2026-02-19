'use client'

interface DrugInputProps {
  value: string
  onChange: (value: string) => void
}

const SUPPORTED_DRUGS = [
  'CODEINE',
  'WARFARIN',
  'CLOPIDOGREL',
  'SIMVASTATIN',
  'AZATHIOPRINE',
  'FLUOROURACIL',
]

export default function DrugInput({ value, onChange }: DrugInputProps) {
  const handleDrugClick = (drug: string) => {
    const currentDrugs = value.split(',').map(d => d.trim()).filter(Boolean)
    
    if (currentDrugs.includes(drug)) {
      // Remove drug if already selected
      onChange(currentDrugs.filter(d => d !== drug).join(', '))
    } else {
      // Add drug
      onChange([...currentDrugs, drug].join(', '))
    }
  }

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Drug Name(s)
      </label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Enter drug names (comma-separated) or select from below"
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
      />
      <div className="mt-3">
        <p className="text-xs text-gray-500 mb-2">Quick select:</p>
        <div className="flex flex-wrap gap-2">
          {SUPPORTED_DRUGS.map((drug) => {
            const isSelected = value.split(',').map(d => d.trim().toUpperCase()).includes(drug)
            return (
              <button
                key={drug}
                onClick={() => handleDrugClick(drug)}
                className={`px-3 py-1 text-sm rounded-full transition-colors ${
                  isSelected
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {drug}
              </button>
            )
          })}
        </div>
      </div>
      <p className="mt-2 text-xs text-gray-500">
        Supported drugs: {SUPPORTED_DRUGS.join(', ')}
      </p>
    </div>
  )
}
