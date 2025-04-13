/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
            {
                source: "/api/:path*",
                destination:
                  process.env.NODE_ENV === "development"
                    ? "http://127.0.0.1:8000/api/:path*"
                    : "https://ski-sage-summit.vercel.app/api/:path*",
              },
        ];
    },
};

export default nextConfig;
