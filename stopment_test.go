package stopment

import (
	"io/fs"
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
