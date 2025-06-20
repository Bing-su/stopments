package stopments

import (
	"io/fs"
	"strings"
	"testing"
)

func TestStaticFS(t *testing.T) {
	entries, err := fs.ReadDir(Static, ".")
	if err != nil {
		t.Fatalf("failed to read static dir: %v", err)
	}
	files := map[string]bool{}
	for _, entry := range entries {
		files[entry.Name()] = true
	}
	for _, name := range []string{"favicon.ico", "styles.min.css", "web-components.min.js", "scalar-api-reference.js"} {
		if !files[name] {
			t.Errorf("missing static file: %s", name)
		}
	}
}

func TestStaticFilesContent(t *testing.T) {
	if len(Favicon) == 0 {
		t.Error("Favicon is empty")
	}
	if len(Styles) == 0 {
		t.Error("Styles is empty")
	}
	if len(WebComponents) == 0 {
		t.Error("WebComponents is empty")
	}
	if len(ScalarApiReference) == 0 {
		t.Error("ScalarApiReference is empty")
	}
}

func TestGetStoplightElementsHtml_Default(t *testing.T) {
	cfg := NewConfig("https://example.com/openapi.yaml", "Test API")
	html, err := GetStoplightElementsHtml(cfg)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !strings.Contains(html, "Test API") {
		t.Error("title not rendered in HTML")
	}
	if !strings.Contains(html, cfg.OpenAPIURL) {
		t.Error("openapi url not rendered in HTML")
	}
	if !strings.Contains(html, cfg.StoplightElementsJSURL) {
		t.Error("JS URL not rendered in HTML")
	}
	if !strings.Contains(html, cfg.StoplightElementsCSSURL) {
		t.Error("CSS URL not rendered in HTML")
	}
	if !strings.Contains(html, cfg.StoplightElementsFavicon) {
		t.Error("favicon not rendered in HTML")
	}
	if !strings.Contains(html, `tryItCredentialPolicy="omit"`) {
		t.Error("tryItCredentialPolicy not rendered in HTML")
	}
	if !strings.Contains(html, `layout="sidebar"`) {
		t.Error("layout not rendered in HTML")
	}
	if !strings.Contains(html, `router="hash"`) {
		t.Error("router not rendered in HTML")
	}
}

func TestGetStoplightElementsHtml_AllOptions(t *testing.T) {
	cfg := StoplightConfig{
		OpenAPIURL:               "https://api.com/openapi.json",
		Title:                    "All Options API",
		StoplightElementsJSURL:   "/static/web-components.min.js",
		StoplightElementsCSSURL:  "/static/styles.min.css",
		StoplightElementsFavicon: "/static/favicon.ico",
		APIDescriptionDocument:   "{openapi:3}",
		BasePath:                 "/docs",
		HideInternal:             true,
		HideTryIt:                true,
		HideExport:               true,
		TryItCORSProxy:           "https://proxy.com",
		TryItCredentialPolicy:    "include",
		Layout:                   "responsive",
		Logo:                     "/static/logo.png",
		Router:                   "history",
	}
	html, err := GetStoplightElementsHtml(cfg)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	checks := []string{
		cfg.Title,
		cfg.OpenAPIURL,
		cfg.StoplightElementsJSURL,
		cfg.StoplightElementsCSSURL,
		cfg.StoplightElementsFavicon,
		cfg.APIDescriptionDocument,
		cfg.BasePath,
		cfg.TryItCORSProxy,
		cfg.TryItCredentialPolicy,
		cfg.Layout,
		cfg.Logo,
		cfg.Router,
		"hideInternal=\"true\"",
		"hideTryIt=\"true\"",
		"hideExport=\"true\"",
	}
	for _, s := range checks {
		if !strings.Contains(html, s) {
			t.Errorf("expected %q in HTML", s)
		}
	}
}
