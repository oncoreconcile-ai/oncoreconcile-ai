/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#028090",
        "primary-dark": "#075f6c",
        "primary-light": "#c8e8e8",
        danger: "#cf222e",
        warning: "#9a6700",
        success: "#1a7f37",
        surface: "#f7f9fb",
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
