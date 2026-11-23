import React, { useState, useEffect } from 'react';
import { X, Package, Clock, CheckCircle2, AlertCircle, RefreshCw, XCircle } from 'lucide-react';
import api from '../services/api';

export default function OrderHistoryModal({ isOpen, onClose, onShowToast }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchOrders = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getOrders();
      setOrders(res.orders || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch your orders.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchOrders();
    }
  }, [isOpen]);

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm('Are you sure you want to cancel this order?')) return;
    try {
      await api.cancelOrder(orderId);
      onShowToast(`Order #${orderId} was cancelled.`);
      fetchOrders();
    } catch (err) {
      onShowToast(err.message || 'Could not cancel order.');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-3 sm:p-6">
      <div 
        onClick={onClose}
        className="fixed inset-0 bg-black/85 backdrop-blur-md transition-opacity"
      />

      <div className="relative w-full max-w-2xl rounded-3xl glass-panel border border-white/20 p-5 sm:p-8 shadow-2xl z-10 max-h-[85vh] flex flex-col justify-between overflow-hidden animate-in fade-in zoom-in-95">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-white/10 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-rose-600/30 border border-rose-500/40 flex items-center justify-center text-rose-300">
              <Package className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-xl font-black text-white font-heading">
                My Orders & History
              </h3>
              <p className="text-xs text-gray-400">
                Live delivery status and receipt history.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={fetchOrders}
              className="p-2 rounded-full bg-white/10 hover:bg-white/20 text-gray-300 hover:text-white transition-all"
              title="Refresh"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={onClose}
              className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-gray-300 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto space-y-4 my-4 pr-1">
          {error && (
            <div className="p-3 rounded-xl bg-red-950/80 border border-red-500/40 text-red-200 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-red-400" />
              <span>{error}</span>
            </div>
          )}

          {orders.length === 0 ? (
            <div className="text-center py-12 text-gray-400 text-xs space-y-2">
              <Package className="w-10 h-10 text-gray-500 mx-auto opacity-50" />
              <p>You haven't placed any orders yet.</p>
            </div>
          ) : (
            orders.map((o) => (
              <div key={o.id} className="p-4 rounded-2xl glass-card border border-white/15 space-y-3">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="font-mono text-xs font-bold text-white block">
                      {o.order_number}
                    </span>
                    <span className="text-[10px] text-gray-400">
                      {new Date(o.created_at).toLocaleDateString()} at {new Date(o.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-sm font-black text-rose-300 font-heading">
                      ₹{o.total_amount}
                    </span>
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                      o.order_status === 'Delivered' 
                        ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/30'
                        : o.order_status === 'Cancelled'
                        ? 'bg-red-950 text-red-400 border border-red-500/30'
                        : 'bg-rose-950 text-rose-300 border border-rose-500/30'
                    }`}>
                      {o.order_status}
                    </span>
                  </div>
                </div>

                {/* Items */}
                <div className="p-2.5 rounded-xl bg-black/40 border border-white/10 space-y-1 text-xs">
                  {o.items.map((it, idx) => (
                    <div key={idx} className="flex justify-between text-gray-300">
                      <span>{it.quantity}x {it.product_name} ({it.selected_weight})</span>
                      <span className="font-semibold text-white">₹{it.total_price}</span>
                    </div>
                  ))}
                </div>

                <div className="flex items-center justify-between pt-1 text-[11px] text-gray-400">
                  <span>Payment: <strong className="text-gray-200">{o.payment_method}</strong> ({o.payment_status})</span>
                  {['Pending', 'Confirmed'].includes(o.order_status) && (
                    <button
                      onClick={() => handleCancelOrder(o.id)}
                      className="text-red-400 hover:text-red-300 font-semibold underline text-xs"
                    >
                      Cancel Order
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

      </div>
    </div>
  );
}
