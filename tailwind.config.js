/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        safe: '#10b981',
        adjust: '#f59e0b',
        toxic: '#ef4444',
        ineffective: '#dc2626',
        unknown: '#6b7280',
      },
    },
  },
  plugins: [],
}
