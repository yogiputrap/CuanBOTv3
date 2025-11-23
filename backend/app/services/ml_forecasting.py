import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

class ForecastingService:
    def __init__(self):
        self.model = None
    
    def prepare_data(self, transactions: List[Dict[str, Any]]) -> pd.DataFrame:
        df = pd.DataFrame(transactions)
        if df.empty:
            return df
        
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df = df[df['transaction_type'] == 'income']
        df = df.groupby(df['transaction_date'].dt.date)['amount'].sum().reset_index()
        df.columns = ['date', 'amount']
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        return df
    
    def forecast_revenue(self, transactions: List[Dict[str, Any]], periods: int = 30) -> Dict[str, Any]:
        df = self.prepare_data(transactions)
        
        if len(df) < 7:
            return {
                "status": "insufficient_data",
                "message": "Minimal 7 hari data diperlukan untuk forecasting",
                "forecast": []
            }
        
        df['days'] = (df['date'] - df['date'].min()).dt.days
        X = df[['days']].values
        y = df['amount'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        last_date = df['date'].max()
        last_day = df['days'].max()
        
        future_days = np.array([[last_day + i] for i in range(1, periods + 1)])
        predictions = model.predict(future_days)
        predictions = np.maximum(predictions, 0)
        
        forecast_dates = [last_date + timedelta(days=i) for i in range(1, periods + 1)]
        
        forecast_data = [
            {
                "date": date.strftime("%Y-%m-%d"),
                "predicted_amount": float(pred),
                "confidence": "medium"
            }
            for date, pred in zip(forecast_dates, predictions)
        ]
        
        return {
            "status": "success",
            "model": "linear_regression",
            "forecast": forecast_data,
            "metadata": {
                "training_samples": len(df),
                "forecast_period_days": periods,
                "average_daily_revenue": float(df['amount'].mean())
            }
        }

forecasting_service = ForecastingService()
