# phenodocs Brand

**AI-CODED, not AI-generated.** The mark is hand-authored as a vector
[`logo.svg`](./logo.svg) (paths/shapes written by hand). No image-generation
model was used. Raster formats are exported deterministically from the SVG.

These assets live at the repo root (`assets/brand/`), **outside** the VitePress
`srcDir: 'docs'` scan path, so they do not affect the docs build.

## The mark

An **open book** of two facing pages (cyan left, indigo right) with text lines,
a red ribbon **bookmark**, and a gold **knowledge spark** rising from the spine
— a docs / book / knowledge mark on a dark rounded app tile.

## Files

| File | Purpose |
|------|---------|
| `logo.svg` | Source of truth (hand-coded vector) |
| `logo-{16,32,48,128,256,512}.png` | Raster sizes |
| `logo.png` | Canonical 512px PNG |
| `logo.jpg` | 512px, white matte |
| `app.ico` | Multi-resolution Windows icon (16/32/48/256) — feeds the Start-Menu / desktop shortcut |

## Regenerating

```powershell
pwsh tools/Export-Brand.ps1
```

Renderer preference matches the Civis pure-Rust SVG convention (RND-016):
**resvg** (canonical), falling back to `rsvg-convert` -> ImageMagick ->
Python/cairosvg+Pillow. ICO/JPG assembly uses ImageMagick when present, else Pillow.
