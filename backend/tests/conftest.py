import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.cart import Cart
from app.models.address import Address

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()

        # Seed test admin
        admin = User(
            full_name='Admin User',
            email='admin@test.com',
            phone='9876543210',
            role='admin'
        )
        admin.set_password('Admin@123')
        db.session.add(admin)

        # Seed test customer
        customer = User(
            full_name='Test Customer',
            email='customer@test.com',
            phone='9876543211',
            role='customer'
        )
        customer.set_password('Customer@123')
        db.session.add(customer)
        db.session.flush()

        # Seed test cart & address for customer
        cart = Cart(user_id=customer.id)
        db.session.add(cart)

        address = Address(
            user_id=customer.id,
            recipient_name='Test Customer',
            phone='9876543211',
            address_line='123 Test Street',
            city='Chennai',
            state='Tamil Nadu',
            pincode='600001',
            is_default=True
        )
        db.session.add(address)

        # Seed test category
        cat = Category(
            category_name='Chicken',
            slug='chicken',
            subtitle='Fresh Poultry',
            description='Farm fresh chicken',
            image='/images/cat-chicken.jpg'
        )
        db.session.add(cat)
        db.session.flush()

        # Seed test product
        prod = Product(
            product_code='test-chicken',
            product_name='Test Country Chicken',
            description='Fresh chicken',
            category_id=cat.id,
            price=300.0,
            original_price=350.0,
            unit='kg',
            weight_options=['500 g', '1 kg', '2 kg'],
            default_weight='1 kg',
            stock_quantity=10,
            is_available=True,
            is_bestseller=True
        )
        db.session.add(prod)

        db.session.commit()
        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def customer_token(client):
    res = client.post('/api/auth/login', json={
        'email': 'customer@test.com',
        'password': 'Customer@123'
    })
    return res.get_json()['access_token']

@pytest.fixture
def admin_token(client):
    res = client.post('/api/auth/login', json={
        'email': 'admin@test.com',
        'password': 'Admin@123'
    })
    return res.get_json()['access_token']
