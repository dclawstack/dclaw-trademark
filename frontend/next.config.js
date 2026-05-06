/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://dclaw-trademark-backend:8141/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
