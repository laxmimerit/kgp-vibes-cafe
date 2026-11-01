/**
 * cart.js
 * Persistent shopping cart management using localStorage.
 */

const Cart = {
  STORAGE_KEY: 'kgp_cart',

  getCart() {
    try {
      const data = localStorage.getItem(this.STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error('Error reading cart from localStorage', e);
      return [];
    }
  },

  saveCart(cart) {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(cart));
      this.dispatchUpdate();
    } catch (e) {
      console.error('Error saving cart to localStorage', e);
    }
  },

  addToCart(item, quantity = 1) {
    if (!item || !item.id) return;
    const qty = Number(quantity) || 1;
    const cart = this.getCart();
    const existingIndex = cart.findIndex(ci => ci.id === item.id);

    if (existingIndex > -1) {
      cart[existingIndex].quantity = (Number(cart[existingIndex].quantity) || 0) + qty;
    } else {
      cart.push({
        id: item.id,
        name: item.name,
        price: Number(item.price),
        category: item.category,
        diet: item.diet,
        quantity: qty
      });
    }

    this.saveCart(cart);
    this.showToast(`Added ${item.name} to cart`);
  },

  updateQuantity(itemId, delta) {
    let cart = this.getCart();
    const item = cart.find(ci => ci.id === itemId);
    if (!item) return;

    item.quantity = (Number(item.quantity) || 0) + Number(delta);
    if (item.quantity <= 0) {
      cart = cart.filter(ci => ci.id !== itemId);
    }

    this.saveCart(cart);
  },

  removeFromCart(itemId) {
    let cart = this.getCart();
    cart = cart.filter(ci => ci.id !== itemId);
    this.saveCart(cart);
    this.showToast('Item removed from cart');
  },

  clearCart() {
    localStorage.removeItem(this.STORAGE_KEY);
    this.dispatchUpdate();
  },

  getCartCount() {
    const cart = this.getCart();
    return cart.reduce((sum, item) => sum + (Number(item.quantity) || 0), 0);
  },

  getCartTotal() {
    const cart = this.getCart();
    const rawTotal = cart.reduce((sum, item) => {
      const price = Number(item.price) || 0;
      const qty = Number(item.quantity) || 0;
      return sum + price * qty;
    }, 0);
    return Math.round(rawTotal * 100) / 100;
  },

  formatPrice(price) {
    return '$' + Number(price).toFixed(2);
  },

  dispatchUpdate() {
    const count = this.getCartCount();
    const total = this.getCartTotal();

    // Update badge in DOM if present
    document.querySelectorAll('.cart-badge').forEach(badge => {
      badge.textContent = count;
      badge.style.display = count > 0 ? 'inline-flex' : 'none';
    });

    window.dispatchEvent(new CustomEvent('cartUpdated', {
      detail: { count, total }
    }));
  },

  showToast(message) {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>☕</span><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(20px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2400);
  }
};

// Initialize badges on load
document.addEventListener('DOMContentLoaded', () => {
  Cart.dispatchUpdate();
});
