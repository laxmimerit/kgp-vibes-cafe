import './globals.css';
import Header from '../components/Header';
import Footer from '../components/Footer';
import MobileNav from '../components/MobileNav';

export const metadata = {
  title: 'KGP Vibes Cafe - Where Code Meets Chai',
  description: 'Artisanal chai, specialty coffee, and cafe favorites in Koramangala and Indiranagar.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Literata:ital,opsz,wght@0,7..72,400..700;1,7..72,400..700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
          rel="stylesheet"
        />
      </head>
      <body className="bg-background text-on-surface antialiased flex flex-col min-h-screen">
        <Header />
        <main className="flex-1 pt-20 pb-16 lg:pb-0">{children}</main>
        <Footer />
        <MobileNav />
      </body>
    </html>
  );
}
