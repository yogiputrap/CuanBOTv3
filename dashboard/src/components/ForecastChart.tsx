'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function ForecastChart() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  const generateForecast = async () => {
    setLoading(true)
    try {
      const result = await api.generateForecast(30)
      if (result.status === 'success') {
        const chartData = result.forecast.map((item: any) => ({
          date: item.date,
          predicted: item.predicted_amount
        }))
        setData(chartData)
      }
    } catch (error) {
      console.error('Error generating forecast:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Prediksi Pendapatan (30 Hari Ke Depan)</h3>
        <button
          onClick={generateForecast}
          disabled={loading}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400 transition-colors"
        >
          {loading ? 'Generating...' : 'Generate Forecast'}
        </button>
      </div>
      
      {data.length === 0 ? (
        <div className="h-64 flex items-center justify-center text-gray-500">
          Klik tombol untuk generate forecast
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip formatter={(value: any) => `Rp ${value.toLocaleString('id-ID')}`} />
            <Legend />
            <Line type="monotone" dataKey="predicted" stroke="#8b5cf6" name="Prediksi Pendapatan" strokeWidth={2} strokeDasharray="5 5" />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
