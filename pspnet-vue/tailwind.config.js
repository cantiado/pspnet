/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./public/**/*.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'soil': '#663300ff',
        'inputColor': '#aaa'
      }
    },
  },
  plugins: [],
}
