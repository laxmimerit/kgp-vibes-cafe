import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-surface-container-low border-t border-outline-variant/30 pt-16 pb-24 lg:pb-16 text-on-surface-variant">
      <div className="max-w-[1280px] mx-auto px-gutter-desktop">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {/* Brand Info */}
          <div>
            <div className="flex items-center gap-space-md mb-4">
              <div className="w-9 h-9 rounded-xl bg-primary flex items-center justify-center text-on-primary shadow-sm text-lg font-bold">
                ☕
              </div>
              <div className="flex flex-col">
                <span className="font-headline-sm text-lg text-on-surface leading-tight font-semibold">KGP Vibes Cafe</span>
                <span className="font-label-sm text-xs text-secondary">Where code meets chai</span>
              </div>
            </div>
            <p className="font-body-sm text-sm text-on-surface-variant/90 leading-relaxed">
              Your neighborhood workspace cafe in Bengaluru, offering specialty chai, artisan coffee, and wholesome cafe favorites.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-headline-sm text-base text-on-surface font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 font-body-sm text-sm">
              <li><Link href="/" className="hover:text-primary transition-colors">Home</Link></li>
              <li><Link href="/about" className="hover:text-primary transition-colors">About Us</Link></li>
              <li><Link href="/menu" className="hover:text-primary transition-colors">Our Menu</Link></li>
              <li><Link href="/cart" className="hover:text-primary transition-colors">Order Ahead</Link></li>
            </ul>
          </div>

          {/* Outlets */}
          <div>
            <h4 className="font-headline-sm text-base text-on-surface font-semibold mb-4">Our Outlets</h4>
            <ul className="space-y-3 font-body-sm text-sm">
              <li>
                <p className="font-semibold text-on-surface">Koramangala</p>
                <p className="text-xs text-on-surface-variant">No. 27, 6th Cross, Koramangala 5th Block, Bengaluru</p>
              </li>
              <li>
                <p className="font-semibold text-on-surface">Indiranagar</p>
                <p className="text-xs text-on-surface-variant">100 Feet Road, Indiranagar, Bengaluru</p>
              </li>
            </ul>
          </div>

          {/* Hours & Notice */}
          <div>
            <h4 className="font-headline-sm text-base text-on-surface font-semibold mb-4">Opening Hours</h4>
            <p className="font-body-sm text-sm text-on-surface mb-2 font-medium">Open Daily: 8:00 AM – 10:00 PM</p>
            <p className="font-body-sm text-xs text-secondary leading-relaxed">
              Order online for seamless pickup at our counter without waiting in line.
            </p>
          </div>
        </div>

        <div className="pt-8 border-t border-outline-variant/20 flex flex-col sm:flex-row items-center justify-between gap-4 font-body-sm text-xs text-on-surface-variant/70">
          <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-4 text-center sm:text-left">
            <p>KGP Vibes Cafe. All rights reserved.</p>
            <span className="hidden sm:inline text-outline-variant/50">•</span>
            <p>Demo cafe made for a course</p>
          </div>
          <div className="flex gap-4">
            <Link href="/about" className="hover:text-primary transition-colors">About</Link>
            <Link href="/menu" className="hover:text-primary transition-colors">Menu</Link>
            <Link href="/cart" className="hover:text-primary transition-colors">Cart</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
