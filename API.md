# 📡 CuanBot API Documentation

Complete API reference for CuanBot backend.

## 🌐 Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## 🔐 Authentication

Currently no authentication required for dashboard access.

**⚠️ For Production:** Implement JWT or API key authentication.

## 📊 Endpoints

### System Endpoints

#### GET `/`

Get API information.

**Response:**
```json
{
  "message": "CuanBot API",
  "version": "1.0.0",
  "status": "running"
}
```

#### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

#### GET `/docs`

Interactive API documentation (Swagger UI).

#### GET `/redoc`

Alternative API documentation (ReDoc).

---

### Dashboard Endpoints

#### GET `/api/dashboard/overview`

Get dashboard overview statistics.

**Response:**
```json
{
  "total_users": 5,
  "total_transactions": 42,
  "total_logs": 128,
  "bot_status": "active"
}
```

---

### Transaction Endpoints

#### GET `/api/transactions/`

List all transactions with pagination.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)
- `transaction_type` (string): Filter by type (income/expense/receivable/payable)
- `user_id` (int): Filter by user ID

**Example:**
```bash
GET /api/transactions/?skip=0&limit=10&transaction_type=income
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "transaction_type": "income",
    "amount": 500000,
    "category": "penjualan",
    "description": "Pembayaran dari customer",
    "transaction_date": "2024-11-23T10:30:00Z",
    "is_anomaly": 0,
    "anomaly_score": null,
    "created_at": "2024-11-23T10:30:00Z"
  }
]
```

#### GET `/api/transactions/stats`

Get transaction statistics.

**Query Parameters:**
- `user_id` (int): Filter by user
- `start_date` (datetime): Start date filter
- `end_date` (datetime): End date filter

**Example:**
```bash
GET /api/transactions/stats?user_id=1
```

**Response:**
```json
{
  "total_income": 5000000,
  "total_expense": 2000000,
  "total_receivable": 1000000,
  "total_payable": 500000,
  "balance": 3000000,
  "transaction_count": 42
}
```

#### GET `/api/transactions/daily`

Get daily transaction aggregates.

**Query Parameters:**
- `days` (int): Number of days (default: 30)
- `user_id` (int): Filter by user

**Example:**
```bash
GET /api/transactions/daily?days=30
```

**Response:**
```json
{
  "data": [
    {
      "date": "2024-11-23",
      "income": 500000,
      "expense": 300000
    },
    {
      "date": "2024-11-22",
      "income": 750000,
      "expense": 200000
    }
  ]
}
```

#### GET `/api/transactions/by-category`

Get transactions grouped by category.

**Query Parameters:**
- `user_id` (int): Filter by user
- `transaction_type` (string): Filter by type

**Example:**
```bash
GET /api/transactions/by-category?transaction_type=expense
```

**Response:**
```json
{
  "data": [
    {
      "category": "operasional",
      "total": 1500000,
      "count": 5
    },
    {
      "category": "gaji",
      "total": 3000000,
      "count": 2
    }
  ]
}
```

---

### Prediction Endpoints

#### POST `/api/predictions/forecast`

Generate revenue forecast using ML.

**Request Body:**
```json
{
  "user_id": 1,
  "periods": 30
}
```

**Response (Success):**
```json
{
  "status": "success",
  "model": "linear_regression",
  "forecast": [
    {
      "date": "2024-11-24",
      "predicted_amount": 450000,
      "confidence": "medium"
    },
    {
      "date": "2024-11-25",
      "predicted_amount": 460000,
      "confidence": "medium"
    }
  ],
  "metadata": {
    "training_samples": 30,
    "forecast_period_days": 30,
    "average_daily_revenue": 475000
  }
}
```

**Response (Insufficient Data):**
```json
{
  "status": "insufficient_data",
  "message": "Minimal 7 hari data diperlukan untuk forecasting",
  "forecast": []
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/predictions/forecast \
  -H "Content-Type: application/json" \
  -d '{"periods": 30}'
```

#### POST `/api/predictions/anomaly`

Detect anomalies in transactions.

**Request Body:**
```json
{
  "user_id": 1
}
```

**Response (Success):**
```json
{
  "status": "success",
  "model": "isolation_forest",
  "total_transactions": 50,
  "anomalies_detected": 3,
  "anomalies": [
    {
      "transaction_id": 42,
      "amount": 5000000,
      "transaction_type": "expense",
      "date": "2024-11-23 14:30:00",
      "anomaly_score": -0.25,
      "reason": "Jumlah transaksi jauh di atas rata-rata"
    }
  ]
}
```

**Response (Insufficient Data):**
```json
{
  "status": "insufficient_data",
  "message": "Minimal 10 transaksi diperlukan untuk deteksi anomali",
  "anomalies": []
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/predictions/anomaly \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### GET `/api/predictions/history`

Get prediction history.

**Query Parameters:**
- `prediction_type` (string): Filter by type (forecast/anomaly)
- `limit` (int): Max records (default: 10)

**Example:**
```bash
GET /api/predictions/history?prediction_type=forecast&limit=5
```

**Response:**
```json
{
  "predictions": [
    {
      "id": 1,
      "prediction_type": "forecast",
      "prediction_data": { /* full forecast data */ },
      "metadata": {
        "user_id": 1,
        "periods": 30
      },
      "created_at": "2024-11-23T15:00:00Z"
    }
  ]
}
```

---

### Bot Logs Endpoints

#### GET `/api/bot-logs/`

Get bot interaction logs.

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Max records (default: 100)
- `level` (string): Filter by level (info/warning/error/debug)
- `user_id` (int): Filter by user

**Example:**
```bash
GET /api/bot-logs/?limit=20&level=info
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "level": "info",
    "message": "User interaction",
    "user_input": "Terima uang 500rb",
    "bot_response": "✅ Transaksi berhasil dicatat!...",
    "created_at": "2024-11-23T10:30:00Z"
  }
]
```

#### GET `/api/bot-logs/stats`

Get bot statistics.

**Response:**
```json
{
  "total_interactions": 128,
  "error_count": 3,
  "success_rate": 97.66
}
```

---

### Webhook Endpoints

#### POST `/webhook/telegram`

Telegram webhook endpoint (used internally by Telegram).

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "update_id": 123456789,
  "message": {
    "message_id": 1,
    "from": {
      "id": 123456,
      "first_name": "John",
      "username": "johndoe"
    },
    "chat": {
      "id": 123456,
      "type": "private"
    },
    "date": 1700000000,
    "text": "Terima uang 500rb"
  }
}
```

**Response:**
```json
{
  "ok": true
}
```

**Note:** This endpoint is called automatically by Telegram. You don't need to call it manually.

---

## 📝 Data Models

### Transaction

```typescript
{
  id: number
  user_id: number
  transaction_type: "income" | "expense" | "receivable" | "payable"
  amount: number
  category: string | null
  description: string | null
  transaction_date: string (ISO 8601)
  is_anomaly: 0 | 1
  anomaly_score: number | null
  created_at: string (ISO 8601)
  updated_at: string (ISO 8601)
}
```

### User

```typescript
{
  id: number
  telegram_id: string
  username: string | null
  first_name: string | null
  last_name: string | null
  is_active: boolean
  created_at: string (ISO 8601)
  updated_at: string (ISO 8601)
}
```

### BotLog

```typescript
{
  id: number
  user_id: number | null
  level: "info" | "warning" | "error" | "debug"
  message: string
  user_input: string | null
  bot_response: string | null
  created_at: string (ISO 8601)
}
```

### Prediction

```typescript
{
  id: number
  prediction_type: "forecast" | "anomaly"
  prediction_data: object
  metadata: object | null
  created_at: string (ISO 8601)
}
```

---

## 🔧 Error Responses

### Standard Error Format

```json
{
  "detail": "Error message here"
}
```

### Common Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

---

## 💡 Usage Examples

### Python

```python
import requests

# Get transaction stats
response = requests.get('http://localhost:8000/api/transactions/stats')
data = response.json()
print(f"Balance: Rp {data['balance']:,}")

# Generate forecast
payload = {"periods": 30}
response = requests.post(
    'http://localhost:8000/api/predictions/forecast',
    json=payload
)
forecast = response.json()
print(f"Forecast status: {forecast['status']}")
```

### JavaScript/TypeScript

```typescript
// Get dashboard overview
const response = await fetch('http://localhost:8000/api/dashboard/overview');
const data = await response.json();
console.log(`Bot status: ${data.bot_status}`);

// Detect anomalies
const response = await fetch('http://localhost:8000/api/predictions/anomaly', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({})
});
const result = await response.json();
console.log(`Anomalies detected: ${result.anomalies_detected}`);
```

### cURL

```bash
# Get stats
curl http://localhost:8000/api/transactions/stats | jq

# Get daily transactions
curl "http://localhost:8000/api/transactions/daily?days=7" | jq

# Generate forecast
curl -X POST http://localhost:8000/api/predictions/forecast \
  -H "Content-Type: application/json" \
  -d '{"periods": 30}' | jq

# Get bot logs
curl "http://localhost:8000/api/bot-logs/?limit=10" | jq
```

---

## 🔒 Security Considerations

### For Production

1. **Add Authentication:**
   - Implement JWT tokens
   - Or use API keys
   - Add rate limiting

2. **Enable CORS Properly:**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],  # Specific domain
       allow_credentials=True,
       allow_methods=["GET", "POST"],
       allow_headers=["*"],
   )
   ```

3. **Use HTTPS:**
   - All endpoints should use SSL/TLS
   - No sensitive data over HTTP

4. **Validate Input:**
   - Already implemented with Pydantic
   - Add additional business logic validation

5. **Monitor & Log:**
   - Log all API access
   - Monitor for unusual patterns
   - Set up alerts

---

## 📊 Rate Limits

**Current:** No rate limiting (development)

**Recommended for Production:**
- 100 requests per minute per IP
- 1000 requests per hour per API key
- Implement using:
  - `slowapi` package
  - Redis for distributed rate limiting
  - Nginx rate limiting

---

## 🧪 Testing API

See [TESTING.md](TESTING.md) for comprehensive API testing guide.

**Quick Test:**
```bash
# Health check
curl http://localhost:8000/health

# Get API docs
open http://localhost:8000/docs
```

---

## 📚 Additional Resources

- **Swagger UI:** http://localhost:8000/docs (interactive)
- **ReDoc:** http://localhost:8000/redoc (documentation)
- **Source Code:** `backend/app/api/` and `backend/app/main.py`

---

**For questions or issues, open a GitHub issue.**
