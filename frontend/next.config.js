/** @type {import('next').NextConfig} */
const BACKEND_URL = process.env.BACKEND_URL || 'http://dclaw-trademark-backend:8066'

const nextConfig = {
  output: 'standalone',
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      { source: '/api/:path*', destination: `${BACKEND_URL}/api/:path*` },
      { source: '/health/:path*', destination: `${BACKEND_URL}/health/:path*` },
    ]
  },
}

module.exports = nextConfig
