module.exports = {
  darkMode:'class',
  content: [
    './templates/**/*.html',
    './octopusDash/templates/**/*.{html,py}',    // App template files
    './octopusDash/static/js/**/*.js', 
    './octopusDash/**/*.py',     // App JavaScript files
    './octopusDash/static/css/**/*.css',    // App CSS files (Tailwind input file)
    './index.html',
  ],
  theme: {
    extend: {
    },
  },
  plugins: [],
}
