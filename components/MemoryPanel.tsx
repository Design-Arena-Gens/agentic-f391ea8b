'use client'

import { useState, useEffect } from 'react'
import { Search, Database, Clock, Trash2 } from 'lucide-react'
import axios from 'axios'

export default function MemoryPanel() {
  const [query, setQuery] = useState('')
  const [memories, setMemories] = useState<any[]>([])
  const [episodes, setEpisodes] = useState<any[]>([])
  const [activeView, setActiveView] = useState<'search' | 'episodes'>('search')

  useEffect(() => {
    loadEpisodes()
  }, [])

  const searchMemories = async () => {
    if (!query.trim()) return

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/memory/query`,
        { query, n_results: 10 }
      )
      setMemories(response.data.memories)
    } catch (error) {
      console.error('Error searching memories:', error)
    }
  }

  const loadEpisodes = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/memory/episodes?n=20`
      )
      setEpisodes(response.data.episodes)
    } catch (error) {
      console.error('Error loading episodes:', error)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      searchMemories()
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setActiveView('search')}
          className={`flex-1 py-2 rounded-lg transition-colors ${
            activeView === 'search'
              ? 'bg-primary text-white'
              : 'bg-white/5 text-gray-400 hover:text-white'
          }`}
        >
          <Database className="w-4 h-4 inline mr-2" />
          Vector Search
        </button>
        <button
          onClick={() => setActiveView('episodes')}
          className={`flex-1 py-2 rounded-lg transition-colors ${
            activeView === 'episodes'
              ? 'bg-primary text-white'
              : 'bg-white/5 text-gray-400 hover:text-white'
          }`}
        >
          <Clock className="w-4 h-4 inline mr-2" />
          Episodes
        </button>
      </div>

      {activeView === 'search' ? (
        <>
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Search memories..."
              className="flex-1 bg-white/5 border border-white/10 rounded-lg px-4 py-2 focus:outline-none focus:border-primary"
            />
            <button
              onClick={searchMemories}
              className="bg-primary hover:bg-primary/80 rounded-lg px-4 py-2 transition-colors"
            >
              <Search className="w-5 h-5" />
            </button>
          </div>

          <div className="space-y-2 max-h-[500px] overflow-y-auto scrollbar-hide">
            {memories.length === 0 ? (
              <div className="text-center text-gray-400 py-8">
                <Database className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>Search to find relevant memories</p>
              </div>
            ) : (
              memories.map((memory, index) => (
                <div
                  key={index}
                  className="bg-white/5 border border-white/10 rounded-lg p-4"
                >
                  <p className="text-sm mb-2">{memory.content}</p>
                  <div className="flex justify-between text-xs text-gray-400">
                    <span>Similarity: {(1 - memory.distance).toFixed(2)}</span>
                    <span>{new Date(memory.metadata.timestamp).toLocaleString()}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      ) : (
        <div className="space-y-2 max-h-[500px] overflow-y-auto scrollbar-hide">
          {episodes.length === 0 ? (
            <div className="text-center text-gray-400 py-8">
              <Clock className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>No episodes yet</p>
            </div>
          ) : (
            episodes.map((episode, index) => (
              <div
                key={index}
                className="bg-white/5 border border-white/10 rounded-lg p-4"
              >
                <div className="mb-2">
                  <span className="text-xs text-gray-400">User:</span>
                  <p className="text-sm">{episode.user_message}</p>
                </div>
                <div className="mb-2">
                  <span className="text-xs text-gray-400">Agent:</span>
                  <p className="text-sm text-primary">{episode.agent_response.substring(0, 100)}...</p>
                </div>
                {episode.tools_used && episode.tools_used.length > 0 && (
                  <div className="flex gap-1 flex-wrap mt-2">
                    {episode.tools_used.map((tool: string, i: number) => (
                      <span
                        key={i}
                        className="text-xs bg-primary/20 text-primary px-2 py-1 rounded"
                      >
                        {tool}
                      </span>
                    ))}
                  </div>
                )}
                <p className="text-xs text-gray-500 mt-2">
                  {new Date(episode.timestamp).toLocaleString()}
                </p>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}
