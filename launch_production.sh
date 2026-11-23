#!/usr/bin/env bash
set -e

# ==============================================================================
# Fresh Meat Market - Production Launch Script
# ==============================================================================

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "=================================================================="
echo "  🥩 FRESH MEAT MARKET - PRODUCTION LAUNCH CONTROLLER"
echo "=================================================================="

echo "Select your launch mode:"
echo "  1) Launch locally in Production Mode (Gunicorn + Frontend Build)"
echo "  2) Launch with Docker Compose (Isolated Containers + Nginx)"
echo "  3) Run Full Pre-Flight Health Check & Pytest Suite"
echo "  4) Exit"
echo ""

read -p "Enter choice [1-4]: " CHOICE

case "$CHOICE" in
  1)
    echo "Starting local production build..."
    
    # 1. Frontend Build
    echo "[1/4] Building optimized production frontend..."
    npm run build
    
    # 2. Database check & seed
    echo "[2/4] Ensuring database is seeded..."
    cd backend
    if [ ! -f "fresh_meat_market.db" ]; then
      venv/bin/python seed.py
    fi
    
    # 3. Start Backend with Gunicorn
    echo "[3/4] Starting Flask backend under Gunicorn on port 5001..."
    venv/bin/gunicorn --config gunicorn_config.py run:app &
    BACKEND_PID=$!
    
    # 4. Preview frontend on port 8080 or 3000
    cd ..
    echo "[4/4] Starting production frontend preview..."
    echo "=================================================================="
    echo "  🚀 App Live! Backend: http://127.0.0.1:5001"
    echo "  🚀 Open your browser to test live meat orders & payments!"
    echo "=================================================================="
    npx vite preview --port 3000 --host
    
    # Kill backend on exit
    kill $BACKEND_PID 2>/dev/null || true
    ;;
    
  2)
    echo "Launching with Docker Compose..."
    if ! command -v docker &> /dev/null; then
      echo "Error: docker command not found. Please install Docker Desktop or run Option 1."
      exit 1
    fi
    docker compose up --build -d
    echo "=================================================================="
    echo "  🚀 Containers running in background!"
    echo "  🌐 Web Storefront: http://localhost"
    echo "  🔌 API Backend:    http://localhost:5001/api/health"
    echo "  📊 Check logs with: docker compose logs -f"
    echo "=================================================================="
    ;;

  3)
    echo "Running Pre-Flight checks..."
    echo "Testing backend endpoints..."
    cd backend
    venv/bin/pytest tests/
    cd ..
    echo "Testing frontend compilation..."
    npm run build
    echo "All pre-flight checks PASSED successfully! Ready for real world launch."
    ;;

  *)
    echo "Exiting."
    exit 0
    ;;
esac
