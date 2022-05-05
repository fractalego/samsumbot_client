
function capitalize_first_letter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

module.exports = {
	capitalizeFirstLetter: function (text) {
		return capitalize_first_letter(text);
	},
};