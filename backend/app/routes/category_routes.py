from flask import Blueprint, jsonify
from app.models.category import Category

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@category_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.filter_by(is_active=True).order_by(Category.id.asc()).all()
    return jsonify({
        'success': True,
        'count': len(categories),
        'categories': [cat.to_dict() for cat in categories]
    }), 200

@category_bp.route('/<identifier>', methods=['GET'])
def get_category(identifier):
    if identifier.isdigit():
        category = Category.query.get(int(identifier))
    else:
        category = Category.query.filter_by(slug=identifier).first()

    if not category or not category.is_active:
        return jsonify({'success': False, 'message': 'Category not found.'}), 404

    return jsonify({
        'success': True,
        'category': category.to_dict()
    }), 200
