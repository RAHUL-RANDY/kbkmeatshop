import React, { useState } from 'react';
import { Heart, ShoppingBag, Plus, Minus, Check, ChevronDown, Eye } from 'lucide-react';
import { calculatePriceForWeight } from '../utils/pricing';

export default function ProductCard({
  product,
  onAddToCart,
  cartItem,
  cartItems = [],
  onUpdateQty,
  isWishlisted,
  onToggleWishlist,
  onQuickView
}) {
  const weightOptions = product?.weightOptions || product?.weight_options || ['1 kg'];
  const defaultWeight = product?.defaultWeight || product?.default_weight || weightOptions[0] || '1 kg';
  const [selectedWeight, setSelectedWeight] = useState(defaultWeight);
  const [showWeightDropdown, setShowWeightDropdown] = useState(false);
  const [addedAnimation, setAddedAnimation] = useState(false);

  const isBestseller = !!(product?.isBestseller ?? product?.is_bestseller);
  const originalPrice = product?.originalPrice ?? product?.original_price;

  // Accurately calculate price for the chosen weight (e.g. 2kg = 2x price, 500g = 0.5x price)
  const currentPrice = calculatePriceForWeight(product, selectedWeight);
  const currentOriginalPrice = originalPrice ? calculatePriceForWeight({ ...product, price: originalPrice }, selectedWeight) : null;

  // Find if this exact product with this exact weight is in the cart
  const activeCartItem = (cartItems && cartItems.length > 0)
    ? cartItems.find((item) => item.id === product.id && item.selectedWeight === selectedWeight)
    : (cartItem && cartItem.selectedWeight === selectedWeight ? cartItem : null);

  const handleAdd = (e) => {
    e.stopPropagation();
    onAddToCart({
      ...product,
      selectedWeight,
      price: currentPrice
    });
    setAddedAnimation(true);
    setTimeout(() => setAddedAnimation(false), 900);
  };

  return (
    <div className="group relative rounded-2xl p-3.5 sm:p-4 glass-card flex flex-col justify-between transition-all duration-300">
      
      {/* Top Card Bar: Badges & Wishlist */}
      <div className="relative mb-2">
        <div className="flex items-center justify-between z-10 relative">
          {/* Badge: Bestseller or Fresh */}
          {isBestseller ? (
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-gradient-to-r from-red-600 to-rose-600 text-white shadow-md shadow-red-900/40">
              Bestseller
            </span>
          ) : (
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-white/10 text-rose-200 border border-white/15">
              100% Fresh
            </span>
          )}

          {/* Action Icons: Quick View & Wishlist */}
          <div className="flex items-center gap-1.5">
            <button
              onClick={(e) => {
                e.stopPropagation();
                onQuickView(product);
              }}
              className="w-7 h-7 rounded-full bg-black/40 hover:bg-white/20 border border-white/15 flex items-center justify-center text-gray-300 hover:text-white transition-all opacity-0 group-hover:opacity-100"
              title="Quick View"
              aria-label="Quick View"
            >
              <Eye className="w-3.5 h-3.5" />
            </button>

            <button
              onClick={(e) => {
                e.stopPropagation();
                onToggleWishlist(product.id);
              }}
              className={`w-7 h-7 rounded-full flex items-center justify-center border transition-all ${
                isWishlisted
                  ? 'bg-rose-600 border-rose-500 text-white shadow-md shadow-rose-900/50'
                  : 'bg-black/40 border-white/15 text-gray-300 hover:text-rose-400 hover:border-rose-400/40'
              }`}
              title="Save to Wishlist"
              aria-label="Save to Wishlist"
            >
              <Heart className={`w-3.5 h-3.5 ${isWishlisted ? 'fill-current text-white' : ''}`} />
            </button>
          </div>
        </div>

        {/* Product Image with Hover Zoom */}
        <div 
          onClick={() => onQuickView(product)}
          className="relative h-40 sm:h-44 w-full rounded-xl overflow-hidden mt-2 bg-gradient-to-b from-[#1a0507] to-black/60 cursor-pointer flex items-center justify-center"
        >
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-full object-cover object-center transform transition-transform duration-500 group-hover:scale-108"
            loading="lazy"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent pointer-events-none" />
        </div>
      </div>

      {/* Product Details */}
      <div className="flex-1 flex flex-col justify-between pt-1">
        <div>
          <h4 
            onClick={() => onQuickView(product)}
            className="text-sm sm:text-base font-bold text-white group-hover:text-rose-200 transition-colors cursor-pointer line-clamp-1"
          >
            {product.name}
          </h4>

          {/* Pricing */}
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-base sm:text-lg font-extrabold text-white font-heading">
              ₹{currentPrice}
            </span>
            <span className="text-xs text-rose-300 font-semibold">
              / {selectedWeight}
            </span>
            {currentOriginalPrice && (
              <span className="text-[11px] text-gray-500 line-through">
                ₹{currentOriginalPrice}
              </span>
            )}
          </div>
        </div>

        {/* Card Controls matching reference image: Weight Selector + Add to Cart */}
        <div className="flex items-center gap-2 mt-3 pt-2 border-t border-white/10">
          
          {/* Weight Selection Dropdown */}
          <div className="relative shrink-0">
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowWeightDropdown(!showWeightDropdown);
              }}
              className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-[11px] font-semibold text-gray-200 bg-white/10 hover:bg-white/15 border border-white/15 transition-all"
            >
              <span>{selectedWeight}</span>
              <ChevronDown className="w-3 h-3 text-gray-400" />
            </button>

            {showWeightDropdown && (
              <div className="absolute bottom-full left-0 mb-1 w-28 py-1 rounded-xl glass-panel border border-white/20 shadow-2xl z-30">
                {weightOptions.map((w) => (
                  <button
                    key={w}
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedWeight(w);
                      setShowWeightDropdown(false);
                    }}
                    className={`w-full text-left px-3 py-1.5 text-[11px] font-medium transition-colors ${
                      selectedWeight === w ? 'text-rose-300 bg-rose-950/60 font-bold' : 'text-gray-300 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    {w}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Add to Cart Button or Quantity Counter */}
          <div className="flex-1">
            {activeCartItem ? (
              <div className="flex items-center justify-between rounded-lg bg-rose-950/80 border border-rose-500/40 p-0.5">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onUpdateQty(product.id, activeCartItem.quantity - 1, selectedWeight);
                  }}
                  className="w-6 h-6 rounded-md bg-white/10 hover:bg-white/20 flex items-center justify-center text-white"
                  aria-label="Decrease quantity"
                >
                  <Minus className="w-3 h-3" />
                </button>
                <span className="text-xs font-bold text-white px-2">
                  {activeCartItem.quantity}
                </span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onUpdateQty(product.id, activeCartItem.quantity + 1, selectedWeight);
                  }}
                  className="w-6 h-6 rounded-md bg-rose-600 hover:bg-rose-500 flex items-center justify-center text-white"
                  aria-label="Increase quantity"
                >
                  <Plus className="w-3 h-3" />
                </button>
              </div>
            ) : (
              <button
                onClick={handleAdd}
                className="w-full btn-crimson py-1.5 px-3 rounded-lg text-xs font-bold text-white flex items-center justify-center gap-1.5 group/btn cursor-pointer transition-all"
              >
                {addedAnimation ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-300" />
                    <span>Added!</span>
                  </>
                ) : (
                  <>
                    <ShoppingBag className="w-3.5 h-3.5" />
                    <span>Add to Cart</span>
                  </>
                )}
              </button>
            )}
          </div>

        </div>

      </div>

    </div>
  );
}
