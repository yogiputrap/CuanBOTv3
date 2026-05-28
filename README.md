# CuanBot v3 🤖💰

**Akunting Chatbot untuk UMKM Indonesia**

<img width="1920" height="1440" alt="Image" src="https://github.com/user-attachments/assets/9f4ddfdd-57d0-4095-b265-9871562077c0" />

CuanBot adalah aplikasi chatbot berbasis Telegram yang membantu UMKM mengelola keuangan mereka dengan mudah menggunakan Natural Language Processing (NLP) dan Machine Learning.

## 🌟 Fitur Utama

### 1. **Telegram Bot Interface**
- Pencatatan transaksi via chat natural language
- Support untuk:
  - 💰 Pemasukan (Income)
  - 💸 Pengeluaran (Expense)
  - 📝 Piutang (Receivable)
  - 📝 Hutang (Payable)
- Ringkasan keuangan otomatis
- Pertanyaan seputar akunting dengan AI

### 2. **Dashboard Web (Next.js)**
- 📊 Real-time monitoring transaksi
- 📈 Visualisasi data dengan charts:
  - Line chart untuk trend transaksi harian
  - Pie chart untuk breakdown kategori
  - Bar chart untuk perbandingan income vs expense
- 🎯 ML Model Predictions:
  - **Forecasting**: Prediksi pendapatan 30 hari ke depan
  - **Anomaly Detection**: Deteksi transaksi mencurigakan
- 🤖 Bot activity logs & monitoring
- 💎 Beautiful & responsive UI dengan Tailwind CSS

### 3. **AI & Machine Learning**
- **LLM Integration (Gemini 2.5 Flash)**:
  - Natural language understanding untuk parsing transaksi
  - Chatbot untuk menjawab pertanyaan akunting
  - Generate summary & insights
  
- **ML Models**:
  - **Time Series Forecasting**: Linear Regression untuk prediksi revenue
  - **Anomaly Detection**: Isolation Forest untuk deteksi fraud/error

### 4. **Backend API (FastAPI)**
- RESTful API untuk dashboard
- Webhook handler untuk Telegram
- PostgreSQL untuk data persistence
- Comprehensive logging system

## 🏗️ Arsitektur

```
┌─────────────────┐
│  Telegram Bot   │
│   (End User)    │
└────────┬────────┘
         │
         ↓ Webhook (via ngrok)
┌─────────────────────────────────────────┐
│          Docker Environment              │
│                                          │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Backend    │    │  Dashboard   │  │
│  │  (FastAPI)   │←───│  (Next.js)   │  │
│  └──────┬───────┘    └──────────────┘  │
│         │                                │
│         ↓                                │
│  ┌──────────────┐                       │
│  │  PostgreSQL  │                       │
│  └──────────────┘                       │
│                                          │
│  ┌──────────────┐                       │
│  │    Ngrok     │                       │
│  └──────────────┘                       │
└─────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Telegram Bot Token (dari @BotFather)
- Gemini API Key (dari Google AI Studio)
- Ngrok Authtoken (dari ngrok.com)

### Setup Steps

1. **Clone & Setup Environment**

```bash
# Clone repository
git clone <repository-url>
cd CuanBOTv3

# Copy environment template
cp .env.example .env

# Edit .env dengan credentials Anda
nano .env
```

2. **Configure Environment Variables**

Edit file `.env`:

```env
# Database
POSTGRES_USER=cuanbot
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=cuanbot_db
DATABASE_URL=postgresql://cuanbot:your_secure_password_here@postgres:5432/cuanbot_db

# Telegram Bot (dapatkan dari @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Gemini API (dapatkan dari Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key

# Ngrok (dapatkan dari ngrok.com)
NGROK_AUTHTOKEN=your_ngrok_authtoken

# Backend
SECRET_KEY=generate_random_secret_key_here

# Dashboard
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Start Application**

```bash
# Build dan start semua services
docker-compose up -d

# Check logs
docker-compose logs -f
```

4. **Setup Webhook**

```bash
# Akses ngrok dashboard untuk mendapatkan public URL
open http://localhost:4040

# Copy ngrok URL (contoh: https://abc123.ngrok.io)
# Update .env dengan webhook URL:
TELEGRAM_WEBHOOK_URL=https://abc123.ngrok.io/webhook/telegram

# Restart backend service
docker-compose restart backend
```

5. **Access Applications**

- 🤖 **Telegram Bot**: Cari bot Anda di Telegram dan start chat
- 📊 **Dashboard**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📡 **Ngrok Dashboard**: http://localhost:4040

## 📱 Cara Menggunakan Bot

### Mencatat Transaksi

Cukup chat dengan bahasa natural:

```
✅ "Terima pembayaran dari customer 500rb"
✅ "Bayar listrik 300 ribu"
✅ "Piutang si Budi 1 juta"
✅ "Hutang ke supplier 2 juta untuk stok barang"
✅ "Dapat transfer dari customer A sebesar 1.5 juta untuk pembelian produk X"
```

### Commands

- `/start` - Mulai bot & lihat panduan
- `/help` - Bantuan lengkap
- `/summary` - Ringkasan keuangan Anda

### Bertanya

```
"Bagaimana cara menghitung laba rugi?"
"Apa itu arus kas?"
"Jelaskan tentang piutang dan hutang"
```

## 🎨 Dashboard Features

### 1. Overview Cards
- Total Pemasukan
- Total Pengeluaran
- Saldo
- Jumlah Transaksi

### 2. Charts & Analytics
- **Daily Transaction Chart**: Trend harian income vs expense
- **Category Breakdown**: Pie chart pengeluaran per kategori
- **Revenue Forecast**: Prediksi 30 hari ke depan (ML)
- **Anomaly Detection**: Transaksi mencurigakan (ML)

### 3. Bot Monitoring
- Real-time logs
- Activity tracking
- Error monitoring

## 🔧 Development

### Project Structure

```
CuanBOTv3/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── services/          # Business logic
│   │   │   ├── telegram_bot.py
│   │   │   ├── llm_service.py
│   │   │   ├── ml_forecasting.py
│   │   │   └── ml_anomaly.py
│   │   ├── api/               # REST API endpoints
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
│
├── dashboard/                  # Next.js Dashboard
│   ├── src/
│   │   ├── app/               # Next.js 14 App Router
│   │   ├── components/        # React components
│   │   └── lib/               # Utilities & API client
│   ├── package.json
│   └── Dockerfile
│
├── init-db/                    # Database initialization
│   └── init.sql
│
├── docker-compose.yml          # Docker orchestration
├── .env.example               # Environment template
└── README.md
```

### Running Locally (Development)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Dashboard:**
```bash
cd dashboard
npm install
npm run dev
```

### API Documentation

Setelah backend running, akses:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

### Manual Testing Telegram Bot

1. Start bot dengan `/start`
2. Test pencatatan transaksi:
   ```
   "Terima uang 500rb dari customer"
   "Bayar gaji 2 juta"
   ```
3. Check dengan `/summary`

### Testing Dashboard

1. Access http://localhost:3000
2. Verify semua cards menampilkan data
3. Test ML features:
   - Click "Generate Forecast"
   - Click "Detect Anomalies"

## 📊 Database Schema

### Tables

- **users**: Telegram user data
- **transactions**: Financial transactions
- **bot_logs**: Bot interaction logs
- **predictions**: ML prediction results

## 🔐 Security Notes

⚠️ **Important for Production:**

1. Change all default passwords
2. Use strong SECRET_KEY
3. Enable HTTPS for webhook
4. Implement authentication for dashboard
5. Add rate limiting
6. Regular database backups

## 🐛 Troubleshooting

### Webhook Issues

```bash
# Check ngrok status
curl http://localhost:4040/api/tunnels

# Manually set webhook
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<NGROK_URL>/webhook/telegram"
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker-compose exec postgres psql -U cuanbot -d cuanbot_db -c "\dt"

# Reset database
docker-compose down -v
docker-compose up -d
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f dashboard
```

## 🚀 Deployment (Production)

### Using Docker Compose

1. Update `.env` dengan production credentials
2. Use production-grade secrets
3. Setup proper domain & SSL
4. Use managed PostgreSQL (e.g., AWS RDS, Google Cloud SQL)
5. Deploy to cloud (AWS, GCP, Azure)

### Recommendations

- Use Kubernetes for scalability
- Implement CI/CD pipeline
- Setup monitoring (Prometheus, Grafana)
- Add backup automation
- Implement proper logging (ELK stack)

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for Indonesian UMKM**
