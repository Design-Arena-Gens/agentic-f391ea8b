'use client'

import { useState, useEffect } from 'react'
import { Wrench, Code, FileText, Calculator, Globe } from 'lucide-react'
import axios from 'axios'

export default function ToolsPanel() {
  const [tools, setTools] = useState<any[]>([])

  useEffect(() => {
    loadTools()
  }, [])

  const loadTools = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/tools`)
      setTools(response.data.tools)
    } catch (error) {
      console.error('Error loading tools:', error)
    }
  }

  const getToolIcon = (name: string) => {
    if (name.includes('code')) return Code
    if (name.includes('file')) return FileText
    if (name.includes('calculate')) return Calculator
    if (name.includes('search')) return Globe
    return Wrench
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
        <Wrench className="w-5 h-5 text-primary" />
        Available Tools
      </h3>

      <div className="grid grid-cols-1 gap-3 max-h-[550px] overflow-y-auto scrollbar-hide">
        {tools.length === 0 ? (
          <div className="text-center text-gray-400 py-8">
            <Wrench className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>Loading tools...</p>
          </div>
        ) : (
          tools.map((tool, index) => {
            const Icon = getToolIcon(tool.name)
            return (
              <div
                key={index}
                className="bg-white/5 border border-white/10 rounded-lg p-4 hover:border-primary/50 transition-colors"
              >
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Icon className="w-5 h-5 text-primary" />
                  </div>

                  <div className="flex-1">
                    <h4 className="font-semibold mb-1">{tool.name}</h4>
                    <p className="text-sm text-gray-400 mb-3">{tool.description}</p>

                    {tool.input_schema.properties && (
                      <div className="space-y-1">
                        <p className="text-xs text-gray-500">Parameters:</p>
                        {Object.entries(tool.input_schema.properties).map(
                          ([key, value]: [string, any]) => (
                            <div
                              key={key}
                              className="text-xs bg-white/5 rounded px-2 py-1 flex justify-between"
                            >
                              <span className="text-primary font-mono">{key}</span>
                              <span className="text-gray-400">{value.type}</span>
                            </div>
                          )
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}
