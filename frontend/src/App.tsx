import { useState } from 'react'
import UploadView from './components/upload/UploadView'
import SearchView from './components/search/SearchView'
import { Upload, Search } from 'lucide-react'

type View = 'upload' | 'search'

function App() {
  const [activeView, setActiveView] = useState<View>('search')

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <header className="py-8 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-semibold text-gray-900 tracking-tight">
              Who can help? A graph expertise search engine
            </h1>

            {/* Tab Navigation */}
            <nav className="flex gap-2 bg-white rounded-lg p-1 shadow-sm border border-gray-200">
              <button
                onClick={() => setActiveView('search')}
                className={`
                  flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all
                  ${activeView === 'search'
                    ? 'bg-gray-900 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}
                `}
              >
                <Search className="w-4 h-4" />
                Search
              </button>
              <button
                onClick={() => setActiveView('upload')}
                className={`
                  flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all
                  ${activeView === 'upload'
                    ? 'bg-gray-900 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}
                `}
              >
                <Upload className="w-4 h-4" />
                Upload
              </button>
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="py-8">
          {activeView === 'upload' && <UploadView />}
          {activeView === 'search' && <SearchView />}
        </main>
      </div>
    </div>
  )
}

export default App
