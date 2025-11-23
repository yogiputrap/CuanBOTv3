from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database import get_db
from ..models.transaction import Transaction
from ..models.prediction import Prediction, PredictionType
from ..services.ml_forecasting import forecasting_service
from ..services.ml_anomaly import anomaly_detection_service
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

class ForecastRequest(BaseModel):
    user_id: int = None
    periods: int = 30

class AnomalyRequest(BaseModel):
    user_id: int = None

@router.post("/forecast")
def generate_forecast(request: ForecastRequest, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if request.user_id:
        query = query.filter(Transaction.user_id == request.user_id)
    
    transactions = query.all()
    
    transactions_data = [
        {
            "id": t.id,
            "transaction_type": t.transaction_type.value,
            "amount": t.amount,
            "transaction_date": t.transaction_date,
            "category": t.category
        }
        for t in transactions
    ]
    
    forecast_result = forecasting_service.forecast_revenue(transactions_data, request.periods)
    
    prediction = Prediction(
        prediction_type=PredictionType.FORECAST,
        prediction_data=forecast_result,
        metadata={"user_id": request.user_id, "periods": request.periods}
    )
    db.add(prediction)
    db.commit()
    
    return forecast_result

@router.post("/anomaly")
def detect_anomalies(request: AnomalyRequest, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if request.user_id:
        query = query.filter(Transaction.user_id == request.user_id)
    
    transactions = query.all()
    
    transactions_data = [
        {
            "id": t.id,
            "transaction_type": t.transaction_type.value,
            "amount": t.amount,
            "transaction_date": t.transaction_date,
            "category": t.category
        }
        for t in transactions
    ]
    
    anomaly_result = anomaly_detection_service.detect_anomalies(transactions_data)
    
    if anomaly_result["status"] == "success":
        for anomaly in anomaly_result["anomalies"]:
            transaction = db.query(Transaction).filter(Transaction.id == anomaly["transaction_id"]).first()
            if transaction:
                transaction.is_anomaly = 1
                transaction.anomaly_score = anomaly["anomaly_score"]
        
        db.commit()
    
    prediction = Prediction(
        prediction_type=PredictionType.ANOMALY,
        prediction_data=anomaly_result,
        metadata={"user_id": request.user_id}
    )
    db.add(prediction)
    db.commit()
    
    return anomaly_result

@router.get("/history")
def get_prediction_history(
    prediction_type: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Prediction)
    
    if prediction_type:
        query = query.filter(Prediction.prediction_type == prediction_type)
    
    predictions = query.order_by(Prediction.created_at.desc()).limit(limit).all()
    
    return {
        "predictions": [
            {
                "id": p.id,
                "prediction_type": p.prediction_type.value,
                "prediction_data": p.prediction_data,
                "metadata": p.metadata,
                "created_at": p.created_at
            }
            for p in predictions
        ]
    }
