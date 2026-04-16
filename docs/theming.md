# Theming

Colors are set per window via `set_theme(...)`:

```python
from guipi26 import create_window, set_theme

app = create_window("Themed", 1000, 600)
set_theme(
    app,
    background="#f5f6f8",
    surface="#ffffff",
    accent="#0d6efd",
    text_primary="#1f1f1f",
    text_secondary="#616161",
)
```

| Argument | Default | What it controls |
| --- | --- | --- |
| `background` | `#f3f3f3` | Window body color (behind the content panel). |
| `surface` | `#ffffff` | Panels, cards, grids, page header. |
| `accent` | `#005fb8` | Primary buttons, active sidebar item, indicators. |
| `text_primary` | `#1f1f1f` | Headings, button text, card values. |
| `text_secondary` | `#616161` | Subtitles, muted labels, table headers. |

Other theme colors (`surface_alt`, `border`, `button_face`, etc.) are derived automatically from the values above so the window stays internally consistent.

## Per-control accents

Most controls accept their own `accent=...` so you can highlight individual cards, panels, or charts without changing the global theme:

```python
create_card(app, "Errors", "3", x=cx, y=200, width=240, height=110,
            subtitle="last hour", accent="#dc3545", tab="home")
```

Buttons accept `accent=...` for the filled style, or `background=` / `border=` for a flat secondary style:

```python
create_button(app, "Primary",   x=cx, y=300, width=140, height=40, accent="#0d6efd")
create_button(app, "Secondary", x=cx + 156, y=300, width=140, height=40,
              background="#ffffff", border="#dee2e6")
```

## Sidebar colors

The sidebar uses a fixed dark palette (`#212529` background, light text) so it always reads as window chrome. Its accent for the active item still uses your theme's `accent` color.

## Typography

Text uses Segoe UI variants by role:

- `title` — Segoe UI Semibold, large
- `subtitle` — Segoe UI, medium
- `body` — Segoe UI, base
- `caption` — Segoe UI, small

Pass `style=` to `create_label(...)` to choose. There is no API for swapping the font family right now; everything goes through Segoe UI for a consistent Windows look.
