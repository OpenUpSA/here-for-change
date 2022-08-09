/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors:{
        "hfc-green":{
          100: "#5b8d8a",
          800: "#303e3e",
          900: "#192827"
        }
      },
      spacing:{
        "1280": "1280px"
      }
    },
  },
  plugins: [],
}
