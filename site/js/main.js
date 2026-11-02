/**
 * main.js
 * Global behaviors: mobile navigation toggle, active link highlights,
 * and dynamic cart badge updates across all pages.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Toggle
  const menuToggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');

  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const isOpen = navLinks.classList.contains('open');
      menuToggle.setAttribute('aria-expanded', isOpen);
    });

    document.addEventListener('click', (e) => {
      if (!navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
        navLinks.classList.remove('open');
      }
    });
  }

  // Active Link Highlight
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const navItems = document.querySelectorAll('.nav-link');
  navItems.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // Dynamic Cart Badge Updates
  function updateCartBadges() {
    if (typeof Cart !== 'undefined' && Cart.getCartCount) {
      const count = Cart.getCartCount();
      document.querySelectorAll('.cart-badge').forEach(badge => {
        badge.textContent = count;
      });
    }
  }

  updateCartBadges();
  window.addEventListener('cartUpdated', updateCartBadges);
});
