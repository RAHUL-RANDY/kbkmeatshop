const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  getToken() {
    return localStorage.getItem('fmm_token');
  }

  setToken(token) {
    if (token) {
      localStorage.setItem('fmm_token', token);
    } else {
      localStorage.removeItem('fmm_token');
    }
  }

  getUser() {
    const raw = localStorage.getItem('fmm_user');
    try {
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  getCurrentUser() {
    return this.getUser();
  }

  setUser(user) {
    if (user) {
      localStorage.setItem('fmm_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('fmm_user');
    }
  }

  async request(endpoint, options = {}) {
    const token = this.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
      ...options,
      headers
    };

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, config);
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.message || `Request failed with status ${response.status}`);
      }

      return data;
    } catch (err) {
      console.warn(`[API] Error on ${endpoint}:`, err.message);
      throw err;
    }
  }

  // Auth APIs
  async register(data) {
    const res = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data)
    });
    if (res.access_token) {
      this.setToken(res.access_token);
      this.setUser(res.user);
    }
    return res;
  }

  async login(email, password) {
    const res = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    if (res.access_token) {
      this.setToken(res.access_token);
      this.setUser(res.user);
    }
    return res;
  }

  async getProfile() {
    const res = await this.request('/auth/profile');
    if (res.user) {
      this.setUser(res.user);
    }
    return res;
  }

  async updateProfile(data) {
    return this.request('/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  logout() {
    this.setToken(null);
    this.setUser(null);
  }

  // Categories API
  async getCategories() {
    return this.request('/categories');
  }

  // Products API
  async getProducts(params = {}) {
    const query = new URLSearchParams();
    if (params.category && params.category !== 'all') query.set('category', params.category);
    if (params.search) query.set('search', params.search);
    if (params.sort) query.set('sort', params.sort);
    if (params.bestseller) query.set('bestseller', 'true');
    const qs = query.toString();
    return this.request(`/products${qs ? `?${qs}` : ''}`);
  }

  async getProductById(id) {
    return this.request(`/products/${id}`);
  }

  async searchProducts(q) {
    return this.request(`/products/search?q=${encodeURIComponent(q)}`);
  }

  // Cart API
  async getCart() {
    return this.request('/cart');
  }

  async addToCart(productId, quantity = 1, selectedWeight = '1 kg') {
    return this.request('/cart/add', {
      method: 'POST',
      body: JSON.stringify({
        product_id: productId,
        quantity,
        selected_weight: selectedWeight
      })
    });
  }

  async updateCartItem(itemId, quantity) {
    return this.request(`/cart/update/${itemId}`, {
      method: 'PUT',
      body: JSON.stringify({ quantity })
    });
  }

  async removeCartItem(itemId) {
    return this.request(`/cart/remove/${itemId}`, {
      method: 'DELETE'
    });
  }

  async clearCart() {
    return this.request('/cart/clear', {
      method: 'DELETE'
    });
  }

  // Address API
  async getAddresses() {
    return this.request('/addresses');
  }

  async addAddress(data) {
    return this.request('/addresses', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async deleteAddress(id) {
    return this.request(`/addresses/${id}`, {
      method: 'DELETE'
    });
  }

  // Orders API
  async placeOrder(data) {
    return this.request('/orders', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async getOrders() {
    return this.request('/orders');
  }

  async getOrderById(id) {
    return this.request(`/orders/${id}`);
  }

  async cancelOrder(id) {
    return this.request(`/orders/${id}/cancel`, {
      method: 'PUT'
    });
  }

  // Payments API
  async createPayment(orderId) {
    return this.request('/payments/create', {
      method: 'POST',
      body: JSON.stringify({ order_id: orderId })
    });
  }

  async verifyPayment(data) {
    return this.request('/payments/verify', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // Admin APIs
  async getAdminDashboard() {
    return this.request('/admin/dashboard');
  }

  async getAdminOrders(status = 'all') {
    return this.request(`/admin/orders?status=${status}`);
  }

  async updateOrderStatus(id, data) {
    return this.request(`/admin/orders/${id}/status`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async getAdminCustomers() {
    return this.request('/admin/customers');
  }

  async adminAddProduct(data) {
    return this.request('/admin/products', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  async adminUpdateProduct(id, data) {
    return this.request(`/admin/products/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async adminDeleteProduct(id) {
    return this.request(`/admin/products/${id}`, {
      method: 'DELETE'
    });
  }

  async getAdminSettings() {
    return this.request('/admin/settings');
  }

  async updateAdminSettings(data) {
    return this.request('/admin/settings', {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async testEmail(data) {
    return this.request('/admin/test-email', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  // 2-Day Data Retention Policy Cleanup API
  async cleanupExpiredOrders(days = 2) {
    return this.request('/admin/cleanup-expired-orders', {
      method: 'POST',
      body: JSON.stringify({ days })
    });
  }

  async getRetentionPolicy() {
    return this.request('/admin/retention-policy');
  }
}

export const api = new ApiService();
export default api;
