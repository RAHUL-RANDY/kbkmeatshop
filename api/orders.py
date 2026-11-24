from http.server import BaseHTTPRequestHandler
import json
import smtplib
import os
import random
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER', 'kbkmeatshop@gmail.com').strip()
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', 'daadudylfgojcqxe').strip().replace(' ', '')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'kbkmeatshop@gmail.com').strip()

def send_smtp_email(to_email, subject, text_content, html_content):
    if not SMTP_USER or not SMTP_PASSWORD:
        return False
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"KBK MEAT SHOP <{SMTP_USER}>"
        msg['To'] = to_email
        msg['Reply-To'] = ADMIN_EMAIL

        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part1)
        msg.attach(part2)

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"[Vercel SMTP Error]: {e}")
        return False

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'online',
            'service': 'KBK MEAT SHOP Vercel Serverless Orders API'
        }).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body.decode('utf-8')) if body else {}
        except Exception:
            data = {}

        recipient_name = data.get('recipient_name') or 'Valued Customer'
        phone = data.get('phone') or '9842729718'
        customer_email = data.get('email')
        address_line = data.get('address_line') or 'Doorstep Delivery'
        city = data.get('city') or 'Chennai'
        pincode = data.get('pincode') or '600040'
        payment_method = data.get('payment_method') or 'COD'
        delivery_day = data.get('delivery_day') or 'Weekend Morning (6:00 AM - 10:00 AM)'
        items = data.get('items') or []

        # Calculate totals
        subtotal = 0
        items_rows_html = []
        items_rows_text = []

        for it in items:
            name = it.get('name') or it.get('product_name') or 'Fresh Meat'
            weight = it.get('selectedWeight') or it.get('selected_weight') or '1 kg'
            qty = int(it.get('quantity') or 1)
            price = float(it.get('price') or 0)
            item_total = price * qty
            subtotal += item_total

            items_rows_html.append(f"""
            <tr>
              <td style="padding: 10px 12px; border-bottom: 1px solid #331518; color: #ffffff; font-weight: 600;">{name} <span style="color: #f43f5e; font-size: 11px;">({weight})</span></td>
              <td style="padding: 10px 12px; border-bottom: 1px solid #331518; text-align: center; color: #d1d5db;">x {qty}</td>
              <td style="padding: 10px 12px; border-bottom: 1px solid #331518; text-align: right; color: #ffffff; font-weight: bold;">₹{item_total:.1f}</td>
            </tr>
            """)
            items_rows_text.append(f"  • {name} ({weight}) x {qty} = ₹{item_total:.1f}")

        delivery_charge = 0.0 if subtotal >= 499 or len(items) == 0 else 49.0
        total_amount = subtotal + delivery_charge

        date_code = datetime.utcnow().strftime('%Y%m%d')
        rand_code = f"{random.randint(100000, 999999):X}"
        order_number = f"FMM-{date_code}-{rand_code}"

        subject = f"🥩 [NEW ORDER #{order_number}] KBK MEAT SHOP - ₹{total_amount:.0f} ({payment_method})"

        text_content = f"""
=====================================================
          KBK MEAT SHOP - ORDER NOTIFICATION
=====================================================

Order ID:           {order_number}
Customer Name:      {recipient_name}
Mobile Number:      +{phone}
Delivery Schedule:  {delivery_day}
Delivery Address:   {address_line}, {city} - {pincode}

-----------------------------------------------------
ORDERED ITEMS:
{"\n".join(items_rows_text) if items_rows_text else "  • Fresh Meat Selection"}
-----------------------------------------------------

Subtotal:           ₹{subtotal:.1f}
Delivery Fee:       {'FREE' if delivery_charge == 0 else f'₹{delivery_charge:.1f}'}
Grand Total:        ₹{total_amount:.1f}
Payment Method:     {payment_method}

Hygiene Promise: 100% Halal, Farm Slaughtered & Delivered Fresh on Weekend Morning.
Store Helpline / WhatsApp: +91 98427 29718
=====================================================
"""

        items_table_html = "".join(items_rows_html) if items_rows_html else "<tr><td colspan='3'>Fresh Meat Selection</td></tr>"

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>New Order #{order_number}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #080203; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #f3f4f6;">
  <table width="100%" cellspacing="0" cellpadding="0" style="background-color: #080203; padding: 30px 15px;">
    <tr>
      <td align="center">
        <table width="600" cellspacing="0" cellpadding="0" style="background-color: #170508; border-radius: 20px; overflow: hidden; border: 1px solid #4a151b; box-shadow: 0 20px 40px rgba(0,0,0,0.8);">
          <tr>
            <td style="padding: 30px 30px 20px; text-align: center; background: linear-gradient(180deg, #2b080e 0%, #170508 100%); border-bottom: 1px solid #331518;">
              <h1 style="margin: 0; font-size: 26px; font-weight: 900; color: #fb7185; letter-spacing: 1px;">🥩 KBK MEAT SHOP</h1>
              <p style="margin: 5px 0 0; font-size: 13px; color: #e5e7eb; letter-spacing: 0.5px;">Weekend Farm-Harvested Fresh Meat Market</p>
            </td>
          </tr>
          <tr>
            <td style="padding: 25px 30px 15px;">
              <div style="background-color: #1f070b; border: 1px solid #5c1822; border-radius: 14px; padding: 18px; margin-bottom: 20px;">
                <table width="100%" style="font-size: 13px;">
                  <tr>
                    <td style="color: #9ca3af; padding: 4px 0;">Order Number:</td>
                    <td align="right" style="color: #ffffff; font-weight: bold; font-family: monospace; font-size: 15px;">{order_number}</td>
                  </tr>
                  <tr>
                    <td style="color: #9ca3af; padding: 4px 0;">Customer Name:</td>
                    <td align="right" style="color: #ffffff; font-weight: 600;">{recipient_name}</td>
                  </tr>
                  <tr>
                    <td style="color: #9ca3af; padding: 4px 0;">Contact Phone:</td>
                    <td align="right" style="color: #fb7185; font-weight: bold; font-family: monospace;">+{phone}</td>
                  </tr>
                  <tr>
                    <td style="color: #9ca3af; padding: 4px 0;">Delivery Schedule:</td>
                    <td align="right" style="color: #10b981; font-weight: bold;">{delivery_day}</td>
                  </tr>
                  <tr>
                    <td style="color: #9ca3af; padding: 4px 0;">Delivery Address:</td>
                    <td align="right" style="color: #ffffff;">{address_line}, {city} - {pincode}</td>
                  </tr>
                </table>
              </div>

              <h3 style="margin: 0 0 10px; font-size: 14px; text-transform: uppercase; color: #d1d5db;">Ordered Meat Items</h3>
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

              <table width="100%" style="font-size: 13px; color: #9ca3af; margin-top: 15px;">
                <tr>
                  <td style="padding: 4px 0;">Subtotal</td>
                  <td align="right" style="color: #ffffff; font-weight: 600;">₹{subtotal:.1f}</td>
                </tr>
                <tr>
                  <td style="padding: 4px 0;">Delivery Fee</td>
                  <td align="right" style="color: #10b981; font-weight: 600;">{'FREE' if delivery_charge == 0 else f'₹{delivery_charge:.1f}'}</td>
                </tr>
                <tr>
                  <td style="padding: 10px 0 0; font-size: 15px; font-weight: 800; color: #ffffff; border-top: 1px solid #331518;">Total Payable ({payment_method})</td>
                  <td align="right" style="padding: 10px 0 0; font-size: 20px; font-weight: 900; color: #fb7185; border-top: 1px solid #331518;">₹{total_amount:.1f}</td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="padding: 20px 30px; background-color: #120406; border-top: 1px solid #331518; text-align: center;">
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

        # Dispatch live email to Store Owner (kbkmeatshop@gmail.com)
        email_sent = send_smtp_email(ADMIN_EMAIL, subject, text_content, html_content)

        # Also dispatch to customer if email is valid and different
        if customer_email and '@' in customer_email and customer_email != ADMIN_EMAIL:
            send_smtp_email(customer_email, f"Order Confirmed #{order_number} - KBK MEAT SHOP", text_content, html_content)

        response_data = {
            'success': True,
            'message': 'Order placed successfully. Email dispatched to store owner.',
            'email_sent': email_sent,
            'order': {
                'id': random.randint(100, 9999),
                'order_number': order_number,
                'total_amount': total_amount,
                'subtotal': subtotal,
                'delivery_charge': delivery_charge,
                'discount_amount': 0.0,
                'order_status': 'Confirmed',
                'payment_status': 'Paid' if payment_method == 'UPI' else 'Pending',
                'payment_method': payment_method,
                'customer_name': recipient_name,
                'customer_phone': phone,
                'customer_email': customer_email or ADMIN_EMAIL,
                'customer_address': f"{address_line}, {city} - {pincode}",
                'items': items,
                'items_count': len(items),
                'created_at': datetime.utcnow().isoformat()
            }
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
