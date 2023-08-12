/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		"../app/templates/**/*.html",
		"../app/templates/*.html",
		"../app/templates/**/*.html.j2",
		"../app/templates/*.html.j2",
	],
	theme: {
		extend: {},
	},
	plugins: [],
};
