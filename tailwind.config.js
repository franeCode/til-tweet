/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.{html,js}',
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '!../../**/node_modules',
    '../../**/*.js',
    '../../**/*.py'
],
  theme: {
    extend: {
      padding: {
        'sm': '2rem',
      }
    },
  },
  plugins: [],
}

