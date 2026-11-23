import React, { useState, useEffect } from 'react';
import { Search, ShoppingBag, ChevronDown, Menu, X, ShieldCheck } from 'lucide-react';

export default function Navbar({
  cartCount,
  onOpenCart,
  onOpenAdmin,
  searchQuery,
  setSearchQuery,
  activeSection,
  setActiveSection,
  onSelectCategory
}) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [showMeatMenu, setShowMeatMenu] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id) => {
    setActiveSection(id);
    setIsMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 px-3 sm:px-6 lg:px-10 pt-2 sm:pt-3 transition-all duration-300 space-y-1.5">
      {/* Top Pre-Booking Announcement Bar */}
      <div className="max-w-7xl mx-auto px-4 py-1 rounded-full bg-black/60 backdrop-blur-md border border-rose-500/30 text-center text-[10px] sm:text-xs font-medium text-rose-200 flex items-center justify-center gap-2 shadow-lg">
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse shrink-0" />
        <span className="truncate">
          <strong className="text-white">Pre-Book Mon–Fri:</strong> Farm-harvested fresh & delivered exclusively on <strong className="text-emerald-400">Saturday & Sunday Morning</strong>!
        </span>
        <span className="hidden sm:inline-block text-gray-500">•</span>
        <span className="hidden sm:inline-block text-emerald-300 font-semibold text-[10px] uppercase tracking-wider">Cash on Delivery</span>
      </div>

      <div className={`max-w-7xl mx-auto rounded-2xl transition-all duration-300 ${
        isScrolled 
          ? 'glass-nav py-2 px-4 sm:px-6 shadow-2xl' 
          : 'glass-panel py-2.5 px-4 sm:px-6'
      }`}>
        <div className="flex items-center justify-between gap-2 lg:gap-6">
          
          {/* Logo & Brand */}
          <div 
            onClick={() => scrollToSection('hero')} 
            className="flex items-center gap-2.5 sm:gap-3 cursor-pointer group shrink-0"
          >
            {/* Official KBK Meat Shop Logo */}
            <div className="h-10 sm:h-12 w-14 sm:w-16 rounded-xl bg-white p-1 border border-white/50 shadow-md flex items-center justify-center overflow-hidden transition-transform duration-300 group-hover:scale-105">
              <img
                src="/images/kbk-logo.jpg"
                alt="KBK MEATE SHOP Logo"
                className="w-full h-full object-contain"
              />
            </div>
            
            <div className="flex flex-col leading-tight">
              <span className="text-sm sm:text-base font-extrabold tracking-tight text-white font-heading">
                KBK MEAT
              </span>
              <span className="text-xs sm:text-sm font-bold tracking-widest text-rose-300/90 -mt-0.5">
                SHOP
              </span>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden lg:flex items-center gap-1 xl:gap-2">
            <button
              onClick={() => scrollToSection('hero')}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold tracking-wide transition-all ${
                activeSection === 'hero'
                  ? 'btn-crimson text-white shadow-lg shadow-rose-900/40'
                  : 'text-gray-300 hover:text-white hover:bg-white/5'
              }`}
            >
              Home
            </button>

            <button
              onClick={() => scrollToSection('about')}
              className={`px-3.5 py-1.5 rounded-full text-xs font-medium tracking-wide transition-all ${
                activeSection === 'about'
                  ? 'btn-crimson text-white'
                  : 'text-gray-300 hover:text-white hover:bg-white/5'
              }`}
            >
              About
            </button>

            {/* Meat Market Dropdown */}
            <div 
              className="relative"
              onMouseEnter={() => setShowMeatMenu(true)}
              onMouseLeave={() => setShowMeatMenu(false)}
            >
              <button
                onClick={() => scrollToSection('marketplace')}
                className={`flex items-center gap-1 px-3.5 py-1.5 rounded-full text-xs font-medium tracking-wide transition-all ${
                  activeSection === 'marketplace'
                    ? 'btn-crimson text-white'
                    : 'text-gray-300 hover:text-white hover:bg-white/5'
                }`}
              >
                <span>Meat Shop</span>
                <ChevronDown className="w-3.5 h-3.5 opacity-70 transition-transform duration-200 group-hover:rotate-180" />
              </button>

              {/* Glass Dropdown Menu */}
              {showMeatMenu && (
                <div className="absolute top-full left-0 mt-2 w-48 py-2 rounded-xl glass-panel border border-white/20 shadow-2xl backdrop-blur-2xl animate-in fade-in slide-in-from-top-2 duration-150">
                  <button
                    onClick={() => {
                      onSelectCategory('chicken');
                      scrollToSection('marketplace');
                      setShowMeatMenu(false);
                    }}
                    className="w-full text-left px-4 py-2 text-xs font-medium text-gray-200 hover:text-white hover:bg-rose-900/40 flex items-center gap-2"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                    Fresh Chicken
                  </button>
                  <button
                    onClick={() => {
                      onSelectCategory('mutton');
                      scrollToSection('marketplace');
                      setShowMeatMenu(false);
                    }}
                    className="w-full text-left px-4 py-2 text-xs font-medium text-gray-200 hover:text-white hover:bg-rose-900/40 flex items-center gap-2"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                    Fresh Mutton
                  </button>
                  <button
                    onClick={() => {
                      onSelectCategory('fish');
                      scrollToSection('marketplace');
                      setShowMeatMenu(false);
                    }}
                    className="w-full text-left px-4 py-2 text-xs font-medium text-gray-200 hover:text-white hover:bg-rose-900/40 flex items-center gap-2"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                    Fresh Fish & Seafood
                  </button>
                </div>
              )}
            </div>

            <button
              onClick={() => {
                onSelectCategory('eggs');
                scrollToSection('marketplace');
              }}
              className="px-3.5 py-1.5 rounded-full text-xs font-medium tracking-wide text-gray-300 hover:text-white hover:bg-white/5 transition-all"
            >
              Eggs
            </button>

            <button
              onClick={() => scrollToSection('contact')}
              className={`px-3.5 py-1.5 rounded-full text-xs font-medium tracking-wide transition-all ${
                activeSection === 'contact'
                  ? 'btn-crimson text-white'
                  : 'text-gray-300 hover:text-white hover:bg-white/5'
              }`}
            >
              Contact
            </button>
          </nav>

          {/* Search Bar - Glass Pill Input */}
          <div className="hidden md:flex items-center relative flex-1 max-w-xs xl:max-w-sm">
            <Search className="w-4 h-4 text-gray-400 absolute left-3.5 pointer-events-none" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search meat, chicken, eggs..."
              className="w-full pl-9 pr-4 py-1.5 rounded-full text-xs font-medium glass-input placeholder:text-gray-400/80 focus:ring-1 focus:ring-rose-500/50"
            />
            {searchQuery && (
              <button 
                onClick={() => setSearchQuery('')}
                className="absolute right-3 text-xs text-gray-400 hover:text-white"
              >
                ✕
              </button>
            )}
          </div>

          {/* Right Action Icons: Admin, Cart & Mobile Menu */}
          <div className="flex items-center gap-2 sm:gap-2.5">
            {/* Admin Panel Button */}
            {onOpenAdmin && (
              <button
                onClick={onOpenAdmin}
                className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-full btn-glass text-rose-300 hover:text-white border border-rose-500/30 hover:border-rose-400 text-xs font-semibold hover:scale-105 active:scale-95 transition-all shadow-sm cursor-pointer"
                title="Open Admin Dashboard"
              >
                <ShieldCheck className="w-3.5 h-3.5 text-rose-400" />
                <span>Admin Panel</span>
              </button>
            )}

            {/* Cart Button */}
            <button
              onClick={onOpenCart}
              className="relative p-2 sm:px-3 sm:py-2 rounded-full btn-glass flex items-center gap-2 text-white hover:scale-105 active:scale-95 transition-all"
              aria-label="Open Shopping Cart"
            >
              <ShoppingBag className="w-4 h-4 text-white" />
              <span className="hidden sm:inline text-xs font-semibold">Cart</span>
              {cartCount > 0 && (
                <span className="absolute -top-1 -right-1 sm:static sm:top-auto sm:right-auto bg-gradient-to-r from-red-600 to-rose-500 text-white text-[10px] font-black w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center shadow-md animate-pulse">
                  {cartCount}
                </span>
              )}
            </button>

            {/* Mobile Menu Toggle */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="lg:hidden p-2 rounded-xl text-gray-300 hover:text-white hover:bg-white/10"
              aria-label="Toggle Navigation Menu"
            >
              {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>

        </div>

        {/* Mobile Expanded Drawer */}
        {isMobileMenuOpen && (
          <div className="lg:hidden pt-4 pb-2 border-t border-white/10 mt-3 flex flex-col gap-2 animate-in fade-in duration-200">
            {/* Mobile Search Input */}
            <div className="relative mb-2">
              <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search meat, chicken, eggs..."
                className="w-full pl-9 pr-3 py-2 rounded-xl text-xs glass-input"
              />
            </div>

            <div className="grid grid-cols-2 gap-2 text-center">
              <button
                onClick={() => scrollToSection('hero')}
                className="py-2 px-3 rounded-lg text-xs font-medium bg-white/5 hover:bg-rose-900/40 text-gray-200"
              >
                Home
              </button>
              <button
                onClick={() => scrollToSection('about')}
                className="py-2 px-3 rounded-lg text-xs font-medium bg-white/5 hover:bg-rose-900/40 text-gray-200"
              >
                About Us
              </button>
              <button
                onClick={() => {
                  onSelectCategory('all');
                  scrollToSection('marketplace');
                }}
                className="py-2 px-3 rounded-lg text-xs font-medium bg-white/5 hover:bg-rose-900/40 text-gray-200"
              >
                Meat Shop
              </button>
              <button
                onClick={() => {
                  onSelectCategory('eggs');
                  scrollToSection('marketplace');
                }}
                className="py-2 px-3 rounded-lg text-xs font-medium bg-white/5 hover:bg-rose-900/40 text-gray-200"
              >
                Farm Eggs
              </button>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => scrollToSection('contact')}
                className="flex-1 py-2 px-3 rounded-lg text-xs font-medium bg-rose-900/40 text-rose-200 text-center"
              >
                Contact Support
              </button>
              {onOpenAdmin && (
                <button
                  onClick={() => {
                    onOpenAdmin();
                    setIsMobileMenuOpen(false);
                  }}
                  className="flex-1 py-2 px-3 rounded-lg text-xs font-bold bg-rose-950/80 border border-rose-500/40 text-rose-300 text-center flex items-center justify-center gap-1.5 hover:bg-rose-900/50"
                >
                  <ShieldCheck className="w-3.5 h-3.5 text-rose-400" />
                  <span>Admin Panel</span>
                </button>
              )}
            </div>
          </div>
        )}

      </div>
    </header>
  );
}
