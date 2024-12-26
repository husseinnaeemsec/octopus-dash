module.exports = {
  content: [
    './templates/**/*.html',               // Root templates
    './octopusDash/templates/**/*.html',    // App template files
    './octopusDash/static/js/**/*.js',      // App JavaScript files
    './octopusDash/static/css/**/*.css',    // App CSS files (Tailwind input file)
    './index.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
