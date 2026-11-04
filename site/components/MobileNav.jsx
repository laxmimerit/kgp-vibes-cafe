'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Cart from '../lib/cart';

export default function MobileNav() {
  const pathname = usePathname();
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
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

  const linkClass = (path) =>
    isActive(path)
      ? 'text-primary font-bold'
      : 'text-on-surface-variant hover:text-on-surface';

  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-50 bg-surface/95 backdrop-blur-md border-t border-outline-variant/30 px-2 sm:px-space-md py-space-xs flex items-center justify-around shadow-[0_-4px_20px_rgba(43,24,16,0.06)] overflow-x-auto">
      <Link href="/" className={`flex flex-col items-center justify-center min-w-[44px] min-h-[44px] gap-0.5 transition-colors ${linkClass('/')}`}>
        <span className="material-symbols-outlined text-xl">home</span>
        <span className="font-label-sm text-[11px]">Home</span>
      </Link>
      <Link href="/menu" className={`flex flex-col items-center justify-center min-w-[44px] min-h-[44px] gap-0.5 transition-colors ${linkClass('/menu')}`}>
        <span className="material-symbols-outlined text-xl">restaurant_menu</span>
        <span className="font-label-sm text-[11px]">Menu</span>
      </Link>
      <Link href="/diet" className={`flex flex-col items-center justify-center min-w-[44px] min-h-[44px] gap-0.5 transition-colors ${linkClass('/diet')}`}>
        <span className="material-symbols-outlined text-xl">eco</span>
        <span className="font-label-sm text-[11px]">Diet</span>
      </Link>
      <Link href="/specials" className={`flex flex-col items-center justify-center min-w-[44px] min-h-[44px] gap-0.5 transition-colors ${linkClass('/specials')}`}>
        <span className="material-symbols-outlined text-xl">auto_awesome</span>
        <span className="font-label-sm text-[11px]">Specials</span>
      </Link>
      <Link href="/faq" className={`flex flex-col items-center justify-center min-w-[44px] min-h-[44px] gap-0.5 transition-colors ${linkClass('/faq')}`}>
        <span className="material-symbols-outlined text-xl">help</span>
        <span className="font-label-sm text-[11px]">FAQ</span>
      </Link>
      <Link href="/cart" className={`flex flex-col items-center justify-center min-w-[44px] min-h-[44px] gap-0.5 transition-colors relative ${linkClass('/cart')}`}>
        <span className="material-symbols-outlined text-xl">shopping_cart</span>
        <span className="font-label-sm text-[11px]">Cart</span>
        <span
          className="cart-badge absolute -top-1 right-1 bg-primary text-on-primary text-[10px] font-bold px-1.5 py-0.2 rounded-full min-w-[16px] text-center"
          style={{ display: cartCount > 0 ? 'inline-block' : 'none' }}
        >
          {cartCount}
        </span>
      </Link>
      <Link href="/about" className={`flex flex-col items-center justify-center min-w-[44px] min-h-[44px] gap-0.5 transition-colors ${linkClass('/about')}`}>
        <span className="material-symbols-outlined text-xl">info</span>
        <span className="font-label-sm text-[11px]">About</span>
      </Link>
    </nav>
  );
}
