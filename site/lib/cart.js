/**
 * cart.js
 * Persistent shopping cart management using localStorage.
 * Compatible with existing kgp_cart schema and event dispatches.
 */

const STORAGE_KEY = 'kgp_cart';

export const Cart = {
  STORAGE_KEY,

  getCart() {
    if (typeof window === 'undefined') return [];
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error('Error reading cart from localStorage', e);
      return [];
    }
  },

  saveCart(cart) {
    if (typeof window === 'undefined') return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
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
    if (typeof window === 'undefined') return;
    localStorage.removeItem(STORAGE_KEY);
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
    return '$' + Number(price || 0).toFixed(2);
  },

  dispatchUpdate() {
    if (typeof window === 'undefined') return;
    const count = this.getCartCount();
    const total = this.getCartTotal();

    // Dispatch standard CustomEvent for React state listeners
    window.dispatchEvent(new CustomEvent('kgp_cart_updated', {
      detail: { count, total }
    }));
  },

  showToast(message) {
    if (typeof window === 'undefined') return;
    let toast = document.getElementById('cart-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'cart-toast';
      toast.className = 'fixed bottom-20 right-6 z-50 bg-secondary text-on-secondary px-4 py-3 rounded-xl shadow-lg border border-outline-variant/30 flex items-center gap-2 transform transition-all duration-300 pointer-events-none opacity-0 translate-y-2';
      document.body.appendChild(toast);
    }
    toast.innerHTML = `<span class="text-lg">🛒</span> <span class="font-label-md">${message}</span>`;
    toast.classList.remove('opacity-0', 'translate-y-2');
    toast.classList.add('opacity-100', 'translate-y-0');

    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => {
      toast.classList.remove('opacity-100', 'translate-y-0');
      toast.classList.add('opacity-0', 'translate-y-2');
    }, 2200);
  }
};

// Also attach to window.Cart for any legacy script or test expectations
if (typeof window !== 'undefined') {
  window.Cart = Cart;
}

export default Cart;
