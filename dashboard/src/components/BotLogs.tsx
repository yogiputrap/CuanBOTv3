'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { MessageSquare, AlertCircle, Info } from 'lucide-react'

export default function BotLogs() {
  const [logs, setLogs] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadLogs()
    const interval = setInterval(loadLogs, 10000)
    return () => clearInterval(interval)
  }, [])

  const loadLogs = async () => {
    try {
      const data = await api.getBotLogs(20)
      setLogs(data)
    } catch (error) {
      console.error('Error loading logs:', error)
    } finally {
      setLoading(false)
    }
  }

  const getLogIcon = (level: string) => {
    switch (level) {
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-600" />
      case 'warning':
        return <AlertCircle className="h-4 w-4 text-yellow-600" />
      default:
        return <Info className="h-4 w-4 text-blue-600" />
    }
  }

  const getLogColor = (level: string) => {
    switch (level) {
      case 'error':
        return 'bg-red-50 border-red-200'
      case 'warning':
        return 'bg-yellow-50 border-yellow-200'
      default:
        return 'bg-blue-50 border-blue-200'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Bot Activity Logs</h3>
        <MessageSquare className="h-5 w-5 text-gray-400" />
      </div>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {loading ? (
          <div className="text-center py-8 text-gray-500">Loading logs...</div>
        ) : logs.length === 0 ? (
          <div className="text-center py-8 text-gray-500">Belum ada log aktivitas</div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className={`border rounded p-3 ${getLogColor(log.level)}`}>
              <div className="flex items-start space-x-2">
                {getLogIcon(log.level)}
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 truncate">
                    {log.user_input || log.message}
                  </p>
                  {log.bot_response && (
                    <p className="text-xs text-gray-600 mt-1 truncate">
                      Bot: {log.bot_response.substring(0, 100)}...
                    </p>
                  )}
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(log.created_at).toLocaleString('id-ID')}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
