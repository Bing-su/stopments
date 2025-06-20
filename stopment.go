package stopment

import (
	"embed"
	"io/fs"
)

//go:embed src/stopments/static
var files embed.FS

// Static is a io/fs directory containing static files for the Stopments application.
// It contains following files:
//
// - favicon.ico
// - styles.min.css
// - web-components.min.js
// - scalar-api-reference.js
var Static, _ = fs.Sub(files, "src/stopments/static")

var Favicon, _ = files.ReadFile("src/stopments/static/favicon.ico")
var Styles, _ = files.ReadFile("src/stopments/static/styles.min.css")
var WebComponents, _ = files.ReadFile("src/stopments/static/web-components.min.js")
var ScalarApiReference, _ = files.ReadFile("src/stopments/static/scalar-api-reference.js")
