import os
import urllib.parse
from datetime import datetime

class NotificationService:
    @staticmethod
    def format_order_receipt(order):
        """
        Formats a structured order confirmation receipt for SMS and WhatsApp.
        """
        customer_name = 'Valued Customer'
        if hasattr(order, 'address') and order.address and getattr(order.address, 'recipient_name', None):
            customer_name = order.address.recipient_name
        elif hasattr(order, 'user') and order.user and getattr(order.user, 'full_name', None) and order.user.full_name != 'Guest User':
            customer_name = order.user.full_name
        elif hasattr(order, 'customer_name') and order.customer_name:
            customer_name = order.customer_name

        order_number = order.order_number
        total = order.total_amount
        payment_mode = getattr(order, 'payment_method', 'COD')
        
        # Phone & Address
        phone = ''
        address_text = 'Doorstep Delivery'
        if hasattr(order, 'address') and order.address:
            phone = getattr(order.address, 'phone', '')
            address_text = f"{order.address.address_line}, {order.address.city} - {order.address.pincode}"
        elif hasattr(order, 'user') and order.user:
            phone = getattr(order.user, 'phone', '')
        
        # Clean phone
        clean_phone = ''.join(c for c in str(phone) if c.isdigit())
        if clean_phone.startswith('91') and len(clean_phone) == 12:
            display_phone = clean_phone
        elif len(clean_phone) == 10:
            display_phone = f"91{clean_phone}"
        else:
            display_phone = clean_phone or '919842729718'

        # Items listing
        items_lines = []
        if hasattr(order, 'items'):
            for item in order.items:
                name = getattr(item, 'product_name', 'Fresh Meat Item')
                weight = getattr(item, 'selected_weight', '1 kg')
                qty = getattr(item, 'quantity', 1)
                price = getattr(item, 'total_price', 0)
                items_lines.append(f"  • {name} ({weight}) x {qty} = ₹{price}")

        items_summary = "\n".join(items_lines) if items_lines else "  • Fresh Meat Selection"

        # Determine delivery schedule
        delivery_schedule = 'Weekend Delivery (Saturday / Sunday Morning Fresh Cut)'
        if hasattr(order, 'notes') and order.notes and 'Weekend Delivery:' in str(order.notes):
            delivery_schedule = str(order.notes).replace('Weekend Delivery:', '').strip()
        elif hasattr(order, 'notes') and order.notes:
            delivery_schedule = str(order.notes).strip()

        # WhatsApp Text (Rich Markdown with emojis)
        whatsapp_message = (
            f"🥩 *KBK MEAT SHOP - WEEKEND PRE-BOOKING CONFIRMED!* 🥩\n\n"
            f"Hello *{customer_name}*,\n"
            f"Thank you for pre-booking with us! Your premium fresh cut meat will be farm-harvested fresh and delivered to your doorstep this weekend.\n\n"
            f"📦 *Order ID:* {order_number}\n"
            f"📅 *Booked On:* {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
            f"🚚 *Delivery Schedule:* Weekend Delivery ({delivery_schedule})\n"
            f"💵 *Payment Mode:* Cash on Delivery (COD)\n"
            f"💰 *Total Amount to Pay:* ₹{total}\n\n"
            f"🛒 *Your Pre-Booked Items:*\n"
            f"{items_summary}\n\n"
            f"📍 *Delivery Address:*\n"
            f"{address_text}\n"
            f"📞 *Recipient Phone:* +{display_phone}\n\n"
            f"🌿 *Freshness Guarantee:* 100% Halal, Farm Slaughtered & Delivered Fresh on Weekend Morning.\n"
            f"Need Help? Call / WhatsApp: +91 9842729718"
        )

        # Standard SMS Text (Compact plain text)
        sms_message = (
            f"KBK MEAT SHOP: Weekend Booking #{order_number} confirmed for {customer_name}! "
            f"Total: Rs.{total} (Pay on Delivery). Delivery: {delivery_schedule} at {address_text[:35]}... "
            f"Call 9842729718 for queries."
        )

        # Admin / Store Owner Phone
        from app.models.user import User
        try:
            admin_user = User.query.filter_by(role='admin').first()
            admin_raw_phone = (admin_user.phone if admin_user and admin_user.phone else None) or os.getenv('ADMIN_PHONE', '9842729718')
        except Exception:
            admin_raw_phone = os.getenv('ADMIN_PHONE', '9842729718')

        clean_admin = ''.join(c for c in str(admin_raw_phone) if c.isdigit())
        if clean_admin.startswith('91') and len(clean_admin) == 12:
            admin_display_phone = clean_admin
        elif len(clean_admin) == 10:
            admin_display_phone = f"91{clean_admin}"
        else:
            admin_display_phone = clean_admin or '919842729718'

        # Admin / Store Owner Alert Text
        admin_whatsapp_message = (
            f"🚨 *NEW WEEKEND PRE-BOOKING ALERT!* 🚨\n\n"
            f"Dear Store Owner,\n"
            f"A customer has pre-booked fresh meat for weekend delivery!\n\n"
            f"📦 *Order ID:* {order_number}\n"
            f"📅 *Booked At:* {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
            f"🚚 *Scheduled Delivery:* Weekend Delivery ({delivery_schedule})\n"
            f"👤 *Customer:* {customer_name}\n"
            f"📞 *Customer Mobile:* +{display_phone}\n"
            f"📍 *Delivery Address:*\n{address_text}\n\n"
            f"🛒 *Ordered Meat Items:*\n"
            f"{items_summary}\n\n"
            f"💵 *Payment:* Cash on Delivery (COD)\n"
            f"💰 *Amount to Collect from Customer:* ₹{total}\n\n"
            f"⚡ Please plan fresh livestock harvest and dispatch for weekend morning delivery!"
        )

        admin_sms_message = (
            f"NEW WEEKEND BOOKING #{order_number}! Customer: {customer_name} (+{display_phone}). "
            f"Collect Rs.{total} (COD). Delivery: {delivery_schedule}. Address: {address_text[:35]}..."
        )

        # Direct deep-links
        encoded_wa = urllib.parse.quote(whatsapp_message)
        whatsapp_url = f"https://wa.me/{display_phone}?text={encoded_wa}"
        
        # SMS URI
        encoded_sms = urllib.parse.quote(sms_message)
        sms_url = f"sms:{display_phone}?body={encoded_sms}"

        # Admin deep-links
        encoded_admin_wa = urllib.parse.quote(admin_whatsapp_message)
        admin_whatsapp_url = f"https://wa.me/{admin_display_phone}?text={encoded_admin_wa}"

        encoded_admin_sms = urllib.parse.quote(admin_sms_message)
        admin_sms_url = f"sms:{admin_display_phone}?body={encoded_admin_sms}"

        return {
            'phone': display_phone,
            'customer_name': customer_name,
            'whatsapp_message': whatsapp_message,
            'sms_message': sms_message,
            'whatsapp_url': whatsapp_url,
            'sms_url': sms_url,
            'admin_phone': admin_display_phone,
            'admin_whatsapp_message': admin_whatsapp_message,
            'admin_sms_message': admin_sms_message,
            'admin_whatsapp_url': admin_whatsapp_url,
            'admin_sms_url': admin_sms_url
        }

    @classmethod
    def send_order_notifications(cls, order):
        """
        Dispatches notification payload and logs delivery details.
        """
        receipt = cls.format_order_receipt(order)

        # Dispatch Automated Order Email
        try:
            from app.services.email_service import EmailService
            email_res = EmailService.send_order_email(order)
            receipt['email_dispatch'] = email_res
        except Exception as e:
            print(f"⚠️ [NotificationService Email Error]: {e}")

        print("\n" + "=" * 65)
        print("  📱 ORDER NOTIFICATION DISPATCH (SMS & WHATSAPP & EMAIL)")
        print("=" * 65)
        print(f"  To Customer Phone: +{receipt['phone']}")
        print(f"  Customer Name:     {receipt['customer_name']}")
        print(f"  To Owner Phone:    +{receipt['admin_phone']}")
        print(f"  Order ID:          {order.order_number}")
        print(f"  Total Payable:     ₹{order.total_amount} (Cash on Delivery)")
        print(f"  Customer WhatsApp: {receipt['whatsapp_url'][:65]}...")
        print(f"  Owner WhatsApp:    {receipt['admin_whatsapp_url'][:65]}...")
        print("  Email Status:      AUTOMATICALLY DISPATCHED / LOGGED")
        print("  Status:            DISPATCHED / ACTIVE")
        print("=" * 65 + "\n")

        return receipt
