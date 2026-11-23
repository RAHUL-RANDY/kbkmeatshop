# 🚀 FRESH MEAT MARKET - REAL WORLD PRODUCTION LAUNCH GUIDE

Welcome to the real-world deployment handbook for **Fresh Meat Market**! Follow this guide to take your store from localhost to a live domain serving real customers.

---

## ⚡ 1. Quick One-Click Launch Options

We have provided automated scripts and configurations for fast deployment:

### Option A: Local Production Mode
Runs the optimized production frontend build + Gunicorn multi-worker backend:
```bash
./launch_production.sh
# Select option 1
```

### Option B: Complete Docker Containerized Stack
Runs isolated Frontend (Nginx reverse proxy) + Backend (Gunicorn WSGI) with 1 command:
```bash
docker compose up --build -d
```
- Web Storefront: `http://localhost`
- API Health Check: `http://localhost:5001/api/health`
- Check Logs: `docker compose logs -f`
- Stop Containers: `docker compose down`

---

## ☁️ 2. Deploy to the Cloud (Free & Low-Cost Real World Methods)

### Method 1: Split Cloud (Recommended for Zero Maintenance)
- **Frontend**: Deploy on [Vercel](https://vercel.com) or [Netlify](https://netlify.com) (Free tier)
- **Backend & Database**: Deploy on [Render](https://render.com) or [Railway](https://railway.app) (Free / Hobby tier)

#### Step 1: Deploy Backend to Render / Railway
1. Push your repository to GitHub.
2. In Render / Railway, click **New Web Service** and select your GitHub repo.
3. Configure the backend service:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python seed.py`
   - **Start Command**: `gunicorn --config gunicorn_config.py run:app`
   - **Environment Variables**:
     ```env
     FLASK_ENV=production
     SECRET_KEY=generate-a-strong-random-key-here
     JWT_SECRET_KEY=generate-a-strong-jwt-secret-here
     USE_SQLITE_FALLBACK=true
     CORS_ORIGINS=https://your-frontend-domain.vercel.app
     RAZORPAY_KEY_ID=your_razorpay_live_or_test_key
     RAZORPAY_KEY_SECRET=your_razorpay_secret
     ADMIN_EMAIL=admin@freshmeatmarket.com
     ADMIN_PASSWORD=YourSecureAdminPassword123!
     ```
4. Click **Deploy**. Note your live API URL (e.g. `https://freshmeat-api.onrender.com`).

#### Step 2: Deploy Frontend to Vercel / Netlify
1. In Vercel, click **Add New Project** and select your repository.
2. Framework Preset: **Vite**
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. **Environment Variable**:
   ```env
   VITE_API_URL=https://freshmeat-api.onrender.com/api
   ```
6. Click **Deploy**. Your custom store is now live worldwide with auto-SSL!

---

### Method 2: Single VPS Deployment (Ubuntu / AWS EC2 / DigitalOcean)

1. SSH into your VPS server:
   ```bash
   ssh root@your-server-ip
   ```
2. Install Docker and Docker Compose:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
   ```
3. Clone your repository:
   ```bash
   git clone <your-repo-url>
   cd "MEATE SHOP"
   ```
4. Start the stack:
   ```bash
   docker compose up --build -d
   ```
5. Point your domain (e.g., `api.freshmeat.com` and `freshmeat.com`) to `your-server-ip` via A-records in your DNS (GoDaddy, Namecheap, Cloudflare).
6. Enable free SSL with Certbot:
   ```bash
   apt install certbot python3-certbot-nginx -y
   certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

---

## 💳 3. Live Payment Gateway Setup (Razorpay)

By default, the store is pre-configured with **Cash On Delivery (COD)** and **Razorpay Sandbox**.

To take real customer payments in India:
1. Log in to your [Razorpay Dashboard](https://dashboard.razorpay.com).
2. Go to **Account & Settings** → **API Keys**.
3. Switch from **Test Mode** to **Live Mode**.
4. Generate your **Live Key ID** (`rzp_live_...`) and **Live Key Secret**.
5. Update your backend environment variables:
   ```env
   RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxx
   RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxx
   ```
6. Restart your backend service. Live UPI, Card, NetBanking, and Wallet payments will now debit real funds into your linked bank account!

---

## 🔑 4. Administrator Credentials

Your store comes pre-seeded with a master administration panel:
- **Admin Email**: `admin@freshmeatmarket.com`
- **Admin Password**: `Admin@123456`
- **Admin Features**:
  - Live revenue & order statistics
  - Real-time order fulfillment & status updating (Processing -> Out for Delivery -> Delivered)
  - Product catalog inventory management (Add/Edit stock, toggle availability, prices)
  - Customer order cancellation & instant refund handling

*(To change the admin password, update `ADMIN_PASSWORD` in your backend `.env` before running `seed.py` or update it in the database).*

---

## ✅ 5. Pre-Flight Production Checklist

- [x] Gunicorn multi-worker WSGI configured (`backend/gunicorn_config.py`)
- [x] Dynamic production CORS support (`CORS_ORIGINS`)
- [x] Multi-stage Docker containerization (`Dockerfile.frontend`, `Dockerfile.backend`, `docker-compose.yml`)
- [x] High-performance Nginx reverse proxy configuration (`nginx/nginx.conf`)
- [x] SPA fallback rules for Vercel (`vercel.json`) & Netlify (`_redirects`)
- [x] 12/12 Automated API & checkout tests passing
- [x] Production frontend asset bundling verified without errors (`dist/`)
- [x] One-click production launch automation script (`launch_production.sh`)
