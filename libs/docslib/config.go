package docslib

import (
	"os"
)

// Config holds configuration for the docslib package.
// Values are loaded from environment variables with sensible defaults.
type Config struct {
	// Version is the library version (env: DOCSLIB_VERSION)
	Version string

	// Renderer settings
	MaxWidth    string // env: DOCSLIB_MAX_WIDTH
	FontFamily  string // env: DOCSLIB_FONT_FAMILY
	BgColor     string // env: DOCSLIB_BG_COLOR
	CodeBgColor string // env: DOCSLIB_CODE_BG_COLOR
	Padding     string // env: DOCSLIB_PADDING

	// Template override; if non-empty it replaces the generated style template
	// (env: DOCSLIB_TEMPLATE)
	Template string
}

// DefaultConfig returns a Config with factory defaults.
func DefaultConfig() Config {
	return Config{
		Version:     "0.1.0",
		MaxWidth:    "800px",
		FontFamily:  "sans-serif",
		BgColor:     "#f4f4f4",
		CodeBgColor: "#f4f4f4",
		Padding:     "20px",
		Template:    "",
	}
}

// ConfigFromEnv loads configuration from environment variables.
// Environment variables take precedence over defaults.
func ConfigFromEnv() Config {
	cfg := DefaultConfig()

	if v := os.Getenv("DOCSLIB_VERSION"); v != "" {
		cfg.Version = v
	}
	if v := os.Getenv("DOCSLIB_MAX_WIDTH"); v != "" {
		cfg.MaxWidth = v
	}
	if v := os.Getenv("DOCSLIB_FONT_FAMILY"); v != "" {
		cfg.FontFamily = v
	}
	if v := os.Getenv("DOCSLIB_BG_COLOR"); v != "" {
		cfg.BgColor = v
	}
	if v := os.Getenv("DOCSLIB_CODE_BG_COLOR"); v != "" {
		cfg.CodeBgColor = v
	}
	if v := os.Getenv("DOCSLIB_PADDING"); v != "" {
		cfg.Padding = v
	}
	if v := os.Getenv("DOCSLIB_TEMPLATE"); v != "" {
		cfg.Template = v
	}

	return cfg
}

// Version is the current version of the library.
// Initialised from DefaultConfig; can be overridden via DOCSLIB_VERSION.
var Version = DefaultConfig().Version
