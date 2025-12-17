'use client'

import { useState, useEffect } from 'react'
import { Activity, Database, Brain, Zap } from 'lucide-react'
import axios from 'axios'

export default function StatsPanel() {
  const [stats, setStats] = useState<any>(null)

  useEffect(() => {
    loadStats()
    const interval = setInterval(loadStats, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadStats = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/memory/stats`
      )
      setStats(response.data)
    } catch (error) {
      console.error('Error loading stats:', error)
    }
  }

  if (!stats) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin">
          <Activity className="w-8 h-8 text-primary" />
        </div>
      </div>
    )
  }

  const statCards = [
    {
      label: 'Vector Memories',
      value: stats.vector_memories,
      icon: Database,
      color: 'text-blue-500',
    },
    {
      label: 'Episodes',
      value: stats.episodes,
      icon: Brain,
      color: 'text-purple-500',
    },
    {
      label: 'Patterns',
      value: stats.learning_stats.total_patterns,
      icon: Zap,
      color: 'text-yellow-500',
    },
    {
      label: 'Skills',
      value: stats.learning_stats.total_skills,
      icon: Activity,
      color: 'text-green-500',
    },
  ]

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold mb-4">System Statistics</h3>

      <div className="grid grid-cols-2 gap-3">
        {statCards.map((card, index) => (
          <div
            key={index}
            className="bg-white/5 border border-white/10 rounded-lg p-4"
          >
            <card.icon className={`w-5 h-5 ${card.color} mb-2`} />
            <p className="text-2xl font-bold">{card.value}</p>
            <p className="text-xs text-gray-400">{card.label}</p>
          </div>
        ))}
      </div>

      {stats.learning_stats.avg_skill_level > 0 && (
        <div className="bg-white/5 border border-white/10 rounded-lg p-4">
          <h4 className="text-sm font-semibold mb-2">Avg Skill Level</h4>
          <div className="w-full bg-white/5 rounded-full h-2 mb-2">
            <div
              className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full"
              style={{
                width: `${(stats.learning_stats.avg_skill_level / 10) * 100}%`,
              }}
            />
          </div>
          <p className="text-xs text-gray-400">
            {stats.learning_stats.avg_skill_level.toFixed(1)} / 10
          </p>
        </div>
      )}

      {stats.learning_stats.top_skills.length > 0 && (
        <div className="bg-white/5 border border-white/10 rounded-lg p-4">
          <h4 className="text-sm font-semibold mb-3">Top Skills</h4>
          <div className="space-y-2">
            {stats.learning_stats.top_skills.slice(0, 3).map(([name, data]: [string, any], index: number) => (
              <div key={index} className="flex justify-between items-center">
                <span className="text-sm truncate">{name}</span>
                <span className="text-xs text-primary font-semibold">
                  Lvl {data.level}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
