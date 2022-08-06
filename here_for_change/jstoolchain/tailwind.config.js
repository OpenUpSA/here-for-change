/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors:{
        "hfc-green":{
          800: "#303e3e",
          900: "#192827"
        }
      }
    },
  },
  plugins: [],
}
