package docslib

import (
	"os"
	"testing"
)

func TestDefaultConfig(t *testing.T) {
	cfg := DefaultConfig()

	if cfg.Version != "0.1.0" {
		t.Errorf("DefaultConfig().Version = %q, want %q", cfg.Version, "0.1.0")
	}
	if cfg.MaxWidth != "800px" {
		t.Errorf("DefaultConfig().MaxWidth = %q, want %q", cfg.MaxWidth, "800px")
	}
	if cfg.FontFamily != "sans-serif" {
		t.Errorf("DefaultConfig().FontFamily = %q, want %q", cfg.FontFamily, "sans-serif")
	}
	if cfg.BgColor != "#f4f4f4" {
		t.Errorf("DefaultConfig().BgColor = %q, want %q", cfg.BgColor, "#f4f4f4")
	}
	if cfg.CodeBgColor != "#f4f4f4" {
		t.Errorf("DefaultConfig().CodeBgColor = %q, want %q", cfg.CodeBgColor, "#f4f4f4")
	}
	if cfg.Padding != "20px" {
		t.Errorf("DefaultConfig().Padding = %q, want %q", cfg.Padding, "20px")
	}
	if cfg.Template != "" {
		t.Errorf("DefaultConfig().Template = %q, want empty", cfg.Template)
	}
}

func TestConfigFromEnv(t *testing.T) {
	// Set env vars for the test
	os.Setenv("DOCSLIB_VERSION", "1.2.3")
	os.Setenv("DOCSLIB_MAX_WIDTH", "1024px")
	os.Setenv("DOCSLIB_FONT_FAMILY", "serif")
	os.Setenv("DOCSLIB_BG_COLOR", "#ffffff")
	os.Setenv("DOCSLIB_CODE_BG_COLOR", "#eeeeee")
	os.Setenv("DOCSLIB_PADDING", "40px")
	os.Setenv("DOCSLIB_TEMPLATE", "<html>{{.Content}}</html>")
	defer func() {
		os.Unsetenv("DOCSLIB_VERSION")
		os.Unsetenv("DOCSLIB_MAX_WIDTH")
		os.Unsetenv("DOCSLIB_FONT_FAMILY")
		os.Unsetenv("DOCSLIB_BG_COLOR")
		os.Unsetenv("DOCSLIB_CODE_BG_COLOR")
		os.Unsetenv("DOCSLIB_PADDING")
		os.Unsetenv("DOCSLIB_TEMPLATE")
	}()

	cfg := ConfigFromEnv()

	if cfg.Version != "1.2.3" {
		t.Errorf("ConfigFromEnv().Version = %q, want %q", cfg.Version, "1.2.3")
	}
	if cfg.MaxWidth != "1024px" {
		t.Errorf("ConfigFromEnv().MaxWidth = %q, want %q", cfg.MaxWidth, "1024px")
	}
	if cfg.FontFamily != "serif" {
		t.Errorf("ConfigFromEnv().FontFamily = %q, want %q", cfg.FontFamily, "serif")
	}
	if cfg.BgColor != "#ffffff" {
		t.Errorf("ConfigFromEnv().BgColor = %q, want %q", cfg.BgColor, "#ffffff")
	}
	if cfg.CodeBgColor != "#eeeeee" {
		t.Errorf("ConfigFromEnv().CodeBgColor = %q, want %q", cfg.CodeBgColor, "#eeeeee")
	}
	if cfg.Padding != "40px" {
		t.Errorf("ConfigFromEnv().Padding = %q, want %q", cfg.Padding, "40px")
	}
	if cfg.Template != "<html>{{.Content}}</html>" {
		t.Errorf("ConfigFromEnv().Template = %q, want %q", cfg.Template, "<html>{{.Content}}</html>")
	}
}

func TestConfigFromEnv_DefaultsWhenUnset(t *testing.T) {
	// Ensure relevant env vars are unset
	os.Unsetenv("DOCSLIB_VERSION")
	os.Unsetenv("DOCSLIB_MAX_WIDTH")
	os.Unsetenv("DOCSLIB_TEMPLATE")

	cfg := ConfigFromEnv()

	// Should have default values when env is not set
	if cfg.Version != "0.1.0" {
		t.Errorf("ConfigFromEnv() with no env: Version = %q, want %q", cfg.Version, "0.1.0")
	}
	if cfg.MaxWidth != "800px" {
		t.Errorf("ConfigFromEnv() with no env: MaxWidth = %q, want %q", cfg.MaxWidth, "800px")
	}
	if cfg.Template != "" {
		t.Errorf("ConfigFromEnv() with no env: Template = %q, want empty", cfg.Template)
	}
}

func TestNewHTMLRendererWithConfig(t *testing.T) {
	cfg := Config{
		Version:     "9.9.9",
		MaxWidth:    "960px",
		FontFamily:  "monospace",
		BgColor:     "#000000",
		CodeBgColor: "#222222",
		Padding:     "10px",
		Template:    "",
	}

	r := NewHTMLRendererWithConfig(cfg)
	if r == nil {
		t.Fatal("NewHTMLRendererWithConfig() returned nil")
	}
	if r.Config.Version != "9.9.9" {
		t.Errorf("HTMLRenderer.Config.Version = %q, want %q", r.Config.Version, "9.9.9")
	}

	// Template should contain the custom MaxWidth and FontFamily
	if !contains(r.Template, "960px") {
		t.Error("HTMLRenderer.Template missing custom MaxWidth")
	}
	if !contains(r.Template, "monospace") {
		t.Error("HTMLRenderer.Template missing custom FontFamily")
	}
}

func TestNewHTMLRendererWithConfig_CustomTemplate(t *testing.T) {
	cfg := Config{
		Template: "<custom>{{.Content}}</custom>",
	}

	r := NewHTMLRendererWithConfig(cfg)
	if r.Template != "<custom>{{.Content}}</custom>" {
		t.Errorf("HTMLRenderer.Template with custom template = %q, want %q",
			r.Template, "<custom>{{.Content}}</custom>")
	}
}

func TestConfigFromEnv_PartialOverride(t *testing.T) {
	// Only set one env var — others should retain defaults
	os.Setenv("DOCSLIB_MAX_WIDTH", "1200px")
	defer os.Unsetenv("DOCSLIB_MAX_WIDTH")

	cfg := ConfigFromEnv()
	if cfg.MaxWidth != "1200px" {
		t.Errorf("MaxWidth = %q, want %q", cfg.MaxWidth, "1200px")
	}
	if cfg.FontFamily != "sans-serif" {
		t.Errorf("FontFamily = %q, want %q (default)", cfg.FontFamily, "sans-serif")
	}
	if cfg.Version != "0.1.0" {
		t.Errorf("Version = %q, want %q (default)", cfg.Version, "0.1.0")
	}
}
