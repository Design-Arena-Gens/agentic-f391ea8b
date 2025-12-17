'use client'

import { useState, useEffect } from 'react'
import { Zap, TrendingUp, Award } from 'lucide-react'
import axios from 'axios'

export default function LearningPanel() {
  const [patterns, setPatterns] = useState<any[]>([])
  const [skills, setSkills] = useState<any>({})

  useEffect(() => {
    loadLearningData()
    const interval = setInterval(loadLearningData, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadLearningData = async () => {
    try {
      const [patternsRes, skillsRes] = await Promise.all([
        axios.get(`${process.env.NEXT_PUBLIC_API_URL}/learning/patterns`),
        axios.get(`${process.env.NEXT_PUBLIC_API_URL}/learning/skills`),
      ])
      setPatterns(patternsRes.data.patterns)
      setSkills(skillsRes.data.skills)
    } catch (error) {
      console.error('Error loading learning data:', error)
    }
  }

  const getSkillLevel = (level: number) => {
    if (level >= 8) return { label: 'Expert', color: 'text-purple-500' }
    if (level >= 5) return { label: 'Advanced', color: 'text-blue-500' }
    if (level >= 3) return { label: 'Intermediate', color: 'text-green-500' }
    return { label: 'Beginner', color: 'text-yellow-500' }
  }

  return (
    <div className="space-y-6">
      {/* Patterns Section */}
      <div>
        <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-primary" />
          Detected Patterns
        </h3>
        <div className="space-y-2 max-h-[250px] overflow-y-auto scrollbar-hide">
          {patterns.length === 0 ? (
            <div className="text-center text-gray-400 py-8">
              <TrendingUp className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>No patterns detected yet</p>
            </div>
          ) : (
            patterns.map((pattern, index) => (
              <div
                key={index}
                className="bg-white/5 border border-white/10 rounded-lg p-4"
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="flex gap-1 flex-wrap">
                    {pattern.keywords.map((keyword: string, i: number) => (
                      <span
                        key={i}
                        className="text-xs bg-primary/20 text-primary px-2 py-1 rounded"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                  <span className="text-sm font-semibold text-primary">
                    ×{pattern.frequency}
                  </span>
                </div>
                <p className="text-xs text-gray-400">
                  Last seen: {new Date(pattern.last_seen).toLocaleString()}
                </p>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Skills Section */}
      <div>
        <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
          <Award className="w-5 h-5 text-secondary" />
          Learned Skills
        </h3>
        <div className="space-y-2 max-h-[250px] overflow-y-auto scrollbar-hide">
          {Object.keys(skills).length === 0 ? (
            <div className="text-center text-gray-400 py-8">
              <Award className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>No skills learned yet</p>
            </div>
          ) : (
            Object.entries(skills).map(([name, data]: [string, any]) => {
              const levelInfo = getSkillLevel(data.level)
              return (
                <div
                  key={name}
                  className="bg-white/5 border border-white/10 rounded-lg p-4"
                >
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-semibold">{name}</span>
                    <span className={`text-sm font-semibold ${levelInfo.color}`}>
                      {levelInfo.label}
                    </span>
                  </div>

                  {/* Level bar */}
                  <div className="w-full bg-white/5 rounded-full h-2 mb-2">
                    <div
                      className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full transition-all"
                      style={{ width: `${(data.level / 10) * 100}%` }}
                    />
                  </div>

                  <div className="flex justify-between text-xs text-gray-400">
                    <span>Level {data.level}</span>
                    <span>{data.uses} uses</span>
                    <span>{(data.success_rate * 100).toFixed(0)}% success</span>
                  </div>
                </div>
              )
            })
          )}
        </div>
      </div>
    </div>
  )
}
