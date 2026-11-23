import React from 'react';
import { Mail, Phone, MapPin, ShieldCheck, Heart } from 'lucide-react';

export default function Footer({ onSelectCategory, onOpenAdmin }) {
  return (
    <footer id="contact" className="relative z-20 pt-16 pb-12 mt-16 border-t border-white/10 bg-gradient-to-b from-[#180508]/80 to-[#0e0405]">
      {/* Main Footer Links */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-12">
          
          {/* Brand Col */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="h-12 sm:h-14 w-16 sm:w-20 rounded-xl bg-white p-1.5 border border-white/50 shadow-lg flex items-center justify-center overflow-hidden">
                <img
                  src="/images/kbk-logo.jpg"
                  alt="KBK MEATE SHOP Logo"
                  className="w-full h-full object-contain"
                />
              </div>
              <div>
                <span className="text-lg font-black tracking-tight text-white font-heading block">
                  KBK MEAT SHOP
                </span>
                <span className="text-xs text-rose-300/80 font-semibold -mt-1 block">
                  Fresh Chicken & Mutton Purveyors
                </span>
              </div>
            </div>

            <p className="text-xs text-gray-400 max-w-sm leading-relaxed">
              Delivering the freshest, premium artisanal meat cuts, fresh poultry, coastal seafood, and free-range table eggs straight from certified hygienic farms to your kitchen.
            </p>

            <div className="flex items-center gap-3 text-xs text-gray-400">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Certified Halal • 100% Antibiotic Residue Free</span>
            </div>
          </div>

          {/* Quick Categories */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-white font-heading">
              Market Categories
            </h4>
            <ul className="space-y-2 text-xs text-gray-400">
              <li>
                <button onClick={() => onSelectCategory('chicken')} className="hover:text-rose-300 transition-colors">
                  Country & Broiler Chicken
                </button>
              </li>
              <li>
                <button onClick={() => onSelectCategory('mutton')} className="hover:text-rose-300 transition-colors">
                  Prime Grass-Fed Mutton
                </button>
              </li>
              <li>
                <button onClick={() => onSelectCategory('fish')} className="hover:text-rose-300 transition-colors">
                  Daily Ocean Fish & Seafood
                </button>
              </li>
              <li>
                <button onClick={() => onSelectCategory('eggs')} className="hover:text-rose-300 transition-colors">
                  Organic Farm Fresh Eggs
                </button>
              </li>
              <li>
                <a href="#offers" className="hover:text-rose-300 transition-colors">
                  Chef Combo Packs
                </a>
              </li>
            </ul>
          </div>

          {/* Customer Care */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-white font-heading">
              Customer Support
            </h4>
            <ul className="space-y-2 text-xs text-gray-400">
              <li><a href="#about" className="hover:text-rose-300 transition-colors">Our Quality Charter</a></li>
              <li><a href="#about" className="hover:text-rose-300 transition-colors">Cold-Chain Logistics</a></li>
              <li><a href="#contact" className="hover:text-rose-300 transition-colors">Delivery Cities & Pincodes</a></li>
              <li><a href="#terms" className="hover:text-rose-300 transition-colors">Terms of Service</a></li>
              <li><a href="#privacy" className="hover:text-rose-300 transition-colors">Privacy Policy</a></li>
            </ul>
          </div>

          {/* Direct Contact */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-white font-heading">
              Direct Contact
            </h4>
            <div className="space-y-2 text-xs text-gray-400">
              <div className="flex items-center gap-2">
                <Phone className="w-3.5 h-3.5 text-rose-300 shrink-0" />
                <a href="tel:+919842729718" className="hover:text-white transition-colors">+91 98427 29718</a>
              </div>
              <div className="flex items-center gap-2">
                <Mail className="w-3.5 h-3.5 text-rose-300 shrink-0" />
                <a href="mailto:kbkmeatshop@gmail.com" className="hover:text-white transition-colors">kbkmeatshop@gmail.com</a>
              </div>
              <div className="flex items-start gap-2">
                <MapPin className="w-3.5 h-3.5 text-rose-300 shrink-0 mt-0.5" />
                <span>Central Processing Hub, Cold-Line Facility, City Center</span>
              </div>
            </div>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-gray-500">
          <div className="flex items-center gap-3">
            <p>© 2026 KBK MEAT SHOP. All Rights Reserved.</p>
            {onOpenAdmin && (
              <button
                onClick={onOpenAdmin}
                className="text-gray-500 hover:text-rose-400 transition-colors text-[11px] flex items-center gap-1 cursor-pointer"
                title="Store Manager Console"
              >
                <ShieldCheck className="w-3 h-3" />
                <span>Admin</span>
              </button>
            )}
          </div>
          <div className="flex items-center gap-2 text-[11px] text-gray-400">
            <span className="text-emerald-400 font-semibold">Cash on Delivery</span>
            <span>•</span>
            <span>Pay on Doorstep (Cash / UPI)</span>
          </div>
        </div>

      </div>
    </footer>
  );
}
