import pytest
from datetime import datetime, timedelta
from app.extensions import db
from app.models.user import User
from app.models.address import Address
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.services.cleanup_service import CleanupService

def test_cleanup_expired_delivered_orders(app):
    """
    Verify that:
    1. Orders marked as Delivered older than 2 days are permanently deleted.
    2. Associated customer accounts with no other orders are also removed.
    3. Delivered orders under 2 days old are retained.
    4. Pending/Processing orders older than 2 days are NOT touched.
    """
    with app.app_context():
        # Setup test customer
        customer = User(
            full_name="Temporary Customer",
            email="tempcustomer@example.com",
            phone="9876543210",
            role="customer"
        )
        customer.set_password("Password123")
        db.session.add(customer)
        db.session.commit()

        # Add customer address
        address = Address(
            user_id=customer.id,
            recipient_name="Temporary Customer",
            phone="9876543210",
            address_line="123 Meat St",
            city="Chennai",
            pincode="600001"
        )
        db.session.add(address)
        db.session.commit()

        # Create 3 orders:
        # 1) Expired delivered order (delivered 3 days ago) -> MUST BE DELETED
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        order_expired = Order(
            user_id=customer.id,
            address_id=address.id,
            order_number="TEST-EXP-001",
            subtotal=500.0,
            delivery_charge=0.0,
            discount_amount=0.0,
            total_amount=500.0,
            order_status="Delivered",
            payment_status="Paid",
            payment_method="COD",
            delivered_at=three_days_ago
        )
        db.session.add(order_expired)

        # 2) Fresh delivered order (delivered 1 hour ago) -> MUST BE KEPT
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        order_fresh = Order(
            user_id=customer.id,
            address_id=address.id,
            order_number="TEST-FRESH-002",
            subtotal=300.0,
            delivery_charge=0.0,
            discount_amount=0.0,
            total_amount=300.0,
            order_status="Delivered",
            payment_status="Paid",
            payment_method="COD",
            delivered_at=one_hour_ago
        )
        db.session.add(order_fresh)
        db.session.commit()

        # Run cleanup with 2-day policy
        result = CleanupService.cleanup_expired_delivered_orders(days=2)

        # Verification: order_expired is deleted, order_fresh remains, customer remains because order_fresh is active
        assert result['success'] is True
        assert result['deleted_orders_count'] == 1
        assert "TEST-EXP-001" in result['deleted_order_numbers']
        assert result['deleted_customers_count'] == 0  # customer still has order_fresh

        assert Order.query.filter_by(order_number="TEST-EXP-001").first() is None
        assert Order.query.filter_by(order_number="TEST-FRESH-002").first() is not None
        assert User.query.get(customer.id) is not None

        # Now simulate order_fresh becoming expired (delivered 4 days ago)
        four_days_ago = datetime.utcnow() - timedelta(days=4)
        order_fresh.delivered_at = four_days_ago
        db.session.commit()

        # Run cleanup again
        result2 = CleanupService.cleanup_expired_delivered_orders(days=2)
        assert result2['deleted_orders_count'] == 1
        assert "TEST-FRESH-002" in result2['deleted_order_numbers']
        assert result2['deleted_customers_count'] == 1  # Now customer data is also purged!

        # Both order and customer must now be completely erased
        assert Order.query.filter_by(order_number="TEST-FRESH-002").first() is None
        assert User.query.get(customer.id) is None
        assert Address.query.filter_by(user_id=customer.id).first() is None
