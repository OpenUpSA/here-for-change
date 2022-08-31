/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./here_for_change/**/*.{html,js}"],
  theme: {
    extend: {
      colors:{
        "hfc-green":{
          100: "#5b8d8a",
          500: "#556060",
          600: "#2f3b3b",
          700: "#253333",
          800: "#303e3e",
          900: "#192827",
          

        }
      },
      boxShadow:{
        "btm": "0 2px grey",
        "wide": "0 10px 13px 0 rgba(25, 40, 39, 0.2), 0 2px grey"
      },
      // borderWith:{
      //   "1": "1px"
      // }
    },
  },
  plugins: [],
}
