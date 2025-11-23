# 🚀 CuanBot Deployment Guide

Panduan lengkap untuk deploy CuanBot ke production.

## 📋 Pre-requisites

### 1. Telegram Bot Token
1. Buka Telegram dan cari `@BotFather`
2. Send `/newbot`
3. Ikuti instruksi dan beri nama bot Anda
4. Copy token yang diberikan (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Gemini API Key
1. Kunjungi [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Login dengan Google account
3. Click "Create API Key"
4. Copy API key yang digenerate

### 3. Ngrok Account (untuk development/testing)
1. Sign up di [ngrok.com](https://ngrok.com)
2. Go to dashboard dan copy authtoken
3. Atau gunakan domain sendiri untuk production

## 🛠️ Setup Development (Local dengan Ngrok)

### Step 1: Clone & Configure

```bash
# Clone repository
git clone <your-repo-url>
cd CuanBOTv3

# Setup environment
cp .env.example .env
```

### Step 2: Edit .env

```env
# Database
POSTGRES_USER=cuanbot
POSTGRES_PASSWORD=ChangeMeInProduction123!
POSTGRES_DB=cuanbot_db
DATABASE_URL=postgresql://cuanbot:ChangeMeInProduction123!@postgres:5432/cuanbot_db

# Telegram Bot
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_WEBHOOK_URL=  # Will be updated after ngrok starts

# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Ngrok
NGROK_AUTHTOKEN=your_ngrok_authtoken_here

# Backend
BACKEND_PORT=8000
SECRET_KEY=generate-a-random-secret-key-here-use-openssl-rand-base64-32

# Dashboard
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 3: Generate Secret Key

```bash
# Generate random secret key
openssl rand -base64 32
# Copy output dan paste ke SECRET_KEY di .env
```

### Step 4: Start Services

```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Step 5: Configure Webhook

```bash
# Open ngrok dashboard
open http://localhost:4040

# atau check via command line
curl http://localhost:4040/api/tunnels | python3 -m json.tool

# Copy public_url (e.g., https://abc123.ngrok.io)
```

Update `.env`:
```env
TELEGRAM_WEBHOOK_URL=https://abc123.ngrok.io/webhook/telegram
```

Restart backend:
```bash
docker-compose restart backend
```

Set webhook menggunakan script:
```bash
./scripts/set_webhook.sh YOUR_BOT_TOKEN https://abc123.ngrok.io/webhook/telegram
```

### Step 6: Test

1. Open Telegram dan cari bot Anda
2. Send `/start`
3. Test transaction: "Terima uang 500rb"
4. Check dashboard: http://localhost:3000

## 🌐 Production Deployment

### Option 1: Deploy ke VPS (DigitalOcean, Linode, AWS EC2)

#### 1. Provision Server

Minimum specs:
- 2 CPU cores
- 4GB RAM
- 20GB SSD
- Ubuntu 22.04 LTS

#### 2. Initial Server Setup

```bash
# SSH to server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Create app user
adduser cuanbot
usermod -aG docker cuanbot
su - cuanbot
```

#### 3. Deploy Application

```bash
# Clone repository
git clone <your-repo-url>
cd CuanBOTv3

# Configure environment
cp .env.example .env
nano .env  # Edit dengan production values
```

#### 4. Setup Domain & SSL

**Using Nginx + Let's Encrypt:**

```bash
# Install Nginx
sudo apt install nginx certbot python3-certbot-nginx -y

# Setup Nginx config
sudo nano /etc/nginx/sites-available/cuanbot
```

Nginx config:
```nginx
server {
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    server_name dashboard.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/cuanbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Get SSL certificates
sudo certbot --nginx -d api.yourdomain.com -d dashboard.yourdomain.com
```

#### 5. Update Environment

Update `.env` for production:
```env
TELEGRAM_WEBHOOK_URL=https://api.yourdomain.com/webhook/telegram
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

#### 6. Start Application

```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps
./scripts/check_health.sh
```

#### 7. Set Webhook

```bash
./scripts/set_webhook.sh YOUR_BOT_TOKEN https://api.yourdomain.com/webhook/telegram
```

### Option 2: Deploy ke Cloud Platform

#### AWS ECS / Google Cloud Run / Azure Container Instances

1. **Build & Push Images**

```bash
# Build images
docker-compose build

# Tag images
docker tag cuanbot-backend:latest your-registry/cuanbot-backend:latest
docker tag cuanbot-dashboard:latest your-registry/cuanbot-dashboard:latest

# Push to registry
docker push your-registry/cuanbot-backend:latest
docker push your-registry/cuanbot-dashboard:latest
```

2. **Setup Managed Database**

Use managed PostgreSQL:
- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL

Update `DATABASE_URL` in environment variables.

3. **Deploy Containers**

Follow cloud provider documentation for container deployment.

4. **Setup Load Balancer & SSL**

Configure cloud load balancer with SSL certificate.

### Option 3: Kubernetes (for scale)

See `k8s/` directory for Kubernetes manifests (to be created).

## 🔒 Production Security Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY (32+ characters random)
- [ ] Enable HTTPS/SSL for all endpoints
- [ ] Configure firewall (allow only 80, 443, 22)
- [ ] Use managed database with backups
- [ ] Implement rate limiting on API
- [ ] Add authentication to dashboard
- [ ] Setup monitoring & alerts
- [ ] Configure log rotation
- [ ] Regular security updates
- [ ] Use secrets management (AWS Secrets Manager, etc)
- [ ] Implement backup strategy

## 📊 Monitoring

### Setup Basic Monitoring

```bash
# Install monitoring tools
docker-compose -f docker-compose.monitoring.yml up -d
```

Access:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

### Log Management

```bash
# View logs
docker-compose logs -f

# Export logs
docker-compose logs > cuanbot.log

# Setup log rotation
sudo nano /etc/logrotate.d/docker-containers
```

## 🔄 Updates & Maintenance

### Update Application

```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Database Backup

```bash
# Backup database
docker-compose exec postgres pg_dump -U cuanbot cuanbot_db > backup_$(date +%Y%m%d).sql

# Restore database
cat backup_20240101.sql | docker-compose exec -T postgres psql -U cuanbot cuanbot_db
```

### Auto Backup Script

```bash
# Create backup script
nano /home/cuanbot/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/cuanbot/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

cd /home/cuanbot/CuanBOTv3
docker-compose exec -T postgres pg_dump -U cuanbot cuanbot_db | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: backup_$DATE.sql.gz"
```

Setup cron:
```bash
chmod +x /home/cuanbot/backup.sh
crontab -e

# Add line (daily at 2 AM):
0 2 * * * /home/cuanbot/backup.sh >> /home/cuanbot/backup.log 2>&1
```

## 🐛 Troubleshooting Production

### Bot Not Responding

```bash
# Check webhook status
curl https://api.telegram.org/botYOUR_TOKEN/getWebhookInfo

# Check backend logs
docker-compose logs backend

# Reset webhook
./scripts/set_webhook.sh YOUR_TOKEN https://api.yourdomain.com/webhook/telegram
```

### Database Connection Issues

```bash
# Check database
docker-compose exec postgres psql -U cuanbot -d cuanbot_db -c "SELECT version();"

# Check connections
docker-compose exec postgres psql -U cuanbot -d cuanbot_db -c "SELECT * FROM pg_stat_activity;"
```

### High Memory Usage

```bash
# Check resource usage
docker stats

# Restart services
docker-compose restart

# Add memory limits in docker-compose.yml
```

## 📞 Support

Jika ada masalah:
1. Check logs: `docker-compose logs -f`
2. Run health check: `./scripts/check_health.sh`
3. Check documentation
4. Open issue on GitHub

---

**Good luck with your deployment! 🚀**
