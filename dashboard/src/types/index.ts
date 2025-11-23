export interface Transaction {
  id: number
  user_id: number
  transaction_type: 'income' | 'expense' | 'receivable' | 'payable'
  amount: number
  category: string | null
  description: string | null
  transaction_date: string
  is_anomaly: number
  anomaly_score: number | null
  created_at: string
}

export interface TransactionStats {
  total_income: number
  total_expense: number
  total_receivable: number
  total_payable: number
  balance: number
  transaction_count: number
}

export interface DailyTransaction {
  date: string
  income: number
  expense: number
}

export interface CategoryData {
  category: string
  total: number
  count: number
}

export interface ForecastData {
  date: string
  predicted_amount: number
  confidence: string
}

export interface AnomalyData {
  transaction_id: number
  amount: number
  transaction_type: string
  date: string
  anomaly_score: number
  reason: string
}

export interface BotLog {
  id: number
  user_id: number | null
  level: 'info' | 'warning' | 'error' | 'debug'
  message: string
  user_input: string | null
  bot_response: string | null
  created_at: string
}

export interface DashboardOverview {
  total_users: number
  total_transactions: number
  total_logs: number
  bot_status: string
}
