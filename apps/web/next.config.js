/** @type {import('next').NextConfig} */

const { version } = require("./package.json");

const remotePatterns = [
    {
        protocol: "https",
        hostname: "**",
    },
];

const nextConfig = {
    output: "standalone",
    env: {
        version,
    },
    reactStrictMode: false,
    typescript: {},
    images: {
        remotePatterns,
    },
    transpilePackages: [
        "@courselit/page-blocks",
        "@courselit/components-library",
        "@courselit/i18n",
    ],
    serverExternalPackages: ["pug", "liquidjs", "mongoose", "mongodb"],
    experimental: {},
};

module.exports = nextConfig;
