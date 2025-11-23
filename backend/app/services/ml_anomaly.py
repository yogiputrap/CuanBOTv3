import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

class AnomalyDetectionService:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
    
    def detect_anomalies(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        if len(transactions) < 10:
            return {
                "status": "insufficient_data",
                "message": "Minimal 10 transaksi diperlukan untuk deteksi anomali",
                "anomalies": []
            }
        
        df = pd.DataFrame(transactions)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        
        features_list = []
        for idx, row in df.iterrows():
            hour = row['transaction_date'].hour if hasattr(row['transaction_date'], 'hour') else 12
            day_of_week = row['transaction_date'].dayofweek
            
            features = [
                row['amount'],
                hour,
                day_of_week,
                1 if row['transaction_type'] == 'expense' else 0
            ]
            features_list.append(features)
        
        X = np.array(features_list)
        
        predictions = self.model.fit_predict(X)
        scores = self.model.score_samples(X)
        
        df['is_anomaly'] = predictions
        df['anomaly_score'] = scores
        
        anomalies = df[df['is_anomaly'] == -1].copy()
        
        anomaly_list = []
        for idx, row in anomalies.iterrows():
            anomaly_list.append({
                "transaction_id": int(row.get('id', idx)),
                "amount": float(row['amount']),
                "transaction_type": row['transaction_type'],
                "date": row['transaction_date'].strftime("%Y-%m-%d %H:%M:%S"),
                "anomaly_score": float(row['anomaly_score']),
                "reason": self._get_anomaly_reason(row, df)
            })
        
        return {
            "status": "success",
            "model": "isolation_forest",
            "total_transactions": len(df),
            "anomalies_detected": len(anomalies),
            "anomalies": anomaly_list
        }
    
    def _get_anomaly_reason(self, anomaly_row, all_data: pd.DataFrame) -> str:
        avg_amount = all_data['amount'].mean()
        std_amount = all_data['amount'].std()
        
        if anomaly_row['amount'] > avg_amount + 2 * std_amount:
            return "Jumlah transaksi jauh di atas rata-rata"
        elif anomaly_row['amount'] < avg_amount - 2 * std_amount:
            return "Jumlah transaksi jauh di bawah rata-rata"
        else:
            return "Pola transaksi tidak biasa"

anomaly_detection_service = AnomalyDetectionService()
