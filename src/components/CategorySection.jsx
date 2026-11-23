import React from 'react';
import { ArrowRight, Flame, Sparkles } from 'lucide-react';
import { CATEGORIES } from '../data/mockData';

export default function CategorySection({ onSelectCategory, selectedCategory }) {
  // Custom SVG outline icons matching the reference image's fine line art
  const renderCategoryIcon = (id) => {
    switch (id) {
      case 'chicken':
        return (
          <svg viewBox="0 0 24 24" className="w-5 h-5 text-rose-300 stroke-current fill-none stroke-2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4c2.5 0 4.5 2 4.5 4.5 0 2-1.5 3.5-3 4.5v3h-3v-3c-1.5-1-3-2.5-3-4.5C7.5 6 9.5 4 12 4z" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 19h6m-4 2h2" />
          </svg>
        );
      case 'mutton':
        return (
          <svg viewBox="0 0 24 24" className="w-5 h-5 text-rose-300 stroke-current fill-none stroke-2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M7 6c0-2 2-3 4-3s4 1 4 3m-9 3c-1.5 0-3 1.5-3 3 0 2 2 3 3 3h10c1 0 3-1 3-3 0-1.5-1.5-3-3-3H6zm2 6v6m8-6v6" />
          </svg>
        );
      case 'fish':
        return (
          <svg viewBox="0 0 24 24" className="w-5 h-5 text-rose-300 stroke-current fill-none stroke-2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M2 12s4-7 10-7 8 7 8 7-2 7-8 7-10-7-10-7zm18 0l2-3m-2 3l2 3M14 10a2 2 0 100 4 2 2 0 000-4z" />
          </svg>
        );
      case 'eggs':
        return (
          <svg viewBox="0 0 24 24" className="w-5 h-5 text-rose-300 stroke-current fill-none stroke-2">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 2C8 2 5 7 5 13a7 7 0 0014 0c0-6-3-11-7-11z" />
          </svg>
        );
      default:
        return <Sparkles className="w-5 h-5 text-rose-300" />;
    }
  };

  return (
    <section id="categories" className="py-8 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-10">
        
        {/* 4 Category Glass Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
          {CATEGORIES.map((cat) => {
            const isSelected = selectedCategory === cat.id;

            return (
              <div
                key={cat.id}
                onClick={() => onSelectCategory(cat.id)}
                className={`group relative rounded-2xl p-4 glass-card-category overflow-hidden cursor-pointer flex flex-col justify-between transition-all duration-300 ${
                  isSelected ? 'border-rose-500/80 shadow-[0_0_25px_rgba(225,29,72,0.35)]' : ''
                }`}
              >
                {/* Top Header inside card: Icon + Title + Subtitle */}
                <div className="flex items-start justify-between gap-2 mb-3">
                  <div className="flex flex-col">
                    <div className="flex items-center gap-2 mb-1">
                      <div className="w-7 h-7 rounded-lg bg-rose-500/20 border border-rose-500/30 flex items-center justify-center">
                        {renderCategoryIcon(cat.id)}
                      </div>
                      <h3 className="text-sm font-bold text-white group-hover:text-rose-200 transition-colors">
                        {cat.title}
                      </h3>
                    </div>
                    <p className="text-[11px] text-gray-400 font-medium">
                      {cat.subtitle}
                    </p>
                  </div>

                  <span className="text-[10px] text-rose-300/80 font-semibold px-2 py-0.5 rounded-full bg-white/5 border border-white/10 shrink-0">
                    {cat.itemCount}
                  </span>
                </div>

                {/* Product Image Showcase with Zoom */}
                <div className="relative h-32 w-full rounded-xl overflow-hidden my-1 bg-black/40">
                  <img
                    src={cat.image}
                    alt={cat.title}
                    className="w-full h-full object-cover object-center transform transition-transform duration-500 group-hover:scale-110"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent pointer-events-none" />
                </div>

                {/* Bottom Action: Explore Button */}
                <div className="mt-3 flex items-center justify-end">
                  <button
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold tracking-wide transition-all ${
                      isSelected 
                        ? 'btn-crimson text-white' 
                        : 'btn-glass text-gray-200 group-hover:text-white group-hover:bg-rose-600/30 group-hover:border-rose-500/40'
                    }`}
                  >
                    <span>Explore</span>
                    <ArrowRight className="w-3.5 h-3.5 transition-transform duration-200 group-hover:translate-x-1" />
                  </button>
                </div>

              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
