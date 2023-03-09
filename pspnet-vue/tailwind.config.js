/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./public/**/*.html',
  './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'soil': '#663300ff',
        'inputColor': '#aaa',
        'tortilla': '#9a7b4f',
        'brown': '#231709',
        'pecan': '#4a2511',
        'plant': '#b9e0a5ff'
      }
    },
  },
  plugins: [],
}
