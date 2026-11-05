/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Robots-Tag',
            value: 'noindex, nofollow',
          },
        ],
      },
    ];
  },
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
