import { useState, useEffect, useCallback, useRef, useMemo } from 'react'
import * as React from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import { Loader2, X, RefreshCw } from 'lucide-react'
import { cn } from '../../lib/utils'

const API_BASE = 'http://localhost:8000'

interface GraphNode {
  id: string
  label: string
  type: string
  properties: Record<string, any>
  x?: number
  y?: number
  vx?: number
  vy?: number
}

interface GraphLink {
  source: string | GraphNode
  target: string | GraphNode
  type: string
  label: string
}

interface GraphData {
  nodes: GraphNode[]
  links: GraphLink[]
  stats: {
    node_count: number
    link_count: number
    truncated: boolean
  }
}

interface GraphVisualizationProps {
  refreshTrigger?: number
}

export default function GraphVisualization({ refreshTrigger = 0 }: GraphVisualizationProps) {
  const [graphData, setGraphData] = useState<GraphData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null)
  const [showPeople, setShowPeople] = useState(true)
  const [showProjects, setShowProjects] = useState(true)
  const [showSkills, setShowSkills] = useState(true)
  const graphRef = useRef<any>()

  const fetchGraphData = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE}/graph?limit=500`)
      if (!response.ok) {
        throw new Error('Failed to fetch graph data')
      }
      const data = await response.json()
      setGraphData(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load graph')
    } finally {
      setLoading(false)
    }
  }, [])

  // Filter graph data based on selected node types
  const filteredGraphData = useMemo(() => {
    if (!graphData) return null

    const filteredNodes = graphData.nodes.filter((node) => {
      if (node.type === 'Person' && !showPeople) return false
      if (node.type === 'Project' && !showProjects) return false
      if (node.type === 'Skill' && !showSkills) return false
      return true
    })

    const filteredNodeIds = new Set(filteredNodes.map((n) => n.id))

    const filteredLinks = graphData.links.filter((link) => {
      const sourceId = typeof link.source === 'string' ? link.source : link.source.id
      const targetId = typeof link.target === 'string' ? link.target : link.target.id
      return filteredNodeIds.has(sourceId) && filteredNodeIds.has(targetId)
    })

    return {
      nodes: filteredNodes,
      links: filteredLinks,
      stats: {
        ...graphData.stats,
        node_count: filteredNodes.length,
        link_count: filteredLinks.length,
      },
    }
  }, [graphData, showPeople, showProjects, showSkills])

  useEffect(() => {
    fetchGraphData()
  }, [fetchGraphData, refreshTrigger])

  const handleNodeClick = useCallback((node: GraphNode) => {
    setSelectedNode(node)
  }, [])

  const handleClosePanel = useCallback(() => {
    setSelectedNode(null)
  }, [])

  const getNodeColor = (node: GraphNode) => {
    switch (node.type) {
      case 'Person':
        return '#3B82F6' // blue
      case 'Project':
        return '#8B5CF6' // purple
      case 'Skill':
        return '#F97316' // orange
      default:
        return '#6B7280' // gray
    }
  }

  const getNodeSize = (node: GraphNode) => {
    // Size based on number of connections
    if (!graphData) return 5
    const connections = graphData.links.filter(
      (link) => link.source === node.id || link.target === node.id
    ).length
    return Math.max(5, Math.min(15, 5 + connections))
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-12">
        <div className="flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 text-gray-400 animate-spin mb-4" />
          <p className="text-sm text-gray-600">Loading graph...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-12">
        <div className="flex flex-col items-center justify-center">
          <p className="text-sm text-red-600">{error}</p>
          <button
            onClick={fetchGraphData}
            className="mt-4 px-4 py-2 bg-gray-900 text-white rounded-lg text-sm hover:bg-gray-800"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!graphData || graphData.nodes.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-12">
        <div className="text-center">
          <p className="text-gray-500">No graph data available</p>
          <p className="text-sm text-gray-400 mt-1">Upload documents to see the knowledge graph</p>
        </div>
      </div>
    )
  }

  const displayData = filteredGraphData || graphData

  return (
    <div className="space-y-4">
      {/* Header with Filters */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Knowledge Graph</h3>
          <p className="text-sm text-gray-600">
            Showing {displayData.stats.node_count} of {graphData.stats.node_count} nodes
            {displayData.stats.node_count !== graphData.stats.node_count && ' (filtered)'}
          </p>
        </div>

        <div className="flex items-center gap-4">
          {/* Filters */}
          <div className="flex items-center gap-3">
            <label className="flex items-center gap-1.5 text-xs cursor-pointer">
              <input
                type="checkbox"
                checked={showPeople}
                onChange={(e) => setShowPeople(e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-gray-700">People</span>
            </label>
            <label className="flex items-center gap-1.5 text-xs cursor-pointer">
              <input
                type="checkbox"
                checked={showProjects}
                onChange={(e) => setShowProjects(e.target.checked)}
                className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
              />
              <span className="text-gray-700">Projects</span>
            </label>
            <label className="flex items-center gap-1.5 text-xs cursor-pointer">
              <input
                type="checkbox"
                checked={showSkills}
                onChange={(e) => setShowSkills(e.target.checked)}
                className="rounded border-gray-300 text-orange-600 focus:ring-orange-500"
              />
              <span className="text-gray-700">Skills</span>
            </label>
          </div>

          <button
            onClick={fetchGraphData}
            className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <RefreshCw className="w-3 h-3" />
            Refresh
          </button>
        </div>
      </div>

      {/* Graph Container */}
      <div className="relative bg-white rounded-xl border border-gray-200 overflow-hidden">
        <ForceGraph2D
          ref={graphRef}
          graphData={displayData}
          nodeLabel="label"
          nodeColor={getNodeColor}
          nodeVal={getNodeSize}
          nodeCanvasObject={(node: any, ctx, globalScale) => {
            const label = node.label
            const fontSize = 12 / globalScale
            const nodeSize = getNodeSize(node)

            // Draw node circle
            ctx.beginPath()
            ctx.arc(node.x, node.y, nodeSize, 0, 2 * Math.PI)
            ctx.fillStyle = getNodeColor(node)
            ctx.fill()

            // Draw label if zoomed in enough
            if (globalScale > 1.5) {
              ctx.font = `${fontSize}px Sans-Serif`
              ctx.textAlign = 'center'
              ctx.textBaseline = 'middle'
              ctx.fillStyle = '#1F2937'
              ctx.fillText(label, node.x, node.y + nodeSize + fontSize)
            }
          }}
          linkColor={() => '#D1D5DB'}
          linkWidth={1}
          linkDirectionalParticles={2}
          linkDirectionalParticleWidth={2}
          onNodeClick={handleNodeClick}
          width={typeof window !== 'undefined' ? Math.min(window.innerWidth * 0.65, 1400) : 800}
          height={600}
          backgroundColor="#ffffff"
        />

        {/* Legend */}
        <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg border border-gray-200 p-3 shadow-sm">
          <div className="text-xs font-medium text-gray-700 mb-2">Node Types</div>
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500"></div>
              <span className="text-xs text-gray-600">Person</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-purple-500"></div>
              <span className="text-xs text-gray-600">Project</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-orange-500"></div>
              <span className="text-xs text-gray-600">Skill</span>
            </div>
          </div>
        </div>

        {/* Node Details Panel */}
        {selectedNode && (
          <div className="absolute top-0 right-0 w-80 h-full bg-white border-l border-gray-200 shadow-lg overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
              <h4 className="font-semibold text-gray-900">Node Details</h4>
              <button
                onClick={handleClosePanel}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
              >
                <X className="w-4 h-4 text-gray-500" />
              </button>
            </div>

            <div className="p-4 space-y-4">
              <div>
                <div className="text-xs font-medium text-gray-500 mb-1">Name</div>
                <div className="text-sm font-semibold text-gray-900">{selectedNode.label}</div>
              </div>

              <div>
                <div className="text-xs font-medium text-gray-500 mb-1">Type</div>
                <span
                  className={cn(
                    'inline-block text-xs px-2 py-1 rounded-md font-medium',
                    selectedNode.type === 'Person' && 'bg-blue-100 text-blue-800',
                    selectedNode.type === 'Project' && 'bg-purple-100 text-purple-800',
                    selectedNode.type === 'Skill' && 'bg-orange-100 text-orange-800'
                  )}
                >
                  {selectedNode.type}
                </span>
              </div>

              {selectedNode.properties.description && (
                <div>
                  <div className="text-xs font-medium text-gray-500 mb-1">Description</div>
                  <div className="text-sm text-gray-700">{selectedNode.properties.description}</div>
                </div>
              )}

              <div>
                <div className="text-xs font-medium text-gray-500 mb-2">Connections</div>
                <div className="space-y-2">
                  {graphData?.links
                    .filter(
                      (link) =>
                        (typeof link.source === 'string'
                          ? link.source === selectedNode.id
                          : link.source.id === selectedNode.id) ||
                        (typeof link.target === 'string'
                          ? link.target === selectedNode.id
                          : link.target.id === selectedNode.id)
                    )
                    .map((link, i) => {
                      const isSource =
                        typeof link.source === 'string'
                          ? link.source === selectedNode.id
                          : link.source.id === selectedNode.id
                      const connectedNodeId = isSource
                        ? typeof link.target === 'string'
                          ? link.target
                          : link.target.id
                        : typeof link.source === 'string'
                        ? link.source
                        : link.source.id
                      const connectedNode = graphData.nodes.find((n) => n.id === connectedNodeId)

                      return (
                        <div key={i} className="text-xs bg-gray-50 rounded-lg p-2">
                          <div className="font-medium text-gray-700">
                            {isSource ? '→' : '←'} {link.label}
                          </div>
                          <div className="text-gray-600 mt-0.5">{connectedNode?.label}</div>
                        </div>
                      )
                    })}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
