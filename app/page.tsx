'use client'

import { useState, useEffect } from 'react'
import ChatInterface from '@/components/ChatInterface'
import MemoryPanel from '@/components/MemoryPanel'
import LearningPanel from '@/components/LearningPanel'
import ToolsPanel from '@/components/ToolsPanel'
import StatsPanel from '@/components/StatsPanel'
import { Brain, Zap, Database, Activity } from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState('chat')
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    // Check backend connection
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`)
      .then(() => setIsConnected(true))
      .catch(() => setIsConnected(false))
  }, [])

  const tabs = [
    { id: 'chat', label: 'Chat', icon: Brain },
    { id: 'memory', label: 'Memory', icon: Database },
    { id: 'learning', label: 'Learning', icon: Zap },
    { id: 'tools', label: 'Tools', icon: Activity },
  ]

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="glass-effect border-b border-white/10 p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center glow">
              <Brain className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Nexus AGI
              </h1>
              <p className="text-xs text-gray-400">Advanced Autonomous Agent</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse-slow`} />
              <span className="text-sm text-gray-400">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="glass-effect border-b border-white/10">
        <div className="max-w-7xl mx-auto flex gap-1 p-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                activeTab === tab.id
                  ? 'bg-primary text-white glow'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
            >
              <tab.icon className="w-4 h-4" />
              <span className="font-medium">{tab.label}</span>
            </button>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-full">
          {/* Main Panel */}
          <div className="lg:col-span-2 glass-effect rounded-xl p-6">
            {activeTab === 'chat' && <ChatInterface />}
            {activeTab === 'memory' && <MemoryPanel />}
            {activeTab === 'learning' && <LearningPanel />}
            {activeTab === 'tools' && <ToolsPanel />}
          </div>

          {/* Side Panel */}
          <div className="glass-effect rounded-xl p-6">
            <StatsPanel />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="glass-effect border-t border-white/10 p-4 mt-8">
        <div className="max-w-7xl mx-auto text-center text-sm text-gray-400">
          <p>Nexus AGI v1.0.0 - Built with Next.js & FastAPI</p>
        </div>
      </footer>
    </div>
  )
}
