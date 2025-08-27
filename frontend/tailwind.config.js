/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#FFE5EC',
          100: '#FFB8D0',
          200: '#FF8AB4',
          300: '#FF5C98',
          400: '#FF2E79', // Neon pink
          500: '#E5005E',
          600: '#B3004A',
          700: '#800035',
          800: '#98002E', // Dark red range
          900: '#7A001C', // Dark red range
        },
        dark: {
          100: '#2D1B21',
          200: '#24151A',
          300: '#1B0F13',
          400: '#12090C',
          500: '#090406',
        }
      },
      animation: {
        'pixel-bounce': 'pixel-bounce 0.3s ease-in-out',
        'scanline': 'scanline 2s linear infinite',
      },
      keyframes: {
        'pixel-bounce': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
        'scanline': {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        }
      }
    },
  },
  plugins: [],
}