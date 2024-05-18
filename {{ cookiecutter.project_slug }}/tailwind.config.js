module.exports = {
  content: [
    './frontend/templates/**/*.html',
    './**/*.py',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
};
