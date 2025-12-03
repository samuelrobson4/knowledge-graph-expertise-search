import { useState } from 'react'
import { Search, Loader2, Sparkles } from 'lucide-react'
import { cn } from '../../lib/utils'

const API_BASE = 'http://localhost:8000'

interface SearchResult {
  name: string
  all_skills?: string[]
  skills?: string[]
  projects?: any[]
  shared_projects?: string[]
  roles?: string[]
  match_count?: number
  project_count?: number
  description?: string
  techs?: string[]
  technologies?: string[]
}

interface SearchResponse {
  intent: string
  results: SearchResult[]
  result_count: number
  explanation: string
  ranking_strategy: string
  cypher_query: string
}

const EXAMPLE_QUERIES = [
  "Find people with React",
  "Who knows Python?",
  "Projects using GraphQL",
  "Who worked with Sarah Chen?",
  "Show me backend developers",
  "People with leadership skills",
  "What did Marcus Rodriguez work on?",
  "Projects using Python and Docker",
]

export default function SearchView() {
  const [query, setQuery] = useState('')
  const [searching, setSearching] = useState(false)
  const [searchResponse, setSearchResponse] = useState<SearchResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Please enter a search query')
      return
    }

    setSearching(true)
    setError(null)
    setSearchResponse(null)

    try {
      const response = await fetch(`${API_BASE}/search?query=${encodeURIComponent(query)}`)

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Search failed')
      }

      const data = await response.json()
      setSearchResponse(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed')
    } finally {
      setSearching(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const handleExampleClick = (example: string) => {
    setQuery(example)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-semibold text-gray-900">Search Knowledge Graph</h2>
        <p className="mt-1 text-sm text-gray-600">
          Ask questions about people, skills, projects, and collaborations
        </p>
      </div>

      {/* Search Section */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="e.g., Find people with React, Who worked with Sarah?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={searching}
              className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-500"
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={!query.trim() || searching}
            className={cn(
              "px-6 py-2.5 rounded-lg font-medium transition-all flex items-center gap-2",
              !query.trim() || searching
                ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                : "bg-gray-900 text-white hover:bg-gray-800 shadow-sm"
            )}
          >
            {searching ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Searching
              </>
            ) : (
              'Search'
            )}
          </button>
        </div>

        <div className="flex flex-wrap gap-2">
          <span className="text-xs text-gray-500 flex items-center gap-1">
            <Sparkles className="w-3 h-3" />
            Try:
          </span>
          {EXAMPLE_QUERIES.map((example, i) => (
            <button
              key={i}
              onClick={() => handleExampleClick(example)}
              disabled={searching}
              className="text-xs px-3 py-1.5 rounded-md bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Results */}
      {searchResponse && (
        <div className="space-y-4">
          <div className="flex items-baseline justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              {searchResponse.result_count} Result{searchResponse.result_count !== 1 ? 's' : ''}
            </h3>
            <div className="flex items-center gap-2">
              <span className="text-xs px-2 py-1 rounded-md bg-blue-100 text-blue-800 font-medium">
                {searchResponse.intent.replace('_', ' ')}
              </span>
            </div>
          </div>

          <p className="text-sm text-gray-600">{searchResponse.explanation}</p>

          {searchResponse.result_count === 0 ? (
            <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
              <p className="text-gray-500">No results found</p>
              <p className="text-sm text-gray-400 mt-1">Try a different query or check your spelling</p>
            </div>
          ) : (
            <div className="space-y-3">
              {searchResponse.results.map((result, i) => (
                <ResultCard key={i} result={result} intent={searchResponse.intent} />
              ))}
            </div>
          )}

          <details className="bg-gray-50 rounded-lg border border-gray-200">
            <summary className="px-4 py-3 text-sm font-medium text-gray-700 cursor-pointer hover:bg-gray-100 rounded-lg">
              View Generated Query
            </summary>
            <pre className="px-4 py-3 text-xs text-gray-600 overflow-x-auto">
              {searchResponse.cypher_query}
            </pre>
          </details>
        </div>
      )}
    </div>
  )
}

function ResultCard({ result, intent }: { result: SearchResult; intent: string }) {
  const skills = result.all_skills || result.skills || []
  const projects = result.projects || []
  const sharedProjects = result.shared_projects || []
  const roles = result.roles || []
  const technologies = result.techs || result.technologies || []

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <h4 className="text-lg font-semibold text-gray-900">{result.name}</h4>
        <div className="flex gap-2">
          {result.match_count !== undefined && (
            <span className="text-xs px-2 py-1 rounded-md bg-green-100 text-green-800 font-medium">
              {result.match_count} match{result.match_count !== 1 ? 'es' : ''}
            </span>
          )}
          {result.project_count !== undefined && (
            <span className="text-xs px-2 py-1 rounded-md bg-purple-100 text-purple-800 font-medium">
              {result.project_count} shared
            </span>
          )}
        </div>
      </div>

      {result.description && (
        <p className="text-sm text-gray-600 mb-4">{result.description}</p>
      )}

      <div className="space-y-3">
        {skills.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-500 mb-2">Skills</div>
            <div className="flex flex-wrap gap-1.5">
              {skills.map((skill, i) => (
                <span
                  key={i}
                  className="text-xs px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-200"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {technologies.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-500 mb-2">Technologies</div>
            <div className="flex flex-wrap gap-1.5">
              {technologies.map((tech, i) => (
                <span
                  key={i}
                  className="text-xs px-2.5 py-1 rounded-md bg-orange-50 text-orange-700 border border-orange-200"
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        )}

        {projects.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-500 mb-2">Projects</div>
            <div className="space-y-2">
              {projects.map((project, i) => (
                <div key={i} className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-baseline gap-2">
                    <span className="font-medium text-sm text-gray-900">{project.project}</span>
                    {project.role && (
                      <span className="text-xs text-gray-500">• {project.role}</span>
                    )}
                  </div>
                  {project.description && (
                    <p className="text-xs text-gray-600 mt-1">{project.description}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {sharedProjects.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-500 mb-2">Shared Projects</div>
            <div className="flex flex-wrap gap-1.5">
              {sharedProjects.map((project, i) => (
                <span
                  key={i}
                  className="text-xs px-2.5 py-1 rounded-md bg-purple-50 text-purple-700 border border-purple-200"
                >
                  {project}
                </span>
              ))}
            </div>
          </div>
        )}

        {roles.length > 0 && (
          <div>
            <div className="text-xs font-medium text-gray-500 mb-2">Roles</div>
            <div className="flex flex-wrap gap-1.5">
              {roles.map((role, i) => (
                <span
                  key={i}
                  className="text-xs px-2.5 py-1 rounded-md bg-gray-100 text-gray-700 border border-gray-200"
                >
                  {role}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
