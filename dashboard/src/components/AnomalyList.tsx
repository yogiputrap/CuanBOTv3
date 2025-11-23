'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { AlertTriangle } from 'lucide-react'

export default function AnomalyList() {
  const [anomalies, setAnomalies] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const detectAnomalies = async () => {
    setLoading(true)
    try {
      const result = await api.detectAnomalies()
      if (result.status === 'success') {
        setAnomalies(result.anomalies || [])
      }
    } catch (error) {
      console.error('Error detecting anomalies:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Deteksi Anomali Transaksi</h3>
        <button
          onClick={detectAnomalies}
          disabled={loading}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-400 transition-colors"
        >
          {loading ? 'Detecting...' : 'Detect Anomalies'}
        </button>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto">
        {anomalies.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            {loading ? 'Detecting anomalies...' : 'Klik tombol untuk deteksi anomali'}
          </div>
        ) : (
          anomalies.map((anomaly, index) => (
            <div key={index} className="border border-red-200 rounded-lg p-4 bg-red-50">
              <div className="flex items-start space-x-3">
                <AlertTriangle className="h-5 w-5 text-red-600 mt-0.5" />
                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <p className="font-medium text-gray-900">
                      Rp {anomaly.amount.toLocaleString('id-ID')}
                    </p>
                    <span className="text-xs bg-red-200 text-red-800 px-2 py-1 rounded">
                      {anomaly.transaction_type}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">{anomaly.reason}</p>
                  <p className="text-xs text-gray-500 mt-1">{anomaly.date}</p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
