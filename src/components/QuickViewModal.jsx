import React, { useState, useEffect } from 'react';
import { X, Star, ShoppingBag, ShieldCheck, Heart, Sparkles, Check } from 'lucide-react';
import { calculatePriceForWeight } from '../utils/pricing';

export default function QuickViewModal({
  product,
  onClose,
  onAddToCart,
  isWishlisted,
  onToggleWishlist
}) {
  const weightOptions = product?.weightOptions || product?.weight_options || ['1 kg'];
  const defaultWeight = product?.defaultWeight || product?.default_weight || weightOptions[0] || '1 kg';
  const [selectedWeight, setSelectedWeight] = useState(defaultWeight);
  const [added, setAdded] = useState(false);

  const isBestseller = !!(product?.isBestseller ?? product?.is_bestseller);
  const originalPrice = product?.originalPrice ?? product?.original_price;

  // Accurately calculate price for the chosen weight (e.g. 2kg = 2x price, 500g = 0.5x price)
  const currentPrice = calculatePriceForWeight(product, selectedWeight);
  const currentOriginalPrice = originalPrice ? calculatePriceForWeight({ ...product, price: originalPrice }, selectedWeight) : null;

  useEffect(() => {
    if (product) {
      const opts = product.weightOptions || product.weight_options || ['1 kg'];
      setSelectedWeight(product.defaultWeight || product.default_weight || opts[0] || '1 kg');
    }
  }, [product]);

  if (!product) return null;

  const handleAdd = () => {
    onAddToCart({
      ...product,
      selectedWeight,
      price: currentPrice
    });
    setAdded(true);
    setTimeout(() => setAdded(false), 1200);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        onClick={onClose}
        className="fixed inset-0 bg-black/80 backdrop-blur-md transition-opacity"
      />

      {/* Glass Card Modal */}
      <div className="relative w-full max-w-2xl rounded-3xl glass-panel border border-white/20 p-6 sm:p-8 shadow-2xl z-10 animate-in fade-in zoom-in-95 duration-200">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-gray-300 hover:text-white transition-colors z-20"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
          
          {/* Product Image */}
          <div className="relative rounded-2xl overflow-hidden bg-black/50 border border-white/15 h-64 md:h-72">
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-full object-cover"
            />
            {isBestseller && (
              <span className="absolute top-3 left-3 px-3 py-1 rounded-full text-[10px] font-black uppercase bg-gradient-to-r from-red-600 to-rose-600 text-white shadow-lg">
                Bestseller
              </span>
            )}
          </div>

          {/* Details */}
          <div className="space-y-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-bold text-rose-300 uppercase tracking-wider px-2 py-0.5 rounded bg-rose-500/10 border border-rose-500/20">
                  {product.category}
                </span>
                <div className="flex items-center gap-1 text-amber-400 text-xs">
                  <Star className="w-3.5 h-3.5 fill-current" />
                  <span className="font-bold text-white">{product.rating || '4.9'}</span>
                  <span className="text-gray-400">({product.reviews || 84} reviews)</span>
                </div>
              </div>

              <h3 className="text-xl sm:text-2xl font-black text-white font-heading">
                {product.name}
              </h3>

              <div className="flex items-baseline gap-2 mt-2">
                <span className="text-2xl font-black text-white font-heading">
                  ₹{currentPrice}
                </span>
                <span className="text-xs text-rose-300 font-semibold">/ {selectedWeight}</span>
                {currentOriginalPrice && (
                  <span className="text-xs text-gray-500 line-through">
                    ₹{currentOriginalPrice}
                  </span>
                )}
              </div>
            </div>

            <p className="text-xs text-gray-300 leading-relaxed">
              {product.description}
            </p>

            {/* Serving & Cut Information */}
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="p-2.5 rounded-xl bg-white/5 border border-white/10">
                <span className="text-gray-400 block text-[10px]">Pieces:</span>
                <span className="text-white font-semibold">{product.pieces || 'Hand Cut'}</span>
              </div>
              <div className="p-2.5 rounded-xl bg-white/5 border border-white/10">
                <span className="text-gray-400 block text-[10px]">Serves:</span>
                <span className="text-white font-semibold">{product.serves || '3-4 Persons'}</span>
              </div>
            </div>

            {/* Weight Picker */}
            <div>
              <label className="block text-xs font-semibold text-gray-300 mb-1.5">
                Select Quantity / Pack Size:
              </label>
              <div className="flex flex-wrap gap-2">
                {weightOptions.map((weight) => (
                  <button
                    key={weight}
                    onClick={() => setSelectedWeight(weight)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                      selectedWeight === weight
                        ? 'btn-crimson text-white'
                        : 'bg-white/5 hover:bg-white/10 text-gray-300 border border-white/10'
                    }`}
                  >
                    {weight}
                  </button>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-3 pt-2">
              <button
                onClick={handleAdd}
                className="flex-1 btn-crimson py-3 rounded-xl text-xs sm:text-sm font-bold text-white flex items-center justify-center gap-2 shadow-lg shadow-rose-950"
              >
                {added ? (
                  <>
                    <Check className="w-4 h-4 text-emerald-300" />
                    <span>Added to Cart!</span>
                  </>
                ) : (
                  <>
                    <ShoppingBag className="w-4 h-4" />
                    <span>Add to Cart • ₹{currentPrice}</span>
                  </>
                )}
              </button>

              <button
                onClick={() => onToggleWishlist(product.id)}
                className={`w-12 h-12 rounded-xl flex items-center justify-center border transition-all ${
                  isWishlisted
                    ? 'bg-rose-600 border-rose-500 text-white'
                    : 'bg-white/5 border-white/15 text-gray-300 hover:text-rose-400'
                }`}
                aria-label="Wishlist"
              >
                <Heart className={`w-5 h-5 ${isWishlisted ? 'fill-current' : ''}`} />
              </button>
            </div>

            <div className="flex items-center gap-2 text-[11px] text-gray-400 pt-1">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Chilled 0-4°C Vacuum Packed • 100% Quality Inspected</span>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
