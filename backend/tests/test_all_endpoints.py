import json

# 1. AUTHENTICATION TESTS
def test_registration_success(client):
    res = client.post('/api/auth/register', json={
        'full_name': 'New User',
        'email': 'newuser@test.com',
        'phone': '9876543299',
        'password': 'Password@123',
        'confirm_password': 'Password@123'
    })
    data = res.get_json()
    assert res.status_code == 201
    assert data['success'] is True
    assert 'access_token' in data
    assert data['user']['email'] == 'newuser@test.com'

def test_duplicate_email_registration(client):
    res = client.post('/api/auth/register', json={
        'full_name': 'Another User',
        'email': 'customer@test.com', # already seeded
        'password': 'Password@123'
    })
    assert res.status_code == 409
    assert res.get_json()['success'] is False

def test_login_invalid_password(client):
    res = client.post('/api/auth/login', json={
        'email': 'customer@test.com',
        'password': 'WrongPassword123'
    })
    assert res.status_code == 401
    assert res.get_json()['success'] is False

def test_login_success(client):
    res = client.post('/api/auth/login', json={
        'email': 'customer@test.com',
        'password': 'Customer@123'
    })
    assert res.status_code == 200
    assert 'access_token' in res.get_json()

def test_get_profile(client, customer_token):
    res = client.get('/api/auth/profile', headers={
        'Authorization': f'Bearer {customer_token}'
    })
    assert res.status_code == 200
    assert res.get_json()['user']['email'] == 'customer@test.com'


# 2. PRODUCT & CATEGORY TESTS
def test_get_categories(client):
    res = client.get('/api/categories')
    assert res.status_code == 200
    data = res.get_json()
    assert data['success'] is True
    assert len(data['categories']) >= 1

def test_get_products(client):
    res = client.get('/api/products')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data['products']) >= 1

def test_search_products(client):
    res = client.get('/api/products/search?q=chicken')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data['products']) >= 1


# 3. CART OPERATIONS & VALIDATION
def test_cart_operations(client, customer_token):
    headers = {'Authorization': f'Bearer {customer_token}'}

    # Add to cart
    res = client.post('/api/cart/add', headers=headers, json={
        'product_code': 'test-chicken',
        'quantity': 2,
        'selected_weight': '1 kg'
    })
    assert res.status_code == 200
    cart = res.get_json()['cart']
    assert cart['items_count'] == 2
    item_id = cart['items'][0]['id']

    # Update qty
    res = client.put(f'/api/cart/update/{item_id}', headers=headers, json={
        'quantity': 3
    })
    assert res.status_code == 200
    assert res.get_json()['cart']['items_count'] == 3

    # Stock validation failure: request more than available stock (stock=10)
    res = client.put(f'/api/cart/update/{item_id}', headers=headers, json={
        'quantity': 999
    })
    assert res.status_code == 400
    assert 'stock' in res.get_json()['message'].lower()

    # Remove item
    res = client.delete(f'/api/cart/remove/{item_id}', headers=headers)
    assert res.status_code == 200
    assert res.get_json()['cart']['items_count'] == 0


# 4. ORDER & CHECKOUT WORKFLOW
def test_checkout_and_cod_order(client, customer_token):
    headers = {'Authorization': f'Bearer {customer_token}'}

    # Get address
    res_addr = client.get('/api/addresses', headers=headers)
    addr_id = res_addr.get_json()['addresses'][0]['id']

    # Add item to cart
    client.post('/api/cart/add', headers=headers, json={
        'product_code': 'test-chicken',
        'quantity': 1,
        'selected_weight': '1 kg'
    })

    # Place COD order
    res_order = client.post('/api/orders', headers=headers, json={
        'address_id': addr_id,
        'payment_method': 'COD',
        'coupon_code': 'FRESH20'
    })
    assert res_order.status_code == 201
    order_data = res_order.get_json()['order']
    assert order_data['order_status'] == 'Confirmed'
    assert order_data['payment_method'] == 'COD'
    assert order_data['discount_amount'] > 0 # FRESH20 discount verified

    order_id = order_data['id']

    # Cancel eligible order
    res_cancel = client.put(f'/api/orders/{order_id}/cancel', headers=headers)
    assert res_cancel.status_code == 200
    assert res_cancel.get_json()['order']['order_status'] == 'Cancelled'


# 5. ONLINE PAYMENT FLOW
def test_online_payment_verification(client, customer_token):
    headers = {'Authorization': f'Bearer {customer_token}'}

    # Add item to cart
    client.post('/api/cart/add', headers=headers, json={
        'product_code': 'test-chicken',
        'quantity': 1,
        'selected_weight': '1 kg'
    })

    # Create Razorpay order
    res_order = client.post('/api/orders', headers=headers, json={
        'payment_method': 'Razorpay'
    })
    assert res_order.status_code == 201
    order = res_order.get_json()['order']

    res_pay = client.post('/api/payments/create', headers=headers, json={
        'order_id': order['id']
    })
    assert res_pay.status_code == 200
    rzp = res_pay.get_json()['payment']
    assert 'razorpay_order_id' in rzp

    # Verify signature
    res_verify = client.post('/api/payments/verify', headers=headers, json={
        'order_id': order['id'],
        'razorpay_order_id': rzp['razorpay_order_id'],
        'razorpay_payment_id': 'pay_test123456',
        'razorpay_signature': 'test_valid_sig'
    })
    assert res_verify.status_code == 200
    assert res_verify.get_json()['order']['payment_status'] == 'Paid'


# 6. ADMIN AUTHORIZATION & CONTROLS
def test_admin_authorization(client, customer_token, admin_token):
    # Customer forbidden from admin dashboard
    res_forbidden = client.get('/api/admin/dashboard', headers={
        'Authorization': f'Bearer {customer_token}'
    })
    assert res_forbidden.status_code == 403

    # Admin authorized
    res_admin = client.get('/api/admin/dashboard', headers={
        'Authorization': f'Bearer {admin_token}'
    })
    assert res_admin.status_code == 200
    stats = res_admin.get_json()['stats']
    assert 'total_customers' in stats
    assert 'total_products' in stats
