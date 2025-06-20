package stopments

import (
	"embed"
	"html/template"
	"io/fs"
	"strings"
)

//go:embed src/stopments/static
var files embed.FS

// Static is an io/fs directory containing static files for the Stopments application.
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

// StoplightConfig holds the configuration for Stoplight Elements.
// It allows you to customize the OpenAPI document URL, title, and other settings
// for the Stoplight Elements documentation.
// You can use NewConfig function to create a new StoplightConfig with default values.
// The configuration can be used to generate the HTML for Stoplight Elements using GetStoplightElementsHtml function.
type StoplightConfig struct {
	// OpenAPIURL is the URL to the OpenAPI document.
	// It can be a URL to a remote OpenAPI document or a local file path.
	OpenAPIURL string

	// Title is the title of the API documentation.
	Title string

	// StoplightElementsJSURL is the URL to the Stoplight Elements JavaScript file.
	// Default is "https://cdn.jsdelivr.net/npm/@stoplight/elements/web-components.min.js"
	StoplightElementsJSURL string

	// StoplightElementsCSSURL is the URL to the Stoplight Elements CSS file.
	// Default is "https://cdn.jsdelivr.net/npm/@stoplight/elements/styles.min.css"
	StoplightElementsCSSURL string

	// StoplightElementsFavicon is the URL to the favicon for Stoplight Elements.
	// Default is "https://docs.stoplight.io/favicons/favicon.ico"
	StoplightElementsFavicon string

	// APIDescriptionDocument is the API description document in JSON or YAML format.
	APIDescriptionDocument string

	// BasePath is the base path for the API.
	BasePath string

	// HideInternal indicates whether to hide internal APIs in the documentation.
	HideInternal bool

	// HideTryIt indicates whether to hide the "Try It" feature in the documentation.
	HideTryIt bool

	// HideExport indicates whether to hide the "Export" feature in the documentation.
	HideExport bool

	// TryItCORSProxy is the CORS proxy URL for the "Try It" feature.
	TryItCORSProxy string

	// TryItCredentialPolicy defines the credential policy for the "Try It" feature.
	// default is "omit".
	// Possible values are "omit", "include", and "same-origin".
	TryItCredentialPolicy string // "omit", "include", "same-origin"

	// Layout defines the layout of the Stoplight Elements documentation.
	// Default is "sidebar".
	// Possible values are "sidebar", "responsive", and "stacked".
	Layout string // "sidebar", "responsive", "stacked"

	// Logo is the URL to the logo for the API documentation.
	// It can be a URL to an image or a local file path.
	// Default is an empty string, which means no logo is displayed.
	Logo string

	// Router defines the routing strategy for Stoplight Elements.
	// Default is "hash".
	// Possible values are "history", "hash", "memory", and "static".
	Router string // "history", "hash", "memory", "static"
}

// NewConfig creates a new StoplightConfig with default values for Stoplight Elements.
func NewConfig(openapiURL string, title string) StoplightConfig {
	return StoplightConfig{
		OpenAPIURL:               openapiURL,
		Title:                    title,
		StoplightElementsJSURL:   "https://cdn.jsdelivr.net/npm/@stoplight/elements/web-components.min.js",
		StoplightElementsCSSURL:  "https://cdn.jsdelivr.net/npm/@stoplight/elements/styles.min.css",
		StoplightElementsFavicon: "https://docs.stoplight.io/favicons/favicon.ico",
		TryItCredentialPolicy:    "omit",
		Layout:                   "sidebar",
		Router:                   "hash",
	}
}

const stoplightElementsTemplate = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>{{.Title}}</title>
    {{if .StoplightElementsFavicon}}<link rel="shortcut icon" href="{{.StoplightElementsFavicon}}">{{end}}
    <script src="{{.StoplightElementsJSURL}}"></script>
    <link rel="stylesheet" href="{{.StoplightElementsCSSURL}}">
  </head>
<body>
  <elements-api
    {{if .OpenAPIURL}}apiDescriptionUrl="{{.OpenAPIURL}}"{{end}}
    {{if .APIDescriptionDocument}}apiDescriptionDocument="{{.APIDescriptionDocument}}"{{end}}
    {{if .BasePath}}basePath="{{.BasePath}}"{{end}}
    {{if .HideInternal}}hideInternal="true"{{end}}
    {{if .HideTryIt}}hideTryIt="true"{{end}}
    {{if .HideExport}}hideExport="true"{{end}}
    {{if .TryItCORSProxy}}tryItCorsProxy="{{.TryItCORSProxy}}"{{end}}
    tryItCredentialPolicy="{{.TryItCredentialPolicy}}"
    layout="{{.Layout}}"
    {{if .Logo}}logo="{{.Logo}}"{{end}}
    router="{{.Router}}"
  />
</body>
</html>`

// GetStoplightElementsHtml generates the HTML for Stoplight Elements based on the provided configuration.
// You can get config using NewConfig function.
// It returns the HTML as a string or an error if the template execution fails.
func GetStoplightElementsHtml(cfg StoplightConfig) (string, error) {
	tmpl, err := template.New("stoplight").Parse(stoplightElementsTemplate)
	if err != nil {
		return "", err
	}
	var builder strings.Builder

	err = tmpl.Execute(&builder, cfg)
	if err != nil {
		return "", err
	}
	return builder.String(), nil
}
