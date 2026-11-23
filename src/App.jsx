import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import CategorySection from './components/CategorySection';
import ProductMarketplace from './components/ProductMarketplace';
import WhyChooseUs from './components/WhyChooseUs';
import CartDrawer from './components/CartDrawer';
import QuickViewModal from './components/QuickViewModal';
import OrderSuccessModal from './components/OrderSuccessModal';
import AdminDashboardModal from './components/AdminDashboardModal';
import Footer from './components/Footer';
import api from './services/api';
import { PRODUCTS } from './data/mockData';

export default function App() {
  // Real backend products with instant fallback
  const [products, setProducts] = useState(PRODUCTS);
  const [isProductsLoading, setIsProductsLoading] = useState(false);

  // Fresh, clean cart and wishlist for all new customers (no duplicate or pre-loaded dummy data)
  const [cartItems, setCartItems] = useState([]);
  const [wishlist, setWishlist] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeSection, setActiveSection] = useState('hero');

  // Modals
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isAdminOpen, setIsAdminOpen] = useState(false);
  const [quickViewProduct, setQuickViewProduct] = useState(null);
  const [orderData, setOrderData] = useState(null);

  // Toast Notification state
  const [toast, setToast] = useState(null);

  const showToast = (message) => {
    setToast(message);
    setTimeout(() => setToast(null), 3000);
  };

  // Load products from backend on mount with strict deduplication
  const loadProducts = async () => {
    try {
      setIsProductsLoading(true);
      const data = await api.getProducts();
      if (data && data.products && data.products.length > 0) {
        // Deduplicate products by product_code or id
        const seen = new Set();
        const uniqueProducts = [];
        for (const item of data.products) {
          const key = (item.product_code || item.id || item.name).toLowerCase();
          if (!seen.has(key)) {
            seen.add(key);
            uniqueProducts.push(item);
          }
        }
        setProducts(uniqueProducts);
      }
    } catch (err) {
      console.warn('Backend product catalog load notice:', err.message);
    } finally {
      setIsProductsLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  // Cart Handlers
  const handleAddToCart = (product) => {
    const weight = product.selectedWeight || '1 kg';
    const unitPrice = product.price;

    setCartItems((prev) => {
      const existingIndex = prev.findIndex(
        (item) => item.id === product.id && item.selectedWeight === weight
      );
      if (existingIndex > -1) {
        const next = [...prev];
        next[existingIndex] = {
          ...next[existingIndex],
          price: unitPrice,
          quantity: next[existingIndex].quantity + 1
        };
        return next;
      } else {
        return [
          ...prev,
          {
            ...product,
            price: unitPrice,
            selectedWeight: weight,
            quantity: 1
          }
        ];
      }
    });
    showToast(`Added ${product.name} (${weight}) - ₹${unitPrice} to cart`);
  };

  const handleUpdateQty = (productId, newQty, selectedWeight) => {
    if (newQty <= 0) {
      handleRemoveItem(productId, selectedWeight);
      return;
    }
    setCartItems((prev) =>
      prev.map((item) => {
        const matches = item.id === productId && (!selectedWeight || item.selectedWeight === selectedWeight);
        return matches ? { ...item, quantity: newQty } : item;
      })
    );
  };

  const handleRemoveItem = (productId, selectedWeight) => {
    setCartItems((prev) =>
      prev.filter((item) =>
        !(item.id === productId && (!selectedWeight || item.selectedWeight === selectedWeight))
      )
    );
    showToast('Item removed from cart');
  };

  const handleClearCart = () => {
    setCartItems([]);
  };

  // Wishlist Handler
  const handleToggleWishlist = (productId) => {
    setWishlist((prev) => {
      if (prev.includes(productId)) {
        showToast('Removed from wishlist');
        return prev.filter((id) => id !== productId);
      } else {
        showToast('Added to your wishlist!');
        return [...prev, productId];
      }
    });
  };

  // Category selection handler with auto-scroll
  const handleSelectCategory = (catId) => {
    setSelectedCategory(catId);
    const marketplaceEl = document.getElementById('marketplace');
    if (marketplaceEl) {
      marketplaceEl.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Checkout Success
  const handleCheckoutSuccess = (order) => {
    setOrderData(order);
    setCartItems([]);
    setIsCartOpen(false);
  };

  return (
    <div className="min-h-screen bg-[#0e0405] text-[#F3F4F6] relative selection:bg-rose-600 selection:text-white">
      
      {/* Global Cinematic Background Image & Atmospheric Lighting */}
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-top bg-no-repeat opacity-85 filter brightness-90 contrast-110"
          style={{ backgroundImage: `url('/images/bg-cinematic-red.jpg')` }}
        />
        {/* Soft vignette to guarantee readable glass card content */}
        <div className="absolute inset-0 bg-gradient-to-b from-[#0e0405]/40 via-[#100305]/60 to-[#0e0405]/90" />
      </div>

      {/* Toast Notification Pill */}
      {toast && (
        <div className="fixed bottom-6 right-6 z-50 animate-in slide-in-from-bottom-5 fade-in duration-300">
          <div className="glass-panel px-4 py-2.5 rounded-2xl border border-rose-500/50 shadow-2xl flex items-center gap-2 text-xs font-semibold text-white">
            <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
            <span>{toast}</span>
          </div>
        </div>
      )}

      {/* Sticky Floating Glassmorphism Navbar */}
      <Navbar
        cartCount={cartItems.reduce((acc, item) => acc + item.quantity, 0)}
        onOpenCart={() => setIsCartOpen(true)}
        onOpenAdmin={() => setIsAdminOpen(true)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        activeSection={activeSection}
        setActiveSection={setActiveSection}
        onSelectCategory={handleSelectCategory}
      />

      {/* Main Content Area */}
      <main>
        {/* Cinematic Hero Section */}
        <HeroSection
          onShopNow={() => {
            const el = document.getElementById('marketplace');
            if (el) el.scrollIntoView({ behavior: 'smooth' });
          }}
          onExplore={() => {
            const el = document.getElementById('categories');
            if (el) el.scrollIntoView({ behavior: 'smooth' });
          }}
        />

        {/* 4 Product Category Cards matching reference */}
        <CategorySection
          onSelectCategory={handleSelectCategory}
          selectedCategory={selectedCategory}
        />

        {/* Best Selling Products Marketplace */}
        <ProductMarketplace
          products={products}
          isLoading={isProductsLoading}
          cartItems={cartItems}
          onAddToCart={handleAddToCart}
          onUpdateQty={handleUpdateQty}
          wishlist={wishlist}
          onToggleWishlist={handleToggleWishlist}
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
          searchQuery={searchQuery}
          onQuickView={(prod) => setQuickViewProduct(prod)}
        />

        {/* Why Discerning Chefs Choose Us & Stats */}
        <WhyChooseUs />
      </main>

      {/* Luxury Burgundy Glass Footer with subtle Admin link */}
      <Footer
        onSelectCategory={handleSelectCategory}
        onOpenAdmin={() => setIsAdminOpen(true)}
      />

      {/* Interactive Sliding Glass Shopping Cart Drawer */}
      <CartDrawer
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cartItems={cartItems}
        onUpdateQty={handleUpdateQty}
        onRemoveItem={handleRemoveItem}
        onClearCart={handleClearCart}
        onCheckoutSuccess={handleCheckoutSuccess}
      />

      {/* Product Quick View Inspector Modal */}
      <QuickViewModal
        product={quickViewProduct}
        onClose={() => setQuickViewProduct(null)}
        onAddToCart={handleAddToCart}
        isWishlisted={quickViewProduct ? wishlist.includes(quickViewProduct.id) : false}
        onToggleWishlist={handleToggleWishlist}
      />

      {/* Checkout Celebration & Order Receipt Modal */}
      <OrderSuccessModal
        orderData={orderData}
        onClose={() => setOrderData(null)}
      />

      {/* Admin Dashboard Console Modal */}
      <AdminDashboardModal
        isOpen={isAdminOpen}
        onClose={() => setIsAdminOpen(false)}
        onShowToast={showToast}
        onProductsUpdated={loadProducts}
      />

    </div>
  );
}
