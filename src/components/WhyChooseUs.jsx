import React from 'react';
import { ThermometerSnowflake, ShieldCheck, Zap, CheckCircle2, Award, Truck, Sparkles } from 'lucide-react';
import { TRUST_FEATURES } from '../data/mockData';

export default function WhyChooseUs() {
  const getFeatureIcon = (iconName) => {
    switch (iconName) {
      case 'ThermometerSnowflake':
        return <ThermometerSnowflake className="w-6 h-6 text-cyan-300" />;
      case 'ShieldCheck':
        return <ShieldCheck className="w-6 h-6 text-emerald-300" />;
      case 'Zap':
        return <Zap className="w-6 h-6 text-amber-300" />;
      case 'CheckCircle2':
        return <CheckCircle2 className="w-6 h-6 text-rose-300" />;
      default:
        return <Award className="w-6 h-6 text-rose-300" />;
    }
  };

  return (
    <section id="about" className="py-16 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-10">
        
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-12 space-y-3">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full glass-badge text-xs font-semibold text-rose-300 border border-rose-500/30">
            <Sparkles className="w-3.5 h-3.5" />
            <span>The KBK MEAT SHOP Difference</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white font-heading tracking-tight">
            Why Discerning Chefs Choose Us
          </h2>
          <p className="text-gray-300 text-xs sm:text-sm leading-relaxed">
            From biosafety audited local poultry farms to precision cold-chain transportation, we uphold the highest international culinary standards.
          </p>
        </div>

        {/* 4 Feature Glass Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {TRUST_FEATURES.map((feature) => (
            <div
              key={feature.id}
              className="group rounded-2xl p-6 glass-card border border-white/15 flex flex-col justify-between hover:border-rose-500/40 transition-all duration-300"
            >
              <div>
                <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/15 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300 shadow-inner">
                  {getFeatureIcon(feature.icon)}
                </div>
                <h3 className="text-base font-bold text-white mb-2 group-hover:text-rose-200 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-xs text-gray-400 leading-relaxed">
                  {feature.desc}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-white/10 flex items-center gap-1.5 text-[11px] font-semibold text-rose-300">
                <span>Verified Standard</span>
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              </div>
            </div>
          ))}
        </div>

        {/* Statistics Bar */}
        <div className="mt-12 rounded-2xl glass-panel p-6 sm:p-8 border border-white/15">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center divide-y md:divide-y-0 md:divide-x divide-white/10">
            <div className="pt-2 md:pt-0">
              <div className="text-2xl sm:text-4xl font-black text-white font-heading mb-1">
                Sat & Sun
              </div>
              <div className="text-xs text-gray-400 font-medium">Weekend Fresh Harvest Delivery</div>
            </div>

            <div className="pt-4 md:pt-0">
              <div className="text-2xl sm:text-4xl font-black text-white font-heading mb-1">
                0-4°C
              </div>
              <div className="text-xs text-gray-400 font-medium">Chilled Cold Chain</div>
            </div>

            <div className="pt-4 md:pt-0">
              <div className="text-2xl sm:text-4xl font-black text-white font-heading mb-1">
                100%
              </div>
              <div className="text-xs text-gray-400 font-medium">Antibiotic & Chemical Free</div>
            </div>

            <div className="pt-4 md:pt-0">
              <div className="text-2xl sm:text-4xl font-black text-white font-heading mb-1">
                50,000+
              </div>
              <div className="text-xs text-gray-400 font-medium">Satisfied Households</div>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}
