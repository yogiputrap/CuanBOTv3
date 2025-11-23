from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, timedelta
from ..database import get_db
from ..models.transaction import Transaction, TransactionType
from ..models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: float
    category: Optional[str]
    description: Optional[str]
    transaction_date: datetime
    is_anomaly: int
    anomaly_score: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransactionStats(BaseModel):
    total_income: float
    total_expense: float
    total_receivable: float
    total_payable: float
    balance: float
    transaction_count: int

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    transaction_type: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    transactions = query.order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/stats", response_model=TransactionStats)
def get_transaction_stats(
    user_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    
    transactions = query.all()
    
    total_income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.INCOME)
    total_expense = sum(t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE)
    total_receivable = sum(t.amount for t in transactions if t.transaction_type == TransactionType.RECEIVABLE)
    total_payable = sum(t.amount for t in transactions if t.transaction_type == TransactionType.PAYABLE)
    
    return TransactionStats(
        total_income=total_income,
        total_expense=total_expense,
        total_receivable=total_receivable,
        total_payable=total_payable,
        balance=total_income - total_expense,
        transaction_count=len(transactions)
    )

@router.get("/daily")
def get_daily_transactions(
    days: int = 30,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(
        func.date(Transaction.transaction_date).label('date'),
        Transaction.transaction_type,
        func.sum(Transaction.amount).label('total')
    ).filter(Transaction.transaction_date >= start_date)
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    
    results = query.group_by(
        func.date(Transaction.transaction_date),
        Transaction.transaction_type
    ).all()
    
    daily_data = {}
    for result in results:
        date_str = str(result.date)
        if date_str not in daily_data:
            daily_data[date_str] = {"date": date_str, "income": 0, "expense": 0}
        
        if result.transaction_type == TransactionType.INCOME:
            daily_data[date_str]["income"] = float(result.total)
        elif result.transaction_type == TransactionType.EXPENSE:
            daily_data[date_str]["expense"] = float(result.total)
    
    return {"data": list(daily_data.values())}

@router.get("/by-category")
def get_transactions_by_category(
    user_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total'),
        func.count(Transaction.id).label('count')
    )
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    results = query.group_by(Transaction.category).all()
    
    return {
        "data": [
            {
                "category": r.category or "Uncategorized",
                "total": float(r.total),
                "count": r.count
            }
            for r in results
        ]
    }
