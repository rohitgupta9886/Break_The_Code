/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  compress: true,
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  httpAgentOptions: {
    keepAlive: true,
  },
  async headers() {
    return [
      {
        source: '/_next/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/images/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
  async rewrites() {
    const backendHost = process.env.INTERNAL_API_HOST || 'http://127.0.0.1:8000';
    return [
      {
        source: '/api/:path*',
        destination: `${backendHost}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
