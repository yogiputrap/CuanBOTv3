'use client'

import { useEffect, useState } from 'react'
import StatsCards from '@/components/StatsCards'
import TransactionChart from '@/components/TransactionChart'
import CategoryChart from '@/components/CategoryChart'
import ForecastChart from '@/components/ForecastChart'
import AnomalyList from '@/components/AnomalyList'
import BotLogs from '@/components/BotLogs'
import { api } from '@/lib/api'

export default function Dashboard() {
  const [overview, setOverview] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadOverview()
  }, [])

  const loadOverview = async () => {
    try {
      const data = await api.getDashboardOverview()
      setOverview(data)
    } catch (error) {
      console.error('Error loading overview:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">🤖 CuanBot</h1>
              <span className="ml-4 text-sm text-gray-500">Dashboard</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                overview?.bot_status === 'active' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {overview?.bot_status === 'active' ? '🟢 Bot Active' : '🔴 Bot Inactive'}
              </span>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Dashboard Overview</h2>
          <p className="mt-2 text-gray-600">Monitor semua aktivitas keuangan dan bot Anda</p>
        </div>

        <StatsCards />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          <TransactionChart />
          <CategoryChart />
        </div>

        <div className="mt-6">
          <ForecastChart />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          <AnomalyList />
          <BotLogs />
        </div>
      </main>
    </div>
  )
}
