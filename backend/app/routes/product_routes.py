from flask import Blueprint, request, jsonify
from app.models.product import Product
from app.models.category import Category

product_bp = Blueprint('products', __name__, url_prefix='/api/products')

@product_bp.route('', methods=['GET'])
def get_products():
    category_slug = request.args.get('category', '').strip().lower()
    search = request.args.get('search', '').strip()
    bestseller_only = request.args.get('bestseller', '').lower() in ('true', '1')
    sort_by = request.args.get('sort', 'popular') # 'popular', 'price-low', 'price-high', 'rating'
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Product.query.filter_by(is_available=True)

    # Category Filter
    if category_slug and category_slug != 'all':
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter(Product.category_id == category.id)
        else:
            # No matching category
            return jsonify({'success': True, 'count': 0, 'products': []}), 200

    # Search Filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.product_name.ilike(search_term)) |
            (Product.description.ilike(search_term)) |
            (Product.product_code.ilike(search_term))
        )

    # Bestseller Filter
    if bestseller_only:
        query = query.filter_by(is_bestseller=True)

    # Price Range Filter
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Sorting
    if sort_by == 'price-low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price-high':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    else:
        # Default 'popular': bestsellers first, then id
        query = query.order_by(Product.is_bestseller.desc(), Product.id.asc())

    products = query.all()

    return jsonify({
        'success': True,
        'count': len(products),
        'products': [p.to_dict() for p in products]
    }), 200


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if not product or not product.is_available:
        return jsonify({'success': False, 'message': 'Product not found.'}), 404

    return jsonify({
        'success': True,
        'product': product.to_dict()
    }), 200


@product_bp.route('/code/<product_code>', methods=['GET'])
def get_product_by_code(product_code):
    product = Product.query.filter_by(product_code=product_code).first()
    if not product or not product.is_available:
        return jsonify({'success': False, 'message': 'Product not found.'}), 404

    return jsonify({
        'success': True,
        'product': product.to_dict()
    }), 200


@product_bp.route('/bestsellers', methods=['GET'])
def get_bestsellers():
    products = Product.query.filter_by(is_available=True, is_bestseller=True).limit(6).all()
    return jsonify({
        'success': True,
        'count': len(products),
        'products': [p.to_dict() for p in products]
    }), 200


@product_bp.route('/search', methods=['GET'])
def search_products():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({'success': True, 'count': 0, 'products': []}), 200

    search_term = f"%{q}%"
    products = Product.query.filter(
        Product.is_available == True,
        (Product.product_name.ilike(search_term) | Product.description.ilike(search_term))
    ).limit(10).all()

    return jsonify({
        'success': True,
        'count': len(products),
        'products': [p.to_dict() for p in products]
    }), 200
