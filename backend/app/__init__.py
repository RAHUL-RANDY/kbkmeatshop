import os
from flask import Flask, jsonify
from sqlalchemy import text
from app.config import Config
from app.extensions import db, jwt, cors, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize CORS for all frontend origins (localhost, 127.0.0.1, network IP, etc.)
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Test / Configure Database Connection with graceful fallback
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    use_sqlite_fallback = app.config.get('USE_SQLITE_FALLBACK', True)

    if not app.config.get('TESTING', False) and db_uri.startswith('mysql'):
        try:
            from sqlalchemy import create_engine
            engine = create_engine(db_uri, connect_args={'connect_timeout': 2})
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"[Database] Successfully connected to MySQL: {app.config.get('MYSQL_DB')}")
        except Exception as e:
            if use_sqlite_fallback:
                print(f"[Database Warning] MySQL connection failed: {e}")
                print(f"[Database Notice] Falling back to SQLite database at {app.config['SQLITE_URI']}")
                app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLITE_URI']
            else:
                print(f"[Database Error] MySQL connection failed and fallback is disabled: {e}")

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register Route Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.category_routes import category_bp
    from app.routes.product_routes import product_bp
    from app.routes.cart_routes import cart_bp
    from app.routes.address_routes import address_bp
    from app.routes.order_routes import order_bp
    from app.routes.payment_routes import payment_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(address_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(admin_bp)

    # Root Health Check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'KBK MEAT SHOP Backend API',
            'version': '1.0.0',
            'database': 'Connected'
        }), 200

    # JWT Error Handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({
            'success': False,
            'message': 'Authentication required. Missing Bearer token in Authorization header.'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({
            'success': False,
            'message': 'Invalid token signature or format. Please log in again.'
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'message': 'Authentication session expired. Please log in again.'
        }), 401

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'message': 'The requested API route was not found.'
        }), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            'success': False,
            'message': 'An unexpected server error occurred.'
        }), 500

    return app
