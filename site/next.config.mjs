/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      { source: '/index.html', destination: '/' },
      { source: '/menu.html', destination: '/menu' },
      { source: '/cart.html', destination: '/cart' },
      { source: '/checkout.html', destination: '/cart' },
      { source: '/confirmation.html', destination: '/confirmation' },
      { source: '/about.html', destination: '/about' },
    ];
  },
};

export default nextConfig;
