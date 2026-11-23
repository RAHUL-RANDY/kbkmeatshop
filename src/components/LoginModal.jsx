import React, { useState } from 'react';
import { X, Lock, Mail, User, ShieldCheck, ArrowRight, Phone, AlertCircle } from 'lucide-react';
import api from '../services/api';

export default function LoginModal({ isOpen, onClose, onLoginSuccess }) {
  const [tab, setTab] = useState('signin'); // 'signin' or 'signup'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (tab === 'signin') {
        const res = await api.login(email, password);
        onLoginSuccess(res.user);
        onClose();
      } else {
        if (password !== confirmPassword) {
          setError('Passwords do not match.');
          setLoading(false);
          return;
        }
        const res = await api.register({
          full_name: name,
          email,
          phone,
          password,
          confirm_password: confirmPassword
        });
        onLoginSuccess(res.user);
        onClose();
      }
    } catch (err) {
      setError(err.message || 'Authentication failed. Please verify your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async (role = 'customer') => {
    setError(null);
    setLoading(true);
    try {
      const demoEmail = role === 'admin' ? 'admin@freshmeatmarket.com' : 'rahul@example.com';
      const demoPass = role === 'admin' ? 'Admin@123456' : 'Customer@123';
      const res = await api.login(demoEmail, demoPass);
      onLoginSuccess(res.user);
      onClose();
    } catch (err) {
      // Offline fallback
      const fallbackUser = role === 'admin' 
        ? { id: 1, full_name: 'Market Administrator', email: 'admin@freshmeatmarket.com', role: 'admin' }
        : { id: 2, full_name: 'Rahul Sharma', email: 'rahul@example.com', role: 'customer' };
      api.setUser(fallbackUser);
      onLoginSuccess(fallbackUser);
      onClose();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        onClick={onClose}
        className="fixed inset-0 bg-black/75 backdrop-blur-md transition-opacity"
      />

      {/* Glass Modal Box */}
      <div className="relative w-full max-w-md rounded-3xl glass-panel border border-white/20 p-6 sm:p-8 shadow-2xl z-10 animate-in fade-in zoom-in-95 duration-200">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-gray-300 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Modal Header */}
        <div className="text-center mb-6">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-rose-500/20 to-red-900/40 border border-rose-500/30 flex items-center justify-center mx-auto mb-3 shadow-inner">
            <Lock className="w-5 h-5 text-rose-300" />
          </div>
          <h3 className="text-xl sm:text-2xl font-black text-white font-heading">
            {tab === 'signin' ? 'Welcome Back' : 'Create an Account'}
          </h3>
          <p className="text-xs text-gray-400 mt-1">
            Access your saved cart, addresses, and track your weekend meat deliveries.
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-950/80 border border-red-500/40 text-red-200 text-xs flex items-center gap-2 animate-in fade-in">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-400" />
            <span>{error}</span>
          </div>
        )}

        {/* Tab Switcher */}
        <div className="grid grid-cols-2 p-1 rounded-xl bg-black/40 border border-white/10 mb-6">
          <button
            onClick={() => { setTab('signin'); setError(null); }}
            className={`py-2 text-xs font-semibold rounded-lg transition-all ${
              tab === 'signin'
                ? 'btn-crimson text-white shadow'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Sign In
          </button>
          <button
            onClick={() => { setTab('signup'); setError(null); }}
            className={`py-2 text-xs font-semibold rounded-lg transition-all ${
              tab === 'signup'
                ? 'btn-crimson text-white shadow'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Register
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-3.5">
          {tab === 'signup' && (
            <>
              <div>
                <label className="block text-xs font-medium text-gray-300 mb-1">
                  Full Name
                </label>
                <div className="relative">
                  <User className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Rahul Sharma"
                    className="w-full pl-10 pr-4 py-2 rounded-xl text-xs glass-input"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-300 mb-1">
                  Mobile Number (Optional)
                </label>
                <div className="relative">
                  <Phone className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
                  <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="9876543210"
                    className="w-full pl-10 pr-4 py-2 rounded-xl text-xs glass-input"
                  />
                </div>
              </div>
            </>
          )}

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full pl-10 pr-4 py-2 rounded-xl text-xs glass-input"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2 rounded-xl text-xs glass-input"
              />
            </div>
          </div>

          {tab === 'signup' && (
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">
                Confirm Password
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
                <input
                  type="password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-4 py-2 rounded-xl text-xs glass-input"
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-crimson py-2.5 rounded-xl text-xs sm:text-sm font-bold text-white flex items-center justify-center gap-2 shadow-lg shadow-rose-950 mt-2"
          >
            {loading ? (
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <span>{tab === 'signin' ? 'Sign In' : 'Create Account'}</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* 1-Click Demo Login Shortcuts */}
        <div className="mt-4 pt-4 border-t border-white/10 space-y-2">
          <button
            type="button"
            onClick={() => handleDemoLogin('customer')}
            className="w-full py-2 px-3 rounded-xl btn-glass text-xs font-semibold text-rose-200 hover:text-white flex items-center justify-center gap-2 border-rose-500/30"
          >
            <ShieldCheck className="w-4 h-4 text-rose-400" />
            <span>1-Click Demo Customer Login</span>
          </button>

          <button
            type="button"
            onClick={() => handleDemoLogin('admin')}
            className="w-full py-2 px-3 rounded-xl bg-white/5 hover:bg-white/10 text-xs font-semibold text-gray-300 hover:text-white flex items-center justify-center gap-2 border border-white/10"
          >
            <span>Login as Administrator</span>
          </button>
        </div>

      </div>
    </div>
  );
}
