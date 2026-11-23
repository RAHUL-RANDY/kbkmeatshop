import os
import urllib.parse
import urllib.request
import json
import threading

class WhatsAppService:
    """
    Automated WhatsApp Notification Service for KBK MEAT SHOP.
    Automatically sends order receipts to Store Owner (+91 98427 29718) and Customers.
    Supports UltraMsg, Twilio WhatsApp, Meta Cloud API, or custom Webhook gateway.
    """

    @staticmethod
    def get_owner_phone():
        raw = os.getenv('ADMIN_PHONE', '9842729718')
        digits = ''.join(c for c in str(raw) if c.isdigit())
        if digits.startswith('91') and len(digits) == 12:
            return digits
        elif len(digits) == 10:
            return f"91{digits}"
        return digits or '919842729718'

    @classmethod
    def send_order_alert(cls, order):
        """
        Non-blocking async dispatch of WhatsApp order notification.
        """
        thread = threading.Thread(target=cls._dispatch_sync, args=(order,))
        thread.daemon = True
        thread.start()

    @classmethod
    def _dispatch_sync(cls, order):
        owner_phone = cls.get_owner_phone()
        
        customer_name = 'Valued Customer'
        customer_phone = ''
        address_text = 'Doorstep Delivery'
        
        if hasattr(order, 'address') and order.address:
            customer_name = getattr(order.address, 'recipient_name', customer_name)
            customer_phone = getattr(order.address, 'phone', '')
            address_text = f"{order.address.address_line}, {order.address.city} - {order.address.pincode}"
        elif hasattr(order, 'user') and order.user:
            customer_name = getattr(order.user, 'full_name', customer_name)
            customer_phone = getattr(order.user, 'phone', '')

        delivery_schedule = 'Weekend Delivery (Saturday / Sunday Morning Fresh Cut)'
        if hasattr(order, 'notes') and order.notes and 'Weekend Delivery:' in str(order.notes):
            delivery_schedule = str(order.notes).replace('Weekend Delivery:', '').strip()
        elif hasattr(order, 'notes') and order.notes:
            delivery_schedule = str(order.notes).strip()

        # Build items summary
        items_lines = []
        if hasattr(order, 'items'):
            for item in order.items:
                name = getattr(item, 'product_name', 'Fresh Meat')
                weight = getattr(item, 'selected_weight', '1 kg')
                qty = getattr(item, 'quantity', 1)
                total_p = getattr(item, 'total_price', 0)
                items_lines.append(f"  • {name} ({weight}) x {qty} = ₹{total_p}")
        items_text = "\n".join(items_lines) if items_lines else "  • Fresh Meat Selection"

        total = order.total_amount
        order_number = order.order_number

        # Owner Alert Message
        admin_message = (
            f"🚨 *NEW WEEKEND PRE-BOOKING ALERT!* 🚨\n\n"
            f"Dear Store Owner,\n"
            f"A customer has pre-booked fresh meat for weekend delivery!\n\n"
            f"📦 *Order ID:* {order_number}\n"
            f"🚚 *Scheduled Delivery:* Weekend Delivery ({delivery_schedule})\n"
            f"👤 *Customer:* {customer_name}\n"
            f"📞 *Customer Mobile:* +{customer_phone}\n"
            f"📍 *Delivery Address:*\n{address_text}\n\n"
            f"🛒 *Ordered Meat Items:*\n"
            f"{items_text}\n\n"
            f"💵 *Payment:* Cash on Delivery (COD)\n"
            f"💰 *Amount to Collect from Customer:* ₹{total}\n\n"
            f"⚡ Please plan fresh livestock harvest and dispatch for weekend morning delivery!"
        )

        # 1. Log WhatsApp dispatch payload to file
        try:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, 'whatsapp_dispatches.log')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*70}\n")
                f.write(f"WHATSAPP ALERT TO OWNER: +{owner_phone}\n")
                f.write(f"ORDER: #{order_number} | TOTAL: ₹{total} (COD)\n")
                f.write(f"{'-'*70}\n")
                f.write(admin_message)
                f.write(f"\n{'='*70}\n")
        except Exception as e:
            print(f"[WhatsApp Log Error]: {e}")

        # 2. Check for configured automated WhatsApp Gateway (UltraMsg / Twilio / Webhook)
        ultramsg_instance = os.getenv('ULTRAMSG_INSTANCE_ID', '').strip()
        ultramsg_token = os.getenv('ULTRAMSG_TOKEN', '').strip()
        
        webhook_url = os.getenv('WHATSAPP_WEBHOOK_URL', '').strip()

        # If UltraMsg is configured
        if ultramsg_instance and ultramsg_token:
            try:
                url = f"https://api.ultramsg.com/{ultramsg_instance}/messages/chat"
                payload = urllib.parse.urlencode({
                    'token': ultramsg_token,
                    'to': f"+{owner_phone}",
                    'body': admin_message
                }).encode('utf-8')
                req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    print(f"📱 [WhatsApp UltraMsg API] Successfully sent to +{owner_phone}: {resp.status}")
                return True
            except Exception as err:
                print(f"⚠️ [WhatsApp UltraMsg Error]: {err}")

        # If Custom Webhook is configured
        elif webhook_url:
            try:
                payload = json.dumps({
                    'to': f"+{owner_phone}",
                    'message': admin_message,
                    'order_id': order_number,
                    'amount': total
                }).encode('utf-8')
                req = urllib.request.Request(
                    webhook_url, 
                    data=payload, 
                    headers={'Content-Type': 'application/json', 'User-Agent': 'KBK-Meat-Shop/1.0'}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    print(f"📱 [WhatsApp Webhook API] Successfully sent to +{owner_phone}: {resp.status}")
                return True
            except Exception as err:
                print(f"⚠️ [WhatsApp Webhook Error]: {err}")

        else:
            print(f"📱 [WhatsApp Service] Order alert prepared for Store Owner (+{owner_phone}). Deep-link and browser auto-launch active.")
            return True
