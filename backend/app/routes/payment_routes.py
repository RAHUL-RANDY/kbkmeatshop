from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import Order
from app.services.payment_service import PaymentService

payment_bp = Blueprint('payments', __name__, url_prefix='/api/payments')

@payment_bp.route('/create', methods=['POST'])
@jwt_required()
def create_payment():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    order_id = data.get('order_id')

    if not order_id:
        return jsonify({'success': False, 'message': 'order_id is required.'}), 400

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'success': False, 'message': 'Order not found.'}), 404

    if order.payment_status == 'Paid':
        return jsonify({'success': False, 'message': 'This order has already been paid for.'}), 400

    try:
        payment_data = PaymentService.create_razorpay_order(order)
        return jsonify({
            'success': True,
            'payment': payment_data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to create payment: {str(e)}'}), 500


@payment_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify_payment():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    order_id = data.get('order_id')
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')

    if not order_id or not razorpay_payment_id:
        return jsonify({'success': False, 'message': 'Missing payment verification details.'}), 400

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'success': False, 'message': 'Order not found.'}), 404

    try:
        payment = PaymentService.verify_razorpay_payment(
            order=order,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature
        )
        return jsonify({
            'success': True,
            'message': 'Payment verified and recorded successfully.',
            'payment': payment.to_dict(),
            'order': order.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Verification error: {str(e)}'}), 500
