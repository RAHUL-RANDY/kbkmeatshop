import os
import sys

# Ensure backend root is on Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.cart import Cart
from app.models.address import Address

def seed_database():
    app = create_app()

    with app.app_context():
        print("--> Creating database tables if they do not exist...")
        db.create_all()

        # 1. Seed Admin User
        admin_email = app.config.get('ADMIN_EMAIL', 'admin@freshmeatmarket.com')
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                full_name=app.config.get('ADMIN_NAME', 'Market Administrator'),
                email=admin_email,
                phone=app.config.get('ADMIN_PHONE', '9876543210'),
                role='admin',
                is_active=True
            )
            admin.set_password(app.config.get('ADMIN_PASSWORD', 'Admin@123456'))
            db.session.add(admin)
            db.session.flush()

            # Create cart
            cart = Cart(user_id=admin.id)
            db.session.add(cart)
            print(f"--> Created Admin: {admin_email} (Password: {app.config.get('ADMIN_PASSWORD')})")
        else:
            print(f"--> Admin '{admin_email}' already exists.")

        # 2. Seed Demo Customer User
        demo_email = 'rahul@example.com'
        demo_user = User.query.filter_by(email=demo_email).first()
        if not demo_user:
            demo_user = User(
                full_name='Rahul Sharma',
                email=demo_email,
                phone='9876543211',
                role='customer',
                is_active=True
            )
            demo_user.set_password('Customer@123')
            db.session.add(demo_user)
            db.session.flush()

            cart = Cart(user_id=demo_user.id)
            db.session.add(cart)

            # Seed demo delivery address
            demo_address = Address(
                user_id=demo_user.id,
                recipient_name='Rahul Sharma',
                phone='9876543211',
                address_line='No. 42, Anna Nagar West, 2nd Avenue',
                city='Chennai',
                state='Tamil Nadu',
                pincode='600040',
                is_default=True
            )
            db.session.add(demo_address)
            print(f"--> Created Demo Customer: {demo_email} (Password: Customer@123)")
        else:
            print(f"--> Demo user '{demo_email}' already exists.")

        # 3. Seed Categories
        categories_data = [
            {
                'category_name': 'Fresh Chicken',
                'slug': 'chicken',
                'subtitle': 'Hygienic & Farm Fresh',
                'description': 'Free-range, antibiotic-free poultry sourced directly from bio-secured local farms.',
                'image': '/images/cat-chicken.jpg',
                'item_count_label': '18 Items'
            },
            {
                'category_name': 'Fresh Mutton',
                'slug': 'mutton',
                'subtitle': 'Tender & High Quality',
                'description': 'Grass-fed tender lamb and goat meat, artfully hand-cut and quality graded.',
                'image': '/images/cat-mutton.jpg',
                'item_count_label': '12 Items'
            },
            {
                'category_name': 'Fresh Fish',
                'slug': 'fish',
                'subtitle': 'Daily Catch & Cleaned',
                'description': 'Daily ocean catch, whole cleaned, gutted, and chilled on ice beds for supreme freshness.',
                'image': '/images/cat-fish.jpg',
                'item_count_label': '15 Items'
            },
            {
                'category_name': 'Farm Fresh Eggs',
                'slug': 'eggs',
                'subtitle': 'Nutritious & Chemical Free',
                'description': 'Organic, farm-laid table eggs with deep golden yolks and thick natural shells.',
                'image': '/images/cat-eggs.jpg',
                'item_count_label': '8 Packs'
            }
        ]

        cat_map = {}
        for cdata in categories_data:
            cat = Category.query.filter_by(slug=cdata['slug']).first()
            if not cat:
                cat = Category(
                    category_name=cdata['category_name'],
                    slug=cdata['slug'],
                    subtitle=cdata['subtitle'],
                    description=cdata['description'],
                    image=cdata['image'],
                    item_count_label=cdata['item_count_label'],
                    is_active=True
                )
                db.session.add(cat)
                db.session.flush()
                print(f"--> Seeded Category: {cat.category_name}")
            cat_map[cdata['slug']] = cat

        # 4. Seed Products
        products_data = [
            {
                'product_code': 'country-chicken',
                'name': 'Country Chicken',
                'category_slug': 'chicken',
                'price': 320.0,
                'original_price': 380.0,
                'unit': 'kg',
                'weight_options': ['500 g', '1 kg', '2 kg'],
                'default_weight': '1 kg',
                'is_bestseller': True,
                'rating': 4.9,
                'reviews_count': 428,
                'image': '/images/prod-country-chicken.jpg',
                'description': 'Rich, natural free-roaming country chicken with tender fibrous texture and authentic rustic flavor. No antibiotics or hormones.',
                'stock_quantity': 150,
                'pieces': '12-16 Pieces',
                'serves': '3-4 Persons'
            },
            {
                'product_code': 'broiler-chicken',
                'name': 'Broiler Chicken',
                'category_slug': 'chicken',
                'price': 220.0,
                'original_price': 260.0,
                'unit': 'kg',
                'weight_options': ['500 g', '1 kg', '2 kg'],
                'default_weight': '1 kg',
                'is_bestseller': False,
                'rating': 4.8,
                'reviews_count': 310,
                'image': '/images/prod-broiler-chicken.jpg',
                'description': 'Juicy and succulent chicken drumsticks and curry cuts, chilled at optimum 0-4°C to retain natural juices and tenderness.',
                'stock_quantity': 200,
                'pieces': '8-10 Pieces',
                'serves': '2-3 Persons'
            },
            {
                'product_code': 'chicken-breast',
                'name': 'Chicken Breast',
                'category_slug': 'chicken',
                'price': 380.0,
                'original_price': 420.0,
                'unit': 'kg',
                'weight_options': ['500 g', '1 kg', '1.5 kg'],
                'default_weight': '1 kg',
                'is_bestseller': False,
                'rating': 4.9,
                'reviews_count': 580,
                'image': '/images/prod-chicken-breast.jpg',
                'description': 'Skinless, boneless lean fillets packed with high protein. Ideal for grilling, keto diets, gym meal preps, and stir-fry recipes.',
                'stock_quantity': 120,
                'pieces': '4-6 Fillets',
                'serves': '4 Persons'
            },
            {
                'product_code': 'mutton-curry-cut',
                'name': 'Mutton Curry Cut',
                'category_slug': 'mutton',
                'price': 780.0,
                'original_price': 850.0,
                'unit': 'kg',
                'weight_options': ['500 g', '1 kg', '2 kg'],
                'default_weight': '1 kg',
                'is_bestseller': True,
                'rating': 5.0,
                'reviews_count': 692,
                'image': '/images/prod-mutton-curry.jpg',
                'description': 'A balance of bone-in and boneless lamb and goat cuts selected from ribs, shoulder, and leg for decadent slow-cooked curries.',
                'stock_quantity': 80,
                'pieces': '16-20 Pieces',
                'serves': '4-5 Persons'
            },
            {
                'product_code': 'mutton-boneless',
                'name': 'Mutton Boneless',
                'category_slug': 'mutton',
                'price': 980.0,
                'original_price': 1080.0,
                'unit': 'kg',
                'weight_options': ['500 g', '1 kg', '1.5 kg'],
                'default_weight': '1 kg',
                'is_bestseller': True,
                'rating': 4.9,
                'reviews_count': 385,
                'image': '/images/prod-mutton-boneless.jpg',
                'description': 'Uniformly diced prime chunks of pure boneless goat meat. Perfect for pan roasts, mutton biryani, kebabs, and gourmet gravies.',
                'stock_quantity': 60,
                'pieces': 'Bite Size Cubes',
                'serves': '4 Persons'
            },
            {
                'product_code': 'farm-fresh-eggs',
                'name': 'Farm Fresh Eggs',
                'category_slug': 'eggs',
                'price': 160.0,
                'original_price': 190.0,
                'unit': '30 Eggs',
                'weight_options': ['6 Eggs', '12 Eggs', '1 Pack (30 Eggs)'],
                'default_weight': '1 Pack (30 Eggs)',
                'is_bestseller': True,
                'rating': 4.9,
                'reviews_count': 840,
                'image': '/images/prod-farm-eggs.jpg',
                'description': 'Farm-laid antibiotic-free table eggs with rich golden yolks and thick shells. Washed, graded, and quality inspected daily.',
                'stock_quantity': 300,
                'pieces': '30 Fresh Eggs',
                'serves': 'Whole Family'
            },
            {
                'product_code': 'salmon-steak',
                'name': 'Atlantic Salmon Steak',
                'category_slug': 'fish',
                'price': 650.0,
                'original_price': 750.0,
                'unit': '500 g',
                'weight_options': ['250 g', '500 g', '1 kg'],
                'default_weight': '500 g',
                'is_bestseller': False,
                'rating': 4.9,
                'reviews_count': 210,
                'image': '/images/prod-salmon-steak.jpg',
                'description': 'Fresh Norwegian Atlantic salmon cut into uniform steaks, rich in Omega-3 fatty acids, vibrant natural color, and tender flaky texture.',
                'stock_quantity': 50,
                'pieces': '2-3 Thick Steaks',
                'serves': '2 Persons'
            },
            {
                'product_code': 'fresh-mackerel',
                'name': 'Fresh Mackerel & Seabass',
                'category_slug': 'fish',
                'price': 360.0,
                'original_price': 420.0,
                'unit': 'kg',
                'weight_options': ['500 g', '1 kg'],
                'default_weight': '1 kg',
                'is_bestseller': False,
                'rating': 4.7,
                'reviews_count': 145,
                'image': '/images/cat-fish.jpg',
                'description': 'Daily ocean catch, whole cleaned and gutted. Ready for spicy coastal tawa fry or aromatic coconut fish curry.',
                'stock_quantity': 90,
                'pieces': '3-4 Whole Fish',
                'serves': '3 Persons'
            }
        ]

        for pdata in products_data:
            prod = Product.query.filter_by(product_code=pdata['product_code']).first()
            cat = cat_map.get(pdata['category_slug'])
            if not prod and cat:
                prod = Product(
                    product_code=pdata['product_code'],
                    product_name=pdata['name'],
                    description=pdata['description'],
                    category_id=cat.id,
                    price=pdata['price'],
                    original_price=pdata['original_price'],
                    unit=pdata['unit'],
                    weight_options=pdata['weight_options'],
                    default_weight=pdata['default_weight'],
                    image=pdata['image'],
                    stock_quantity=pdata['stock_quantity'],
                    is_available=True,
                    is_bestseller=pdata['is_bestseller'],
                    rating=pdata['rating'],
                    reviews_count=pdata['reviews_count'],
                    pieces=pdata['pieces'],
                    serves=pdata['serves']
                )
                db.session.add(prod)
                print(f"--> Seeded Product: {prod.product_name}")

        db.session.commit()
        print("\n✅ Database seed completed successfully!")

if __name__ == '__main__':
    seed_database()
