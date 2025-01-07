/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        pixeloid: ['Pixeloid', 'sans-serif'],
      }
    },
  },
  plugins: [],
  darkMode: 'class',
}