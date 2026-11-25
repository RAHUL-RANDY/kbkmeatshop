import React, { useState } from 'react';
import { X, MapPin, CheckCircle2, AlertCircle, ArrowRight, Clock, Truck } from 'lucide-react';
import { translations } from '../utils/translations';

const ALLOWED_CHIDAMBARAM_PINCODES = ['608001', '608002', '608102', '608601'];

const POPULAR_AREAS = [
  { name: 'Chidambaram Town', pincode: '608001' },
  { name: 'Annamalainagar', pincode: '608002' },
  { name: 'Killai / C. Mutlur', pincode: '608102' },
  { name: 'Bhuvanagiri', pincode: '608601' }
];

export default function PincodeCheckerModal({ isOpen, onClose, onPincodeSelected, lang = 'en' }) {
  const t = translations[lang] || translations.en;
  const [pincode, setPincode] = useState(() => {
    const saved = localStorage.getItem('kbk_delivery_pincode') || '';
    return ALLOWED_CHIDAMBARAM_PINCODES.includes(saved) ? saved : '';
  });
  const [checkResult, setCheckResult] = useState(null);

  if (!isOpen) return null;

  const handleCheck = (codeToCheck) => {
    const clean = (codeToCheck || pincode).replace(/\D/g, '');
    if (clean.length !== 6) {
      setCheckResult({
        status: 'error',
        message: lang === 'ta' ? 'தயவுசெய்து சரியான 6-இலக்க பின்கோடை உள்ளிடவும்.' : 'Please enter a valid 6-digit PIN code.'
      });
      return;
    }

    // Chidambaram & 10 km surrounding pincodes
    if (ALLOWED_CHIDAMBARAM_PINCODES.includes(clean)) {
      localStorage.setItem('kbk_delivery_pincode', clean);
      setCheckResult({
        status: 'success',
        pincode: clean,
        message: t.deliveryAvailable,
        desc: t.deliveryAvailableDesc
      });
      if (onPincodeSelected) {
        onPincodeSelected(clean);
      }
    } else {
      setCheckResult({
        status: 'outside',
        pincode: clean,
        message: t.deliveryOutside,
        desc: t.deliveryOutsideDesc
      });
    }
  };

  const handleSelectArea = (code) => {
    setPincode(code);
    handleCheck(code);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-3 sm:p-4 animate-in fade-in duration-200">
      {/* Backdrop */}
      <div 
        onClick={onClose}
        className="fixed inset-0 bg-black/85 backdrop-blur-md transition-opacity"
      />

      {/* Glass Modal Box */}
      <div className="relative w-full max-w-md rounded-3xl glass-panel border border-rose-500/30 p-5 sm:p-7 shadow-2xl z-10 text-center">
        
        <button
          onClick={onClose}
          className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-gray-300 hover:text-white transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Icon & Heading */}
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-rose-600/30 to-red-900/40 border border-rose-500/40 flex items-center justify-center mx-auto mb-3 shadow-inner">
          <MapPin className="w-7 h-7 text-rose-400" />
        </div>

        <h3 className="text-lg sm:text-xl font-black text-white font-heading">
          {t.checkDeliveryTitle}
        </h3>
        
        <p className="text-xs text-gray-300 mt-1 max-w-xs mx-auto">
          {t.enterPincodePrompt}
        </p>

        {/* Input Form */}
        <form onSubmit={(e) => { e.preventDefault(); handleCheck(); }} className="mt-4 flex gap-2">
          <div className="relative flex-1">
            <span className="absolute left-3.5 top-2.5 text-gray-400 text-xs font-mono font-bold">PIN</span>
            <input
              type="text"
              maxLength={6}
              value={pincode}
              onChange={(e) => {
                setPincode(e.target.value.replace(/\D/g, ''));
                if (checkResult) setCheckResult(null);
              }}
              placeholder="e.g. 608001"
              className="w-full pl-12 pr-3 py-2.5 rounded-xl glass-input text-sm font-mono font-bold text-white focus:ring-2 focus:ring-rose-500/50"
              autoFocus
            />
          </div>
          <button
            type="submit"
            className="btn-crimson px-4 py-2.5 rounded-xl text-xs font-bold text-white shrink-0 shadow-lg shadow-rose-950 flex items-center gap-1 cursor-pointer"
          >
            <span>{t.checkAvailabilityBtn}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </form>

        {/* Result Message */}
        {checkResult && (
          <div className={`mt-4 p-3.5 rounded-2xl text-left text-xs border animate-in zoom-in-95 duration-200 ${
            checkResult.status === 'success'
              ? 'bg-emerald-950/60 border-emerald-500/40 text-emerald-200'
              : checkResult.status === 'outside'
              ? 'bg-amber-950/60 border-amber-500/40 text-amber-200'
              : 'bg-red-950/60 border-red-500/40 text-red-200'
          }`}>
            <div className="flex items-start gap-2.5">
              {checkResult.status === 'success' ? (
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              ) : checkResult.status === 'outside' ? (
                <AlertCircle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
              ) : (
                <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
              )}
              <div>
                <strong className="block text-sm font-bold text-white mb-0.5">
                  {checkResult.message}
                </strong>
                <p className="text-[11px] opacity-90 leading-relaxed">
                  {checkResult.desc || checkResult.message}
                </p>

                {checkResult.status === 'success' && (
                  <div className="mt-2 pt-2 border-t border-emerald-500/20 flex items-center gap-3 text-[10px] text-emerald-300 font-semibold">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3 text-emerald-400" />
                      Sat & Sun: 6:00 AM - 10:00 AM
                    </span>
                    <span className="flex items-center gap-1">
                      <Truck className="w-3 h-3 text-emerald-400" />
                      Free Delivery &gt; ₹499
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Quick Popular Area Chips */}
        <div className="mt-5 pt-4 border-t border-white/10 text-left">
          <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-2">
            {lang === 'ta' ? 'சிதம்பரம் 10 கி.மீ டெலிவரி பகுதிகள்:' : 'Chidambaram 10 km Service Areas:'}
          </span>
          <div className="flex flex-wrap gap-1.5">
            {POPULAR_AREAS.map((area) => (
              <button
                key={area.pincode}
                type="button"
                onClick={() => handleSelectArea(area.pincode)}
                className="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-rose-900/40 border border-white/10 hover:border-rose-500/40 text-[11px] text-gray-300 hover:text-white transition-all cursor-pointer flex items-center gap-1"
              >
                <span>{area.name}</span>
                <span className="text-[9px] font-mono opacity-60">({area.pincode})</span>
              </button>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
