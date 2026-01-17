import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  typescript: {
    ignoreBuildErrors: false,
  },
  // Add smooth page transitions
  experimental: {
    optimizeCss: true,
    optimizePackageImports: ['lucide-react', 'react-markdown'],
  },
};

export default nextConfig;
