# Changelog

All notable changes to CuanBot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-23

### Added
- 🤖 Telegram bot interface with natural language processing
- 📊 Next.js dashboard with beautiful UI
- 💰 Transaction recording (income, expense, receivable, payable)
- 🧠 LLM integration using Gemini 2.5 Flash for:
  - Natural language understanding
  - Transaction parsing
  - Accounting Q&A
- 🔮 Machine Learning models:
  - Revenue forecasting (Linear Regression)
  - Anomaly detection (Isolation Forest)
- 📈 Data visualization with charts:
  - Daily transaction line chart
  - Category breakdown pie chart
  - Forecast predictions chart
- 🗄️ PostgreSQL database with proper schema
- 🐳 Docker Compose setup for easy deployment
- 🌐 Ngrok integration for webhook tunneling
- 📝 Comprehensive logging and monitoring
- 📚 Complete documentation:
  - README.md
  - QUICKSTART.md
  - DEPLOYMENT.md
  - STRUCTURE.md

### Features

#### Telegram Bot
- `/start` command - Introduction and help
- `/help` command - Detailed usage guide
- `/summary` command - Financial summary with AI insights
- Natural language transaction input
- AI-powered accounting Q&A

#### Dashboard
- Real-time financial statistics cards
- Interactive charts for data visualization
- ML prediction generation (forecast & anomaly)
- Bot activity logs with real-time updates
- Responsive design with Tailwind CSS

#### API
- RESTful endpoints for transactions
- ML prediction endpoints
- Bot logs and monitoring endpoints
- Health check and system info endpoints

### Technical

#### Backend
- FastAPI framework
- SQLAlchemy ORM with PostgreSQL
- Python-telegram-bot for bot handling
- Google Generative AI (Gemini) integration
- Scikit-learn for ML models
- Async/await for performance

#### Frontend
- Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Recharts for data visualization
- Axios for API calls

#### Infrastructure
- Docker Compose orchestration
- PostgreSQL 16 Alpine
- Ngrok for webhook tunneling
- Environment-based configuration
- Volume persistence for data

### Security
- Environment variable configuration
- Database password protection
- Secret key for backend
- CORS configuration
- Input validation

### Documentation
- Comprehensive README with all features
- Quick start guide (5 minutes)
- Production deployment guide
- Project structure reference
- Troubleshooting guides

## [Unreleased]

### Planned Features
- [ ] User authentication for dashboard
- [ ] Multi-language support (EN, ID)
- [ ] Advanced ML models (Prophet for forecasting)
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Mobile app (React Native)
- [ ] Multi-tenancy support
- [ ] Advanced analytics dashboard
- [ ] Export data (CSV, Excel)
- [ ] Recurring transaction templates
- [ ] Budget tracking and alerts
- [ ] Integration with payment gateways
- [ ] WhatsApp bot support
- [ ] Voice message support
- [ ] Image receipt processing (OCR)

---

**Legend:**
- 🤖 Bot feature
- 📊 Dashboard feature
- 🧠 AI/ML feature
- 🗄️ Database feature
- 🐳 Infrastructure
- 📝 Documentation
- 🔒 Security
