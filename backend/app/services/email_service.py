import os
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class EmailService:
    """
    Automated Email Notification Service for KBK MEAT SHOP.
    Sends beautifully styled order receipts to Store Owner and Customers.
    """

    @staticmethod
    def get_smtp_config():
        return {
            'host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
            'port': int(os.getenv('SMTP_PORT', 587)),
            'user': os.getenv('SMTP_USER', '').strip(),
            'password': os.getenv('SMTP_PASSWORD', '').strip(),
            'use_tls': os.getenv('SMTP_USE_TLS', 'true').lower() in ('true', '1', 'yes'),
            'from_email': os.getenv('SMTP_FROM_EMAIL', os.getenv('SMTP_USER', 'orders@kbkmeatshop.com')).strip(),
            'admin_email': os.getenv('ADMIN_EMAIL', 'kbkmeatshop@gmail.com').strip()
        }

    @classmethod
    def send_order_email(cls, order, target_email=None):
        """
        Builds and dispatches order confirmation email to the owner / recipient.
        """
        config = cls.get_smtp_config()
        recipient = target_email or config['admin_email']
        if not recipient:
            recipient = 'admin@freshmeatmarket.com'

        customer_name = 'Valued Customer'
        if hasattr(order, 'address') and order.address and getattr(order.address, 'recipient_name', None):
            customer_name = order.address.recipient_name
        elif hasattr(order, 'user') and order.user and getattr(order.user, 'full_name', None):
            customer_name = order.user.full_name

        phone = ''
        address_text = 'Doorstep Delivery'
        if hasattr(order, 'address') and order.address:
            phone = getattr(order.address, 'phone', '')
            address_text = f"{order.address.address_line}, {order.address.city} - {order.address.pincode}"
        elif hasattr(order, 'user') and order.user:
            phone = getattr(order.user, 'phone', '')

        delivery_schedule = 'Weekend Delivery (Saturday / Sunday Morning Fresh Cut)'
        if hasattr(order, 'notes') and order.notes and 'Weekend Delivery:' in str(order.notes):
            delivery_schedule = str(order.notes).replace('Weekend Delivery:', '').strip()
        elif hasattr(order, 'notes') and order.notes:
            delivery_schedule = str(order.notes).strip()

        # Build items rows
        items_rows_html = []
        items_rows_text = []
        if hasattr(order, 'items'):
            for item in order.items:
                name = getattr(item, 'product_name', 'Fresh Meat Item')
                weight = getattr(item, 'selected_weight', '1 kg')
                qty = getattr(item, 'quantity', 1)
                unit_price = getattr(item, 'unit_price', 0)
                total_p = getattr(item, 'total_price', unit_price * qty)
                
                items_rows_html.append(f"""
                <tr>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #331518; color: #ffffff; font-weight: 600;">{name} <span style="color: #f43f5e; font-size: 11px;">({weight})</span></td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #331518; text-align: center; color: #d1d5db;">x {qty}</td>
                    <td style="padding: 10px 12px; border-bottom: 1px solid #331518; text-align: right; color: #ffffff; font-weight: bold;">₹{total_p}</td>
                </tr>
                """)
                items_rows_text.append(f"  • {name} ({weight}) x {qty} = ₹{total_p}")

        items_table_html = "".join(items_rows_html) if items_rows_html else "<tr><td colspan='3'>Fresh Meat Selection</td></tr>"
        items_text = "\n".join(items_rows_text) if items_rows_text else "  • Fresh Meat Selection"

        order_num = order.order_number
        total = order.total_amount
        subtotal = getattr(order, 'subtotal', total)
        delivery_charge = getattr(order, 'delivery_charge', 0)
        delivery_str = "FREE" if delivery_charge == 0 else f"₹{delivery_charge}"

        subject = f"🥩 [NEW ORDER #{order_num}] KBK MEAT SHOP - ₹{total} (COD)"

        # Text Body
        text_content = f"""
=====================================================
          KBK MEAT SHOP - ORDER NOTIFICATION
=====================================================

Order ID:           {order_num}
Customer Name:      {customer_name}
Mobile Number:      +{phone}
Delivery Schedule:  {delivery_schedule}
Delivery Address:   {address_text}

-----------------------------------------------------
ORDERED ITEMS:
{items_text}
-----------------------------------------------------

Subtotal:           ₹{subtotal}
Delivery Fee:       {delivery_str}
Grand Total (COD):  ₹{total}
Payment Method:     Cash on Delivery (Pay at Doorstep)

Hygiene Promise: 100% Halal, Farm Slaughtered & Delivered Fresh on Weekend Morning.
Store Helpline / WhatsApp: +91 98427 29718
=====================================================
"""

        # HTML Body
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>KBK MEAT SHOP - Order #{order_num}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0b0204; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #f3f4f6;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0b0204; padding: 30px 10px;">
    <tr>
      <td align="center">
        <!-- Main Card Container -->
        <table role="presentation" width="100%" style="max-width: 600px; background-color: #170508; border-radius: 20px; border: 1px solid #4a151b; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.8);">
          
          <!-- Brand Header -->
          <tr>
            <td style="background: linear-gradient(135deg, #be123c, #881337); padding: 25px 30px; text-align: center;">
              <h1 style="margin: 0; color: #ffffff; font-size: 26px; font-weight: 900; letter-spacing: 1px; text-transform: uppercase;">KBK MEAT SHOP</h1>
              <p style="margin: 4px 0 0; color: #ffe4e6; font-size: 13px; font-weight: 500;">Fresh Chicken & Mutton • Farm Harvested for Weekend Feast</p>
            </td>
          </tr>

          <!-- Order Status Bar -->
          <tr>
            <td style="padding: 20px 30px; background-color: #22070b; border-bottom: 1px solid #3d1217;">
              <table width="100%">
                <tr>
                  <td>
                    <span style="display: inline-block; background-color: #059669; color: #ffffff; font-size: 10px; font-weight: 800; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.5px;">Order Placed (COD)</span>
                    <h2 style="margin: 8px 0 0; font-size: 18px; color: #ffffff;">Order #{order_num}</h2>
                    <p style="margin: 3px 0 0; font-size: 12px; color: #9ca3af;">{datetime.now().strftime('%d %b %Y, %I:%M %p')}</p>
                  </td>
                  <td align="right" valign="top">
                    <span style="font-size: 11px; color: #9ca3af;">Total Amount:</span>
                    <div style="font-size: 24px; font-weight: 900; color: #fb7185;">₹{total}</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Delivery Schedule Highlight Box -->
          <tr>
            <td style="padding: 20px 30px;">
              <div style="background-color: #290a0f; border: 1px solid #e11d48; border-radius: 12px; padding: 15px;">
                <table width="100%">
                  <tr>
                    <td width="30" valign="top" style="font-size: 20px;">🚚</td>
                    <td>
                      <div style="font-size: 11px; text-transform: uppercase; color: #fda4af; font-weight: 800; letter-spacing: 0.5px;">Scheduled Delivery</div>
                      <div style="font-size: 15px; color: #ffffff; font-weight: 700; margin-top: 2px;">{delivery_schedule}</div>
                      <div style="font-size: 11px; color: #10b981; margin-top: 3px;">🌿 Farm-slaughtered fresh on delivery morning, 100% Halal.</div>
                    </td>
                  </tr>
                </table>
              </div>
            </td>
          </tr>

          <!-- Customer & Address Information -->
          <tr>
            <td style="padding: 0 30px 20px;">
              <table width="100%" style="background-color: #120406; border-radius: 12px; padding: 15px; border: 1px solid #2d0e12;">
                <tr>
                  <td width="50%" valign="top" style="padding: 5px;">
                    <span style="font-size: 11px; color: #9ca3af; text-transform: uppercase;">Customer Details</span>
                    <div style="color: #ffffff; font-weight: 700; font-size: 14px; margin-top: 3px;">{customer_name}</div>
                    <div style="color: #fb7185; font-size: 13px; font-weight: 600; margin-top: 2px;">📞 +{phone}</div>
                  </td>
                  <td width="50%" valign="top" style="padding: 5px;">
                    <span style="font-size: 11px; color: #9ca3af; text-transform: uppercase;">Delivery Address</span>
                    <div style="color: #e5e7eb; font-size: 13px; line-height: 1.4; margin-top: 3px;">{address_text}</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Items Ordered Table -->
          <tr>
            <td style="padding: 0 30px 20px;">
              <h3 style="margin: 0 0 12px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; color: #d1d5db;">Ordered Meat Items</h3>
              <table width="100%" cellspacing="0" cellpadding="0" style="background-color: #120406; border-radius: 12px; overflow: hidden; border: 1px solid #2d0e12; font-size: 13px;">
                <thead>
                  <tr style="background-color: #24090d; color: #9ca3af; font-size: 11px; text-transform: uppercase;">
                    <th style="padding: 10px 12px; text-align: left;">Item</th>
                    <th style="padding: 10px 12px; text-align: center;">Qty</th>
                    <th style="padding: 10px 12px; text-align: right;">Total</th>
                  </tr>
                </thead>
                <tbody>
                  {items_table_html}
                </tbody>
              </table>
            </td>
          </tr>

          <!-- Payment Breakdown -->
          <tr>
            <td style="padding: 0 30px 25px;">
              <table width="100%" style="font-size: 13px; color: #9ca3af;">
                <tr>
                  <td style="padding: 4px 0;">Subtotal</td>
                  <td align="right" style="color: #ffffff; font-weight: 600;">₹{subtotal}</td>
                </tr>
                <tr>
                  <td style="padding: 4px 0;">Delivery Fee</td>
                  <td align="right" style="color: #10b981; font-weight: 600;">{delivery_str}</td>
                </tr>
                <tr>
                  <td style="padding: 10px 0 0; font-size: 15px; font-weight: 800; color: #ffffff; border-top: 1px solid #331518;">Total Payable (COD)</td>
                  <td align="right" style="padding: 10px 0 0; font-size: 20px; font-weight: 900; color: #fb7185; border-top: 1px solid #331518;">₹{total}</td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer Actions & Helpline -->
          <tr>
            <td style="padding: 20px 30px; background-color: #120406; border-top: 1px solid #331518; text-align: center;">
              <p style="margin: 0 0 8px; font-size: 12px; color: #9ca3af;">
                Payment Mode: <strong style="color: #f59e0b;">Cash on Delivery (Pay at Doorstep via Cash or UPI QR)</strong>
              </p>
              <p style="margin: 0; font-size: 12px; color: #6b7280;">
                Store Helpline / WhatsApp: <a href="https://wa.me/919842729718" style="color: #fb7185; text-decoration: none; font-weight: 700;">+91 98427 29718</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

        # Dispatch async to recipient
        cls.send_email_async(recipient, subject, text_content, html_content)

        # Also dispatch to customer email if distinct
        customer_email = getattr(order.user, 'email', None) if hasattr(order, 'user') else None
        if customer_email and '@' in customer_email and not customer_email.endswith('@freshmeatmarket.com') and customer_email != recipient:
            cls.send_email_async(customer_email, f"Order Confirmed #{order_num} - KBK MEAT SHOP", text_content, html_content)

        return {
            'recipient': recipient,
            'subject': subject,
            'status': 'dispatched'
        }

    @classmethod
    def send_email_async(cls, to_email, subject, text_content, html_content=None):
        """Dispatches an email in a background thread so checkout response is instant."""
        thread = threading.Thread(
            target=cls.send_email_sync,
            args=(to_email, subject, text_content, html_content)
        )
        thread.daemon = True
        thread.start()

    @classmethod
    def send_email_sync(cls, to_email, subject, text_content, html_content=None):
        """
        Synchronous SMTP execution with robust fallback logging.
        """
        config = cls.get_smtp_config()
        
        # Always log email to sent_emails.log
        try:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, 'sent_emails.log')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*70}\n")
                f.write(f"TIMESTAMP: {datetime.now().isoformat()}\n")
                f.write(f"TO:        {to_email}\n")
                f.write(f"SUBJECT:   {subject}\n")
                f.write(f"{'-'*70}\n")
                f.write(text_content.strip())
                f.write(f"\n{'='*70}\n")
        except Exception as e:
            print(f"[EmailService Log Error]: {e}")

        # If SMTP user and password are provided, send live SMTP email
        if config['user'] and config['password']:
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = config['from_email']
                msg['To'] = to_email

                part1 = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(part1)

                if html_content:
                    part2 = MIMEText(html_content, 'html', 'utf-8')
                    msg.attach(part2)

                if config['port'] == 465:
                    server = smtplib.SMTP_SSL(config['host'], config['port'], timeout=15)
                else:
                    server = smtplib.SMTP(config['host'], config['port'], timeout=15)
                    if config['use_tls']:
                        server.starttls()

                server.login(config['user'], config['password'])
                server.send_message(msg)
                server.quit()
                print(f"📧 [EmailService] Live email successfully delivered to: {to_email}")
                return True
            except Exception as err:
                print(f"⚠️ [EmailService SMTP Error] Failed to send via SMTP to {to_email}: {err}")
                return False
        else:
            print(f"📧 [EmailService] Email formatted & logged to sent_emails.log for: {to_email} (SMTP credentials optional)")
            return True
