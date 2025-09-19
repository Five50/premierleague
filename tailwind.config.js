/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/*.py',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      fontFamily: {
        'heading': ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        'body': ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        'inter': ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      colors: {
        // Premier League team colors
        arsenal: '#EF0107',
        chelsea: '#034694',
        liverpool: '#C8102E',
        city: '#6CABDD',
        united: '#DA020E',
        tottenham: '#132257',
      },
      letterSpacing: {
        'heading': '-0.025em',
      },
    },
  },
  plugins: [],
}