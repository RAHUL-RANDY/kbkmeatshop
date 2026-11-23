import React, { useState, useEffect } from 'react';
import { Timer, Tag, Copy, Check, Sparkles, ArrowRight } from 'lucide-react';

export default function SpecialOfferBanner({ onShopOffer }) {
  const [timeLeft, setTimeLeft] = useState({ hours: 8, minutes: 42, seconds: 15 });
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev.seconds > 0) {
          return { ...prev, seconds: prev.seconds - 1 };
        } else if (prev.minutes > 0) {
          return { ...prev, minutes: 59, seconds: 59 };
        } else if (prev.hours > 0) {
          return { ...prev, hours: prev.hours - 1, minutes: 59, seconds: 59 };
        }
        return { hours: 12, minutes: 0, seconds: 0 };
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleCopy = () => {
    navigator.clipboard.writeText('PRIME30');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="py-8 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-10">
        <div className="relative rounded-3xl overflow-hidden glass-panel border border-rose-500/30 p-6 sm:p-10 shadow-2xl">
          
          {/* Ambient Red Glow in background */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-radial from-rose-600/30 via-red-900/10 to-transparent blur-3xl pointer-events-none" />

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
            
            {/* Left Content */}
            <div className="lg:col-span-7 space-y-4 text-left">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/20 border border-rose-400/30 text-rose-300 text-xs font-semibold">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Weekend Culinary Special</span>
              </div>

              <h3 className="text-2xl sm:text-4xl font-extrabold text-white font-heading leading-tight">
                Gourmet Mutton & Chicken Feast Pack
              </h3>

              <p className="text-gray-300 text-xs sm:text-sm max-w-xl leading-relaxed">
                Get 1kg Fresh Mutton Curry Cut + 1kg Country Chicken + 1 Pack of Farm Fresh Eggs bundled at an exclusive 30% discount. Hand-selected for weekend banquets.
              </p>

              {/* Countdown Timer Boxes */}
              <div className="flex items-center gap-3 pt-2">
                <div className="flex items-center gap-1.5 text-xs text-rose-300 font-semibold mr-1">
                  <Timer className="w-4 h-4 animate-pulse" />
                  <span>Ends In:</span>
                </div>

                <div className="flex items-center gap-2">
                  <div className="w-12 h-12 rounded-xl glass-badge flex flex-col items-center justify-center border border-white/20">
                    <span className="text-sm sm:text-base font-extrabold text-white font-heading">
                      {String(timeLeft.hours).padStart(2, '0')}
                    </span>
                    <span className="text-[9px] text-gray-400 uppercase">Hours</span>
                  </div>

                  <span className="text-white font-bold">:</span>

                  <div className="w-12 h-12 rounded-xl glass-badge flex flex-col items-center justify-center border border-white/20">
                    <span className="text-sm sm:text-base font-extrabold text-white font-heading">
                      {String(timeLeft.minutes).padStart(2, '0')}
                    </span>
                    <span className="text-[9px] text-gray-400 uppercase">Mins</span>
                  </div>

                  <span className="text-white font-bold">:</span>

                  <div className="w-12 h-12 rounded-xl glass-badge flex flex-col items-center justify-center border border-white/20">
                    <span className="text-sm sm:text-base font-extrabold text-rose-400 font-heading">
                      {String(timeLeft.seconds).padStart(2, '0')}
                    </span>
                    <span className="text-[9px] text-gray-400 uppercase">Secs</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Action & Coupon Box */}
            <div className="lg:col-span-5 flex flex-col sm:flex-row lg:flex-col items-start sm:items-center lg:items-end gap-4">
              <div className="w-full sm:w-auto p-4 rounded-2xl glass-card border border-white/20 flex flex-col items-start gap-2">
                <div className="flex items-center justify-between w-full gap-4">
                  <div className="flex items-center gap-2 text-rose-300 text-xs font-semibold">
                    <Tag className="w-4 h-4" />
                    <span>Promo Coupon Code</span>
                  </div>
                  <span className="text-emerald-400 text-xs font-bold">30% OFF</span>
                </div>

                <div className="w-full flex items-center justify-between gap-2 p-2 rounded-xl bg-black/40 border border-white/10">
                  <code className="text-sm font-black tracking-widest text-white font-mono">
                    PRIME30
                  </code>
                  <button
                    onClick={handleCopy}
                    className="p-1.5 rounded-lg bg-rose-600/30 hover:bg-rose-600/50 text-rose-200 text-xs flex items-center gap-1 transition-all"
                  >
                    {copied ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-emerald-400" />
                        <span className="text-[10px] text-emerald-300">Copied</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5" />
                        <span className="text-[10px]">Copy</span>
                      </>
                    )}
                  </button>
                </div>
              </div>

              <button
                onClick={onShopOffer}
                className="w-full sm:w-auto btn-crimson px-7 py-3 rounded-full text-xs sm:text-sm font-bold text-white flex items-center justify-center gap-2 shadow-xl shadow-rose-950"
              >
                <span>Claim Offer Now</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>

          </div>

        </div>
      </div>
    </section>
  );
}
