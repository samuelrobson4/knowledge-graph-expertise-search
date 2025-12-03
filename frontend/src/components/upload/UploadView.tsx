import { useState } from 'react'
import { Upload, FileText, CheckCircle, Loader2 } from 'lucide-react'
import { cn } from '../../lib/utils'
import GraphVisualization from './GraphVisualization'

const API_BASE = 'http://localhost:8000'

interface UploadStats {
  filename: string
  text_length: number
  extraction_summary: {
    people_count: number
    projects_count: number
    relationships_count: number
  }
  storage_stats: {
    people_inserted: number
    projects_inserted: number
    skills_linked: number
    technologies_linked: number
    relationships_created: number
  }
}

export default function UploadView() {
  const [files, setFiles] = useState<FileList | null>(null)
  const [uploading, setUploading] = useState(false)
  const [uploadResults, setUploadResults] = useState<UploadStats[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFiles(e.target.files)
    setError(null)
    setUploadResults([])
  }

  const handleUpload = async () => {
    if (!files || files.length === 0) {
      setError('Please select at least one file')
      return
    }

    setUploading(true)
    setError(null)
    setUploadResults([])

    const results: UploadStats[] = []

    for (let i = 0; i < files.length; i++) {
      const file = files[i]
      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await fetch(`${API_BASE}/upload`, {
          method: 'POST',
          body: formData,
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || `Upload failed for ${file.name}`)
        }

        const data = await response.json()
        results.push(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Upload failed')
        break
      }
    }

    setUploadResults(results)
    setUploading(false)
  }

  return (
    <div className="grid md:grid-cols-[30%_70%] gap-6">
      {/* Left Column - Upload Section */}
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h2 className="text-2xl font-semibold text-gray-900">Upload Documents</h2>
          <p className="mt-1 text-sm text-gray-600">
            Upload status documents (.pdf, .docx, .txt) to extract knowledge
          </p>
        </div>

        {/* Upload Section */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <div className="flex items-center justify-center w-full">
          <label className={cn(
            "flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-lg cursor-pointer transition-colors",
            uploading ? "border-gray-200 bg-gray-50 cursor-not-allowed" : "border-gray-300 bg-gray-50 hover:bg-gray-100"
          )}>
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <Upload className={cn("w-10 h-10 mb-3", uploading ? "text-gray-400" : "text-gray-500")} />
              <p className="mb-2 text-sm text-gray-600">
                <span className="font-semibold">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-gray-500">PDF, DOCX, or TXT files</p>
            </div>
            <input
              type="file"
              className="hidden"
              multiple
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              disabled={uploading}
            />
          </label>
        </div>

        {files && files.length > 0 && (
          <div className="space-y-2">
            <p className="text-sm font-medium text-gray-700">
              Selected {files.length} file{files.length !== 1 ? 's' : ''}:
            </p>
            <div className="space-y-1">
              {Array.from(files).map((file, i) => (
                <div key={i} className="flex items-center gap-2 text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded-md">
                  <FileText className="w-4 h-4 text-gray-400" />
                  {file.name}
                </div>
              ))}
            </div>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!files || files.length === 0 || uploading}
          className={cn(
            "w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg font-medium transition-all",
            !files || files.length === 0 || uploading
              ? "bg-gray-100 text-gray-400 cursor-not-allowed"
              : "bg-gray-900 text-white hover:bg-gray-800 shadow-sm"
          )}
        >
          {uploading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <Upload className="w-4 h-4" />
              Upload
            </>
          )}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Results */}
      {uploadResults.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-green-700">
            <CheckCircle className="w-5 h-5" />
            <h3 className="text-lg font-semibold">Upload Successful</h3>
          </div>

          {uploadResults.map((result, i) => (
            <div key={i} className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-100">
                <h4 className="font-semibold text-gray-900">{result.filename}</h4>
              </div>

              <div className="px-6 py-4 grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div>
                  <div className="text-xs text-gray-500 mb-1">Text Length</div>
                  <div className="text-lg font-semibold text-gray-900">
                    {result.text_length.toLocaleString()}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-500 mb-1">People</div>
                  <div className="text-lg font-semibold text-gray-900">
                    {result.extraction_summary.people_count}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-500 mb-1">Projects</div>
                  <div className="text-lg font-semibold text-gray-900">
                    {result.extraction_summary.projects_count}
                  </div>
                </div>
                <div>
                  <div className="text-xs text-gray-500 mb-1">Relationships</div>
                  <div className="text-lg font-semibold text-gray-900">
                    {result.extraction_summary.relationships_count}
                  </div>
                </div>
              </div>

              <details className="border-t border-gray-100">
                <summary className="px-6 py-3 text-sm font-medium text-gray-700 cursor-pointer hover:bg-gray-50">
                  Storage Stats
                </summary>
                <div className="px-6 py-4 bg-gray-50 grid grid-cols-2 sm:grid-cols-3 gap-4">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">People Inserted</div>
                    <div className="text-sm font-semibold text-gray-900">
                      {result.storage_stats.people_inserted}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Projects Inserted</div>
                    <div className="text-sm font-semibold text-gray-900">
                      {result.storage_stats.projects_inserted}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Skills Linked</div>
                    <div className="text-sm font-semibold text-gray-900">
                      {result.storage_stats.skills_linked}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Technologies Linked</div>
                    <div className="text-sm font-semibold text-gray-900">
                      {result.storage_stats.technologies_linked}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Relationships Created</div>
                    <div className="text-sm font-semibold text-gray-900">
                      {result.storage_stats.relationships_created}
                    </div>
                  </div>
                </div>
              </details>
            </div>
          ))}
        </div>
      )}
      </div>

      {/* Right Column - Graph Visualization */}
      <div>
        <GraphVisualization refreshTrigger={uploadResults.length} />
      </div>
    </div>
  )
}
