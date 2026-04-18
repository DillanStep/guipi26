# API reference

Every public symbol exported from `guipi26`.

## `create_window(title, width, height) -> Window`

Create the host window.

```python
app = create_window("My App", 1200, 760)
```

## `set_theme(app, *, background, surface, accent, text_primary, text_secondary) -> Window`

Set the window's color theme. All arguments are optional and have sensible defaults. Returns the window so calls can be chained.

## `create_label(app, text, *, x, y, width, height, color=None, style="body", tab=None)`

`style` is `"title"`, `"subtitle"`, or `"body"`. Pass `color="#hex"` to override the default color for the chosen style.

## `create_button(app, text, command=None, *, x, y, width, height, background=None, foreground=None, border=None, accent=None, tab=None)`

`command` is a zero-argument callback fired on click. Pass `accent="#hex"` for a filled button, or `background=` / `border=` for a flat one.

## `create_collapsible_nav_bar(app, title, items, *, width=240, collapsed_width=72, selected_key=None)`

The Bootstrap-style sidebar.

`items` is a list of dicts:

```python
[{"key": "home", "title": "Home", "subtitle": "Start here"}, ...]
```

`subtitle` is optional. The returned object has a mutable `.selected_key` and `.collapsed`.

## `create_nav_bar(app, title, *, x, y, width, height=54, subtitle=None, actions=None, tab=None)`

Page header. `actions` is a list of dicts: `[{"text": "Save", "accent": True}, ...]`.

## `create_panel(app, title, *, x, y, width, height, subtitle=None, accent=None, tab=None)`

A grouped surface.

## `create_card(app, title, value, *, x, y, width, height, subtitle=None, accent=None, tab=None, collision_safety=True)`

A card with a title, big value, and optional subtitle. See [collision safety](collision-safety.md) for the overlap behavior.

## `create_grid(app, columns, rows, *, x, y, width, row_height=34, tab=None)`

`columns` is a list of strings. `rows` is a list of lists of strings (or any value with a sensible `str(...)` representation).

## `create_chart(app, title, points, *, x, y, width, height, accent=None, tab=None)`

`points` is a list of `(label, value)` tuples.

## `create_horizontal_grid(x, y, total_width, count, height, gap=16) -> HorizontalGrid`

Returns a layout helper with `.cells` — a list of `LayoutCell(x, y, width, height)`.

## `create_vertical_grid(x, y, width, count, height, gap=16) -> VerticalGrid`

Same idea but stacked vertically.

## `Window` methods

| Method | Description |
| --- | --- |
| `mainloop()` | Run the message loop. Blocks. |
| `destroy()` | Close the window. |
| `invalidate()` | Force a repaint. |
| `client_size() -> (w, h)` | Current client area size. |
| `content_origin_x(padding=24) -> int` | First X to use right of the sidebar. |
| `on_layout(callback)` | Register a `(w, h)` callback fired on resize. |
| `set_card_collision_safety(enabled, card=None)` | Toggle card overlap protection. |
| `set_theme(...)` | Same arguments as the top-level `set_theme(app, ...)`. |

## `__version__`

```python
import guipi26
print(guipi26.__version__)   # e.g. '0.1.0'
```
