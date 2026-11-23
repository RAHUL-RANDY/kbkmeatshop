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
  Phone
} from 'lucide-react';

export default function OrderSuccessModal({ orderData, onClose }) {
  const [copiedId, setCopiedId] = useState(false);

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
        <div className="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/20 text-left flex items-center gap-3 text-xs mb-5">
          <ShieldCheck className="w-5 h-5 text-emerald-400 shrink-0" />
          <div className="text-[11px] text-gray-300">
            <strong className="text-white">KBK Quality Assurance:</strong> 100% Halal Certified, Farm Slaughtered & Delivered Fresh on Weekend Morning.
          </div>
        </div>

        {/* Action Button: Continue Shopping */}
        <button
          onClick={onClose}
          className="w-full py-3 px-6 rounded-full btn-crimson text-white font-bold text-xs sm:text-sm flex items-center justify-center gap-2 shadow-lg shadow-rose-950/60 cursor-pointer"
        >
          <ShoppingBag className="w-4 h-4" />
          <span>Continue Shopping</span>
          <ArrowRight className="w-4 h-4" />
        </button>

      </div>
    </div>
  );
}
