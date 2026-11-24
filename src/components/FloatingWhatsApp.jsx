import React, { useState } from 'react';
import { MessageSquare, Sparkles, X } from 'lucide-react';
import { translations } from '../utils/translations';

export default function FloatingWhatsApp({ lang = 'en' }) {
  const [showTooltip, setShowTooltip] = useState(false);
  const t = translations[lang] || translations.en;

  const phone = '919842729718';
  const message = lang === 'ta'
    ? 'வணக்கம் KBK மீட் ஷாப்! எனக்கு வார இறுதி புதிய இறைச்சி முன்பதிவு / விசேஷ மொத்த ஆர்டர் பற்றி தகவல் தேவை.'
    : 'Hello KBK MEAT SHOP! I would like to enquire about fresh meat pre-booking / bulk party orders.';

  const waUrl = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;

  return (
    <aside 
      aria-label="WhatsApp Support and Bulk Orders"
      className="fixed bottom-6 right-6 z-40 flex items-center gap-3 select-none"
    >
      {/* Hover / Active Tooltip Card */}
      {showTooltip && (
        <div 
          role="tooltip"
          className="hidden sm:flex flex-col bg-black/90 backdrop-blur-xl border border-emerald-500/40 p-3 rounded-2xl shadow-2xl text-left animate-in slide-in-from-right-3 duration-200 max-w-xs"
        >
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="text-[10px] font-black uppercase tracking-wider text-emerald-400 flex items-center gap-1">
              <Sparkles className="w-3 h-3" />
              KBK Helpline
            </span>
            <button 
              onClick={(e) => { e.stopPropagation(); setShowTooltip(false); }}
              aria-label="Close WhatsApp tooltip"
              className="text-gray-400 hover:text-white"
            >
              <X className="w-3 h-3" />
            </button>
          </div>
          <p className="text-xs font-bold text-white leading-tight">
            {t.whatsappHelp} &amp; {t.bulkOrders}
          </p>
          <p className="text-[10px] text-gray-300 mt-1">
            +91 98427 29718 (Instant WhatsApp Support)
          </p>
        </div>
      )}

      {/* Pulsing Floating Action Button */}
      <a
        href={waUrl}
        target="_blank"
        rel="noopener noreferrer"
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        className="group relative flex items-center gap-2 px-3.5 py-3 rounded-full bg-gradient-to-r from-emerald-600 to-green-500 text-white shadow-xl shadow-emerald-950/80 hover:shadow-emerald-500/40 hover:scale-105 active:scale-95 transition-all duration-300 border border-emerald-300/40"
        title="WhatsApp Support & Bulk Orders"
      >
        {/* Glow Ring */}
        <span className="absolute -inset-1 rounded-full bg-emerald-500/30 blur-sm group-hover:bg-emerald-400/50 transition-all animate-pulse pointer-events-none" />

        {/* WhatsApp SVG Icon */}
        <svg 
          className="w-5 h-5 fill-current shrink-0 relative z-10" 
          viewBox="0 0 24 24"
        >
          <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.711 2.598 2.669-.699c.969.587 1.838.883 2.791.884 3.185 0 5.769-2.587 5.77-5.768.001-3.18-2.585-5.768-5.77-5.768zm0 10.36c-.846 0-1.637-.247-2.316-.677l-.166-.104-1.579.414.421-1.539-.115-.183c-.477-.759-.728-1.583-.728-2.497 0-2.529 2.059-4.588 4.59-4.588 2.531 0 4.59 2.059 4.59 4.588-.001 2.53-2.06 4.586-4.707 4.586zm7.969-4.594c0 4.418-3.582 8-8 8-1.408 0-2.733-.365-3.882-1.002l-4.118 1.078 1.097-4.015c-.718-1.21-1.097-2.602-1.097-4.061 0-4.418 3.582-8 8-8s8 3.582 8 8z"/>
        </svg>

        <span className="relative z-10 text-xs font-bold font-heading hidden sm:inline tracking-wide">
          {lang === 'ta' ? 'வாட்ஸ்அப் உதவி' : 'WhatsApp'}
        </span>
      </a>
    </aside>
  );
}
