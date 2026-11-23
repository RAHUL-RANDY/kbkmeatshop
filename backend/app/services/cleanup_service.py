import logging
import threading
import time
from datetime import datetime, timedelta
from app.extensions import db
from app.models.order import Order
from app.models.user import User

logger = logging.getLogger(__name__)

class CleanupService:
    """
    Automated Data Retention & Cleanup Service:
    Permanently deletes orders and associated customer data 2 days (48 hours)
    after order delivery completion.
    """

    @staticmethod
    def cleanup_expired_delivered_orders(days=2):
        """
        Deletes orders and associated customer data 2 days after order status is 'Delivered'.
        - Finds orders with order_status == 'Delivered' where delivered_at (or updated_at fallback) <= now - days.
        - Deletes the orders (cascading items, payment).
        - For the customers owning those orders: if they have role == 'customer' and have no remaining orders,
          deletes their saved addresses, carts, and user account.
        Returns dict with statistics.
        """
        now = datetime.utcnow()
        cutoff = now - timedelta(days=days)

        expired_orders = Order.query.filter(
            Order.order_status == 'Delivered',
            db.or_(
                Order.delivered_at <= cutoff,
                db.and_(Order.delivered_at.is_(None), Order.updated_at <= cutoff)
            )
        ).all()

        deleted_orders_count = 0
        deleted_customers_count = 0
        deleted_order_numbers = []
        customer_ids_to_check = set()

        for order in expired_orders:
            deleted_order_numbers.append(order.order_number)
            if order.user_id:
                customer_ids_to_check.add(order.user_id)
            db.session.delete(order)
            deleted_orders_count += 1

        db.session.flush()

        # Check if customer accounts have any other active/remaining orders
        for user_id in customer_ids_to_check:
            user = User.query.get(user_id)
            if user and user.role == 'customer':
                remaining_orders_count = Order.query.filter_by(user_id=user.id).count()
                if remaining_orders_count == 0:
                    db.session.delete(user)
                    deleted_customers_count += 1

        db.session.commit()

        logger.info(
            f"[DATA RETENTION POLICY] Purged {deleted_orders_count} delivered orders (>{days} days old) "
            f"and {deleted_customers_count} customer accounts."
        )

        return {
            'success': True,
            'policy_days': days,
            'cutoff': cutoff.isoformat(),
            'deleted_orders_count': deleted_orders_count,
            'deleted_customers_count': deleted_customers_count,
            'deleted_order_numbers': deleted_order_numbers
        }

    @staticmethod
    def start_cleanup_scheduler(app, interval_seconds=3600):
        """
        Starts a background daemon thread that periodically checks and removes expired delivered orders.
        Default interval: every 1 hour (3600s).
        """
        def run_worker():
            # Initial run after 10 seconds of app start
            time.sleep(10)
            while True:
                try:
                    with app.app_context():
                        CleanupService.cleanup_expired_delivered_orders(days=2)
                except Exception as e:
                    logger.error(f"[DATA RETENTION ERROR] Error in periodic cleanup: {e}")
                time.sleep(interval_seconds)

        thread = threading.Thread(target=run_worker, daemon=True, name="DataCleanupWorker")
        thread.start()
        logger.info(f"Order & Customer Data Cleanup background worker started (Interval: {interval_seconds}s).")
        return thread
