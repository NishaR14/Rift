'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'

interface FileUploadProps {
  file: File | null
  onFileSelect: (file: File | null) => void
  maxSize: number
}

export default function FileUpload({ file, onFileSelect, maxSize }: FileUploadProps) {
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    setError(null)

    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0]
      if (rejection.errors.some((e: any) => e.code === 'file-too-large')) {
        setError(`File size exceeds ${maxSize / 1024 / 1024} MB limit`)
      } else if (rejection.errors.some((e: any) => e.code === 'file-invalid-type')) {
        setError('Invalid file type. Please upload a .vcf file')
      } else {
        setError('File upload failed')
      }
      return
    }

    if (acceptedFiles.length > 0) {
      const selectedFile = acceptedFiles[0]
      if (selectedFile.size > maxSize) {
        setError(`File size exceeds ${maxSize / 1024 / 1024} MB limit`)
        return
      }
      onFileSelect(selectedFile)
    }
  }, [maxSize, onFileSelect])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/vcf': ['.vcf'],
      'text/plain': ['.vcf'],
    },
    maxSize,
    multiple: false,
  })

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / 1024 / 1024).toFixed(2) + ' MB'
  }

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        VCF File Upload
      </label>
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-indigo-500 bg-indigo-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <input {...getInputProps()} />
        {file ? (
          <div className="space-y-2">
            <div className="text-green-600 font-medium">✓ File selected</div>
            <div className="text-sm text-gray-600">
              {file.name} ({formatFileSize(file.size)})
            </div>
            <button
              onClick={(e) => {
                e.stopPropagation()
                onFileSelect(null)
              }}
              className="text-sm text-red-600 hover:text-red-700"
            >
              Remove file
            </button>
          </div>
        ) : (
          <div>
            <p className="text-gray-600 mb-2">
              {isDragActive
                ? 'Drop the VCF file here'
                : 'Drag & drop a VCF file here, or click to select'}
            </p>
            <p className="text-xs text-gray-500">
              Maximum file size: {maxSize / 1024 / 1024} MB
            </p>
          </div>
        )}
      </div>
      {error && (
        <div className="mt-2 text-sm text-red-600">{error}</div>
      )}
    </div>
  )
}
