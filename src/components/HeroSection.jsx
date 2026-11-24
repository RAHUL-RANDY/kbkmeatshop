import React from 'react';
import { Star, Users, ArrowRight, LayoutGrid, ShieldCheck, Award, Sparkles, CalendarCheck } from 'lucide-react';
import { translations } from '../utils/translations';

export default function HeroSection({ onShopNow, onExplore, lang = 'en' }) {
  const t = translations[lang] || translations.en;
  return (
    <section id="hero" className="relative min-h-[92vh] lg:min-h-screen pt-28 sm:pt-32 pb-16 flex items-center justify-center overflow-hidden">
      {/* Cinematic Background Image Layer */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {/* Exact photo background with floating leaves, rustic wood & dramatic red spotlight */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-95 filter brightness-95 contrast-115 scale-[1.02]"
          style={{ backgroundImage: `url('/images/bg-cinematic-red.jpg')` }}
        />

        {/* Delicate vignette to blend edges smoothly without hiding the artwork */}
        <div className="absolute inset-0 bg-gradient-to-t from-[#0e0405] via-transparent to-[#0e0405]/40" />
        <div className="absolute inset-0 bg-gradient-to-r from-[#0e0405]/55 via-transparent to-[#0e0405]/35" />

        {/* Subtle crimson accent glow */}
        <div className="absolute top-1/4 right-1/3 w-[450px] h-[450px] bg-rose-600/20 rounded-full blur-[90px] animate-pulse-glow" />
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-10 w-full relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-6 items-center">
          
          {/* Left Hero Content: 6 Columns */}
          <div className="lg:col-span-6 flex flex-col items-start text-left space-y-6 pt-4 lg:pt-0">
            
            {/* Top Weekend Pre-Booking Badge & Brand Logo */}
            <div className="flex flex-wrap items-center gap-2.5">
              <div className="h-9 w-14 rounded-lg bg-white p-1 border border-white/50 shadow-md flex items-center justify-center overflow-hidden">
                <img
                  src="/images/kbk-logo.jpg"
                  alt="KBK MEATE SHOP Logo"
                  className="w-full h-full object-contain"
                />
              </div>
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full glass-badge text-xs font-semibold tracking-wide text-rose-200 border border-rose-500/30 shadow-lg shadow-rose-950/50">
                <CalendarCheck className="w-3.5 h-3.5 text-rose-400" />
                <span>Pre-Book All Week • Delivered Fresh Every Sat & Sun</span>
              </div>
            </div>

            {/* Oversized Cinematic Typography matching reference image */}
            <div className="space-y-1">
              <h1 className="text-4xl sm:text-6xl xl:text-7xl font-extrabold italic uppercase tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-white via-rose-100 to-rose-300 font-display drop-shadow-[0_4px_20px_rgba(225,29,72,0.4)]">
                KBK MEAT
              </h1>
              <h2 className="text-5xl sm:text-7xl xl:text-8xl font-black uppercase tracking-tight text-white font-display hero-glow-title">
                SHOP
              </h2>
            </div>

            {/* Subtitle explaining the business model */}
            <p className="text-gray-300 text-sm sm:text-base md:text-lg font-medium max-w-lg leading-relaxed">
              {t.heroDesc}
            </p>

            {/* Live Weekend Booking Status Pill */}
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span>{lang === 'ta' ? 'வரும் சனி & ஞாயிறு டெலிவரிக்கான முன்பதிவு நடைபெறுகிறது' : 'Pre-Booking is Open for Upcoming Saturday & Sunday'}</span>
            </div>

            {/* Ratings & Social Proof Stats */}
            <div className="flex flex-wrap items-center gap-6 sm:gap-8 pt-2">
              {/* Rating */}
              <div className="flex items-center gap-3">
                <span className="text-2xl sm:text-3xl font-bold text-white font-heading">
                  4.9
                </span>
                <div>
                  <div className="flex items-center gap-0.5 text-amber-400">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className="w-3.5 h-3.5 fill-current" />
                    ))}
                  </div>
                  <span className="text-[11px] text-gray-400 font-medium">
                    Customer Rating
                  </span>
                </div>
              </div>

              {/* Divider */}
              <div className="h-8 w-[1px] bg-white/15 hidden sm:block" />

              {/* Happy Customers */}
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-full glass-panel flex items-center justify-center text-rose-300">
                  <Users className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-base sm:text-lg font-bold text-white font-heading">
                    5K+
                  </div>
                  <span className="text-[11px] text-gray-400 font-medium">
                    Happy Customers
                  </span>
                </div>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <button
                onClick={onShopNow}
                className="btn-crimson px-7 py-3 rounded-full text-xs sm:text-sm font-bold text-white flex items-center gap-2.5 group cursor-pointer"
              >
                <span>{t.preBookNowBtn}</span>
                <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
              </button>

              <button
                onClick={onExplore}
                className="btn-glass px-6 py-3 rounded-full text-xs sm:text-sm font-semibold text-gray-200 hover:text-white flex items-center gap-2 group cursor-pointer"
              >
                <LayoutGrid className="w-4 h-4 text-rose-300 transition-transform group-hover:rotate-45" />
                <span>{t.exploreMenuBtn}</span>
              </button>
            </div>

          </div>

          {/* Right Hero Visual: 6 Columns */}
          <div className="lg:col-span-6 relative flex items-center justify-center mt-4 lg:mt-0">
            
            {/* Ambient Radial Spotlight behind Steak */}
            <div className="absolute inset-0 bg-radial from-rose-600/35 via-rose-900/10 to-transparent blur-3xl transform scale-110 pointer-events-none" />

            {/* Floating Glass Badge 1: Quality Verified */}
            <div className="absolute -top-3 left-4 sm:left-10 z-20 glass-badge px-4 py-2 rounded-2xl flex items-center gap-2.5 shadow-2xl animate-float-slow border border-white/25">
              <div className="w-7 h-7 rounded-lg bg-rose-600/40 flex items-center justify-center text-rose-200">
                <ShieldCheck className="w-4 h-4" />
              </div>
              <div className="flex flex-col text-left">
                <span className="text-[10px] text-gray-300 font-medium">Certified 100%</span>
                <span className="text-xs font-bold text-white tracking-wide">Quality Verified</span>
              </div>
            </div>

            {/* Floating Glass Badge 2: Freshness Guaranteed */}
            <div className="absolute top-8 right-2 sm:right-6 z-20 glass-badge px-4 py-2.5 rounded-2xl flex items-center gap-2.5 shadow-2xl animate-float-reverse border border-white/25">
              <div className="w-7 h-7 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                <Award className="w-4 h-4" />
              </div>
              <div className="flex flex-col text-left">
                <span className="text-[10px] text-emerald-400 font-semibold tracking-wider uppercase">0-4°C Cold</span>
                <span className="text-xs font-bold text-white tracking-wide">Freshness Guaranteed</span>
              </div>
            </div>

            {/* Main Ribeye Steak & Cleaver Photo with glowing frame */}
            <div className="relative group w-full max-w-lg lg:max-w-xl">
              {/* Outer soft glow ring */}
              <div className="absolute -inset-1.5 rounded-3xl bg-gradient-to-r from-rose-600/30 via-red-500/20 to-rose-700/30 blur-lg opacity-70 group-hover:opacity-100 transition duration-500" />
              
              <div className="relative rounded-3xl overflow-hidden glass-panel border border-white/20 p-2 shadow-2xl">
                <img
                  src="/images/hero-steak.jpg"
                  alt="Cinematic marbled steak on rustic cutting board with butcher cleaver"
                  className="w-full h-auto object-cover rounded-2xl transform transition-transform duration-700 group-hover:scale-[1.03]"
                />
              </div>

              {/* Bottom Subtle Reflection shadow */}
              <div className="w-3/4 h-6 bg-black/60 mx-auto rounded-full blur-xl -mt-3" />
            </div>

          </div>

        </div>
      </div>
    </section>
  );
}
