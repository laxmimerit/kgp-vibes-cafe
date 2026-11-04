import Link from 'next/link';

export const metadata = {
  title: '404 - Page Not Found | KGP Vibes Cafe',
  description: 'Looks like this page stepped out for a chai break.',
};

export default function NotFound() {
  return (
    <div className="w-full min-h-[calc(100vh-16rem)] flex items-center justify-center px-gutter-desktop py-space-xl bg-background">
      <div className="w-full max-w-xl mx-auto bg-surface-container-lowest rounded-2xl border border-outline-variant/30 p-8 sm:p-12 shadow-sm text-center flex flex-col items-center">
        {/* Warm Coffee Cup Emoji */}
        <div className="w-16 h-16 rounded-2xl bg-secondary-container text-on-secondary-container flex items-center justify-center text-3xl shadow-sm mb-5">
          ☕
        </div>

        {/* Stylized Terminal Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container text-on-surface-variant font-label-sm text-label-sm mb-4 border border-outline-variant/40">
          <span className="w-2 h-2 rounded-full bg-primary" />
          <span>404: route_missing</span>
        </div>

        {/* Headline */}
        <h1 className="font-headline-lg text-headline-lg text-on-surface mb-3 tracking-tight">
          404 // Route Not Found
        </h1>

        {/* Short & Plain Message (Single sentence) */}
        <p className="font-body-md text-body-md text-on-surface-variant max-w-md mb-8 leading-relaxed">
          Looks like this page stepped out for a chai break.
        </p>

        {/* Primary & Secondary Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 w-full sm:w-auto mb-8">
          <Link
            href="/"
            className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3 rounded-full bg-primary hover:bg-primary-container text-on-primary font-label-md transition-colors shadow-sm"
          >
            Back to Home
          </Link>
          <Link
            href="/menu"
            className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3 rounded-full bg-secondary-container hover:bg-secondary-container/80 text-on-secondary-container font-label-md transition-colors"
          >
            Explore Menu
          </Link>
        </div>

        {/* Helpful Navigation Links */}
        <div className="pt-6 border-t border-outline-variant/20 w-full flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4 font-body-sm text-body-sm text-on-surface-variant">
          <span>Looking for something else?</span>
          <div className="flex items-center gap-3">
            <Link
              href="/diet"
              className="text-primary hover:underline font-label-md transition-colors"
            >
              Diet Guide
            </Link>
            <span className="text-outline-variant">·</span>
            <Link
              href="/faq"
              className="text-primary hover:underline font-label-md transition-colors"
            >
              FAQ
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
