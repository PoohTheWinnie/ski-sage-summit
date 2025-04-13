/** @type {import('tailwindcss').Config} */
const { nextui } = require("@nextui-org/theme");

module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'alpine': {
          100: '#E6EEF2', // Light ice blue
          500: '#2C5D7C', // Mountain lake blue
          700: '#1B3B4B', // Deep glacier blue
          900: '#0F2634', // Night mountain blue
        }
      }
    },
  },
  plugins: [
    require('tailwind-scrollbar-hide')
  ],
}