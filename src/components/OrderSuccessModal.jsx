import React, { useState } from 'react';
import { 
  CheckCircle2, 
  ArrowRight, 
  X, 
  Copy, 
  Check, 
  ShieldCheck, 
  ShoppingBag,
  Calendar,
  Phone,
  Printer
} from 'lucide-react';
import { translations } from '../utils/translations';

export default function OrderSuccessModal({ orderData, onClose, lang = 'en' }) {
  const [copiedId, setCopiedId] = useState(false);
  const t = translations[lang] || translations.en;

  if (!orderData) return null;

  const rawCustomerPhone = orderData.phone || '';
  const cleanCustomerDigits = rawCustomerPhone.replace(/\D/g, '');
  const customerPhone = cleanCustomerDigits.length === 10 
    ? `+91 ${cleanCustomerDigits}` 
    : (cleanCustomerDigits || '9842729718');

  const customerName = orderData.customerName || 'Valued Customer';
  const orderId = orderData.orderId || 'FMM-000000';
  const grandTotal = orderData.grandTotal || 0;
  const address = orderData.address || 'Doorstep Delivery';
  const deliverySchedule = orderData.deliveryDay || 'Saturday / Sunday Morning (Fresh Cut)';

  const handleCopyOrderId = () => {
    navigator.clipboard.writeText(orderId);
    setCopiedId(true);
    setTimeout(() => setCopiedId(false), 2000);
  };

  const handlePrintReceipt = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    
    const itemsHtml = (orderData.items || []).map(item => `
      <tr>
        <td style="padding: 8px; border-bottom: 1px solid #ddd;">${item.name || item.product_name} (${item.selectedWeight || item.selected_weight || '1 kg'})</td>
        <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: center;">${item.quantity}</td>
        <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">₹${item.price || item.total_price || (item.unit_price * item.quantity)}</td>
      </tr>
    `).join('');

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>KBK Meat Shop - Receipt ${orderId}</title>
        <style>
          body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 25px; color: #222; max-width: 600px; margin: 0 auto; line-height: 1.5; }
          .header { text-align: center; border-bottom: 2px dashed #b91c1c; padding-bottom: 15px; margin-bottom: 15px; }
          .logo-text { font-size: 24px; font-weight: 900; color: #b91c1c; margin: 0; }
          .sub { font-size: 12px; color: #555; margin-top: 3px; }
          .info-table { width: 100%; font-size: 12px; margin-bottom: 15px; }
          .info-table td { padding: 4px 0; }
          .items-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 15px; }
          .items-table th { background: #f3f4f6; padding: 8px; text-align: left; border-bottom: 2px solid #ddd; font-size: 11px; text-transform: uppercase; }
          .total-box { font-size: 13px; font-weight: bold; text-align: right; margin-top: 10px; border-top: 2px solid #222; padding-top: 8px; }
          .footer-note { margin-top: 25px; text-align: center; font-size: 11px; color: #666; border-top: 1px solid #eee; padding-top: 12px; }
          @media print { button { display: none; } }
        </style>
      </head>
      <body>
        <div class="header">
          <h1 class="logo-text">🥩 KBK MEAT SHOP</h1>
          <div class="sub">Fresh Chicken &amp; Mutton • Farm-Harvested Weekend Meat Market</div>
          <div class="sub">Helpline: +91 98427 29718 | Email: kbkmeatshop@gmail.com</div>
        </div>

        <table class="info-table">
          <tr><td><strong>Order ID:</strong> ${orderId}</td><td style="text-align: right;"><strong>Date:</strong> ${new Date().toLocaleDateString()}</td></tr>
          <tr><td><strong>Customer:</strong> ${customerName}</td><td style="text-align: right;"><strong>Phone:</strong> ${customerPhone}</td></tr>
          <tr><td colspan="2"><strong>Delivery Address:</strong> ${address}</td></tr>
          <tr><td colspan="2"><strong>Delivery Timing:</strong> ${deliverySchedule}</td></tr>
          <tr><td colspan="2"><strong>Payment Method:</strong> ${orderData.paymentMethod || 'Cash on Delivery'}</td></tr>
        </table>

        <table class="items-table">
          <thead>
            <tr>
              <th>Item &amp; Weight</th>
              <th style="text-align: center;">Qty</th>
              <th style="text-align: right;">Amount</th>
            </tr>
          </thead>
          <tbody>
            ${itemsHtml}
          </tbody>
        </table>

        <div class="total-box">
          <div>Subtotal: ₹${orderData.subtotal || grandTotal}</div>
          ${orderData.deliveryFee ? `<div>Weekend Delivery Fee: ₹${orderData.deliveryFee}</div>` : '<div>Weekend Delivery: FREE</div>'}
          <div style="font-size: 18px; color: #b91c1c; margin-top: 5px;">Total Amount: ₹${grandTotal}</div>
        </div>

        <div class="footer-note">
          <p><strong>Quality Assurance:</strong> 100% Halal Slaughtered, Hand-Cleaned &amp; Chilled.</p>
          <p><strong>Privacy Policy:</strong> Customer contact details and order records will be permanently erased 2 days after delivery.</p>
          <p>Thank you for ordering with KBK MEAT SHOP! Helpline: +91 98427 29718</p>
        </div>
        <script>
          window.onload = function() { window.print(); }
        </script>
      </body>
      </html>
    `);
    printWindow.document.close();
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-3 sm:p-4 animate-in fade-in duration-200">
      {/* Backdrop */}
      <div 
        onClick={onClose}
        className="fixed inset-0 bg-black/85 backdrop-blur-md transition-opacity"
      />

      {/* Glass Card */}
      <div className="relative w-full max-w-lg rounded-3xl glass-panel border border-white/20 p-5 sm:p-8 shadow-2xl z-10 text-center max-h-[92vh] overflow-y-auto">
        
        <button
          onClick={onClose}
          className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-gray-300 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Confirmation Header */}
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-teal-500/30 border border-emerald-500/40 flex items-center justify-center mx-auto mb-3 shadow-lg shadow-emerald-950/50">
          <CheckCircle2 className="w-8 h-8 text-emerald-400" />
        </div>

        <span className="inline-block text-[10px] font-bold uppercase tracking-wider text-emerald-400 px-3 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
          Order Confirmed
        </span>

        <h3 className="text-xl sm:text-2xl font-black text-white font-heading mt-2">
          Thank You, {customerName}!
        </h3>

        <p className="text-xs text-gray-300 mt-1 max-w-sm mx-auto leading-relaxed">
          Your farm-fresh meat booking has been successfully placed. We will slaughter and prepare your order fresh on delivery morning.
        </p>

        {/* Order Summary Box */}
        <div className="my-5 p-4 rounded-2xl bg-black/50 border border-white/10 text-left space-y-2.5 text-xs">
          <div className="flex justify-between items-center pb-2 border-b border-white/10">
            <span className="text-gray-400">Order ID:</span>
            <div className="flex items-center gap-1.5">
              <span className="font-mono font-bold text-white tracking-wider">{orderId}</span>
              <button
                onClick={handleCopyOrderId}
                className="p-1 rounded bg-white/10 hover:bg-white/20 text-gray-300 hover:text-white cursor-pointer"
                title="Copy Order ID"
              >
                {copiedId ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
              </button>
            </div>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-gray-400">Customer Mobile:</span>
            <span className="font-semibold text-white font-mono">{customerPhone}</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-gray-400">Scheduled Delivery:</span>
            <span className="font-bold text-emerald-400 flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5" />
              <span>{deliverySchedule}</span>
            </span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-gray-400">Items Ordered:</span>
            <span className="font-semibold text-white">{(orderData.items || []).length} items</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-gray-400">Payment Mode:</span>
            <span className="font-bold text-amber-300">Cash on Delivery (COD)</span>
          </div>

          <div className="flex justify-between items-center">
            <span className="text-gray-400">Delivery Address:</span>
            <span className="text-gray-200 text-right truncate max-w-[220px]">{address}</span>
          </div>

          <div className="flex justify-between items-center pt-2.5 border-t border-white/10 text-sm font-extrabold text-white">
            <span>Amount to Collect on Delivery:</span>
            <span className="text-emerald-400 font-heading text-lg">₹{grandTotal}</span>
          </div>
        </div>

        {/* Quality Guarantee Box */}
        <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/20 text-left flex items-center gap-3 text-xs mb-4">
          <ShieldCheck className="w-5 h-5 text-emerald-400 shrink-0" />
          <div className="text-[11px] text-gray-300">
            <strong className="text-white">KBK Quality Assurance:</strong> 100% Halal Certified, Farm Slaughtered & Delivered Fresh on Weekend Morning.
          </div>
        </div>

        {/* Action Buttons: Print Bill / Receipt & Continue Shopping */}
        <div className="space-y-2.5">
          <button
            type="button"
            onClick={handlePrintReceipt}
            className="w-full py-2.5 px-4 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all cursor-pointer shadow-md"
          >
            <Printer className="w-4 h-4 text-emerald-400" />
            <span>{t.printReceipt}</span>
          </button>

          <button
            type="button"
            onClick={onClose}
            className="w-full py-3 px-6 rounded-full btn-crimson text-white font-bold text-xs sm:text-sm flex items-center justify-center gap-2 shadow-lg shadow-rose-950/60 cursor-pointer"
          >
            <ShoppingBag className="w-4 h-4" />
            <span>{t.continueShopping}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

      </div>
    </div>
  );
}
