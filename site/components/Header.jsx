'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Cart from '../lib/cart';

export default function Header() {
  const pathname = usePathname();
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    // Initial read
    setCartCount(Cart.getCartCount());

    const handleUpdate = (e) => {
      setCartCount(e.detail?.count ?? Cart.getCartCount());
    };

    window.addEventListener('kgp_cart_updated', handleUpdate);
    return () => window.removeEventListener('kgp_cart_updated', handleUpdate);
  }, []);

  const isActive = (path) => {
    if (path === '/') return pathname === '/' || pathname === '/index.html';
    return pathname.startsWith(path);
  };

  const navClass = (path) =>
    isActive(path)
      ? 'bg-secondary-container text-on-secondary-container font-label-md rounded-full shadow-sm'
      : 'text-on-surface-variant hover:text-on-surface';

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-surface/90 backdrop-blur-md shadow-[0_4px_20px_-4px_rgba(43,24,16,0.06)] border-b border-outline-variant/30">
      <div className="h-20 max-w-[1280px] mx-auto px-gutter-desktop flex items-center justify-between gap-space-md">
        <Link href="/" className="flex items-center gap-space-md shrink-0 cursor-pointer" aria-label="KGP Vibes Cafe Home">
          <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-on-primary shadow-sm text-xl font-bold">
            ☕
          </div>
          <div className="flex flex-col">
            <span className="font-headline-sm text-headline-sm text-on-surface leading-tight brand-title">KGP Vibes Cafe</span>
            <span className="font-label-sm text-label-sm text-secondary tracking-normal">Where code meets chai</span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden lg:flex items-center gap-space-xs bg-surface-container-low px-space-xs py-space-xs rounded-full shadow-[0_1px_4px_rgba(43,24,16,0.04)]">
          <Link href="/" className={`px-space-md py-space-xs transition-colors flex items-center gap-space-xs font-label-md ${navClass('/')}`}>
            Home
          </Link>
          <Link href="/about" className={`px-space-md py-space-xs transition-colors flex items-center gap-space-xs font-label-md rounded-full ${navClass('/about')}`}>
            About
          </Link>
          <Link href="/menu" className={`px-space-md py-space-xs rounded-full font-label-md transition-colors flex items-center gap-space-xs ${navClass('/menu')}`}>
            Menu
          </Link>
          <Link href="/specials" className={`px-space-md py-space-xs rounded-full font-label-md transition-colors flex items-center gap-space-xs ${navClass('/specials')}`}>
            Specials
          </Link>
          <Link href="/cart" className={`px-space-md py-space-xs rounded-full font-label-md transition-colors flex items-center gap-space-xs ${navClass('/cart')}`}>
            <span>Cart</span>
            <span
              className="cart-badge bg-primary text-on-primary text-[11px] font-bold px-2 py-0.5 rounded-full"
              style={{ display: cartCount > 0 ? 'inline-flex' : 'none' }}
            >
              {cartCount}
            </span>
          </Link>
        </nav>

        {/* Order Ahead Action Button */}
        <div className="hidden sm:flex items-center gap-space-sm">
          <Link
            href="/cart"
            className="bg-primary hover:bg-primary-container text-on-primary font-label-md text-label-md px-space-lg py-space-sm rounded-full shadow-sm transition-all duration-200 flex items-center gap-space-xs"
          >
            <span className="material-symbols-outlined text-lg">shopping_bag</span>
            <span>Order Ahead</span>
            <span
              className="cart-badge bg-on-primary text-primary text-[11px] font-bold px-2 py-0.5 rounded-full ml-1"
              style={{ display: cartCount > 0 ? 'inline-flex' : 'none' }}
            >
              {cartCount}
            </span>
          </Link>
        </div>
      </div>
    </header>
  );
}
