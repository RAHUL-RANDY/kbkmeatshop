import os
import sys

# Ensure backend directory is in python search path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.services.cleanup_service import CleanupService

app = create_app()

# Start background cleanup daemon for 2-day order & customer retention policy
CleanupService.start_cleanup_scheduler(app, interval_seconds=3600)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() in ('true', '1')
    print(f"\n========================================================")
    print(f"  🥩 FRESH MEAT MARKET - BACKEND API SERVER")
    print(f"  Running on: http://127.0.0.1:{port}")
    print(f"  Health Check: http://127.0.0.1:{port}/api/health")
    print(f"========================================================\n")
    app.run(host='0.0.0.0', port=port, debug=debug)
