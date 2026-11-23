import React, { useState, useMemo } from 'react';
import { Flame, ArrowRight, Filter, SlidersHorizontal, Sparkles } from 'lucide-react';
import ProductCard from './ProductCard';
import { PRODUCTS } from '../data/mockData';

export default function ProductMarketplace({
  cartItems,
  onAddToCart,
  onUpdateQty,
  wishlist,
  onToggleWishlist,
  selectedCategory,
  onSelectCategory,
  searchQuery,
  onQuickView,
  products = null,
  isLoading = false
}) {
  const [sortBy, setSortBy] = useState('popular');
  const [filterType, setFilterType] = useState('all');

  const filterTabs = [
    { id: 'all', label: 'All Products' },
    { id: 'chicken', label: 'Fresh Chicken' },
    { id: 'mutton', label: 'Tender Mutton' },
    { id: 'fish', label: 'Fresh Fish' },
    { id: 'eggs', label: 'Farm Fresh Eggs' }
  ];

  // Active category: if selected from category cards or internal tabs
  const activeCat = selectedCategory !== 'all' ? selectedCategory : filterType;

  const filteredProducts = useMemo(() => {
    const sourceList = (products && products.length > 0) ? products : PRODUCTS;
    
    // Strict deduplication to ensure zero duplicate products are ever displayed
    const seen = new Set();
    let list = [];
    for (const item of sourceList) {
      const key = (item.product_code || item.id || item.name).toLowerCase();
      if (!seen.has(key)) {
        seen.add(key);
        list.push(item);
      }
    }

    // Filter by Category
    if (activeCat !== 'all') {
      list = list.filter((p) => p.category === activeCat);
    }

    // Filter by Search
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      list = list.filter(
        (p) =>
          (p.name || '').toLowerCase().includes(q) ||
          (p.category || '').toLowerCase().includes(q) ||
          (p.description || '').toLowerCase().includes(q)
      );
    }

    // Sort
    if (sortBy === 'price-low') {
      list.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-high') {
      list.sort((a, b) => b.price - a.price);
    } else if (sortBy === 'rating') {
      list.sort((a, b) => b.rating - a.rating);
    } else {
      // popular (bestsellers first)
      list.sort((a, b) => ((b.isBestseller ?? b.is_bestseller) ? 1 : 0) - ((a.isBestseller ?? a.is_bestseller) ? 1 : 0));
    }

    return list;
  }, [products, activeCat, searchQuery, sortBy]);

  return (
    <section id="marketplace" className="py-12 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-10">
        
        {/* Marketplace Section Header matching reference image */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-2.5">
            <span className="text-2xl animate-bounce">🔥</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white font-heading tracking-tight">
              Best Selling Products
            </h2>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={() => {
                onSelectCategory('all');
                setFilterType('all');
              }}
              className="text-xs sm:text-sm font-semibold text-rose-300 hover:text-white flex items-center gap-1.5 transition-colors group cursor-pointer"
            >
              <span>View All Products</span>
              <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
            </button>
          </div>
        </div>

        {/* Filter Pills & Sorting Controls */}
        <div className="flex flex-wrap items-center justify-between gap-3 mb-8 pb-3 border-b border-white/10">
          
          {/* Category Filter Pills */}
          <div className="flex flex-wrap items-center gap-2">
            {filterTabs.map((tab) => {
              const isActive = activeCat === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    onSelectCategory(tab.id);
                    setFilterType(tab.id);
                  }}
                  className={`px-3.5 py-1.5 rounded-full text-xs font-semibold tracking-wide transition-all ${
                    isActive
                      ? 'btn-crimson text-white shadow-md shadow-rose-950'
                      : 'btn-glass text-gray-300 hover:text-white hover:border-white/30'
                  }`}
                >
                  {tab.label}
                </button>
              );
            })}
          </div>

          {/* Sort Dropdown */}
          <div className="flex items-center gap-2">
            <SlidersHorizontal className="w-3.5 h-3.5 text-gray-400" />
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="glass-panel text-xs font-medium text-gray-200 px-3 py-1.5 rounded-xl border border-white/15 focus:outline-none focus:border-rose-500 cursor-pointer"
            >
              <option value="popular" className="bg-[#1a0507] text-white">Popularity</option>
              <option value="price-low" className="bg-[#1a0507] text-white">Price: Low to High</option>
              <option value="price-high" className="bg-[#1a0507] text-white">Price: High to Low</option>
              <option value="rating" className="bg-[#1a0507] text-white">Top Customer Rating</option>
            </select>
          </div>

        </div>

        {/* Empty State */}
        {filteredProducts.length === 0 ? (
          <div className="glass-panel rounded-3xl p-12 text-center max-w-md mx-auto my-8 border border-white/15">
            <Sparkles className="w-10 h-10 text-rose-400 mx-auto mb-3 opacity-60" />
            <h3 className="text-lg font-bold text-white mb-1">No products found</h3>
            <p className="text-xs text-gray-400 mb-4">
              Try adjusting your category filter or search keywords.
            </p>
            <button
              onClick={() => {
                onSelectCategory('all');
                setFilterType('all');
              }}
              className="btn-crimson px-5 py-2 rounded-full text-xs font-semibold text-white"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          /* Products Grid (6 cards row on 3 cols / 2 cols on tablet / 1 col mobile) */
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {filteredProducts.map((product) => {
              const isWishlisted = wishlist.includes(product.id);

              return (
                <ProductCard
                  key={product.id}
                  product={product}
                  onAddToCart={onAddToCart}
                  cartItems={cartItems}
                  onUpdateQty={onUpdateQty}
                  isWishlisted={isWishlisted}
                  onToggleWishlist={onToggleWishlist}
                  onQuickView={onQuickView}
                />
              );
            })}
          </div>
        )}

      </div>
    </section>
  );
}
