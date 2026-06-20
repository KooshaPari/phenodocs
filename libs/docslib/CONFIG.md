# docslib Configuration

The `docslib` Go library uses environment variables for configuration.
All settings have sensible defaults; only override what you need.

## Configuration precedence

1. Environment variable (highest)
2. `Config` struct passed to `NewHTMLRendererWithConfig(cfg)`
3. `ConfigFromEnv()` / `DefaultConfig()` (lowest)

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `DOCSLIB_VERSION` | `0.1.0` | Library version string |
| `DOCSLIB_MAX_WIDTH` | `800px` | CSS `max-width` for the rendered HTML body |
| `DOCSLIB_FONT_FAMILY` | `sans-serif` | CSS `font-family` for the rendered HTML body |
| `DOCSLIB_BG_COLOR` | `#f4f4f4` | CSS `background` for `<pre>` and `<code>` blocks |
| `DOCSLIB_CODE_BG_COLOR` | `#f4f4f4` | CSS `background` for `<pre>` and `<code>` blocks |
| `DOCSLIB_PADDING` | `20px` | CSS `padding` for the rendered HTML body |
| `DOCSLIB_TEMPLATE` | *(empty)* | Full HTML template override. If set, all other style keys are ignored and this value is used verbatim as the template. The template should accept `{{.Title}}` and `{{.Content}}` placeholders. |

## Programmatic usage

```go
// Option A: Use environment variables
renderer := docslib.NewHTMLRenderer()

// Option B: Explicit configuration
cfg := docslib.Config{
    Version:    "2.0.0",
    MaxWidth:   "100%",
    FontFamily: "system-ui, sans-serif",
}
renderer = docslib.NewHTMLRendererWithConfig(cfg)

// Option C: Load from env then tweak
cfg = docslib.ConfigFromEnv()
cfg.MaxWidth = "1200px"
renderer = docslib.NewHTMLRendererWithConfig(cfg)
```

## Adding new config keys

1. Add the field to the `Config` struct in `config.go`
2. Set the default in `DefaultConfig()`
3. Add the env lookup in `ConfigFromEnv()`
4. Wire the value into `buildTemplate()` in `renderer.go`
5. Add a test case in `config_test.go`
6. Document in this file
