# Layout & responsiveness

GUIpi26 controls have plain `x`, `y`, `width`, and `height` attributes you can set at any time. Combined with `app.on_layout()`, this makes responsive layouts straightforward.

## `on_layout`

Register a callback that receives the live `(width, height)` of the client area:

```python
def layout(w, h):
    cx = app.content_origin_x(padding=32)
    cw = max(420, w - cx - 32)

    header.x = cx
    header.width = cw
    grid.x = cx
    grid.width = cw - 280

app.on_layout(layout)
```

The callback runs:

1. **Immediately** when registered (so initial positioning works).
2. On every Windows `WM_SIZE` event (so resizing reflows).

You can register multiple callbacks if you want to split layout responsibilities.

## `content_origin_x`

The sidebar sits flush to the left edge. Use `content_origin_x(padding=...)` to get the first X to the right of it. This automatically accounts for whether the sidebar is collapsed or not.

```python
cx = app.content_origin_x(padding=32)
```

## Layout helpers

For grids of equally-sized cells, use the helpers instead of computing offsets by hand:

```python
row = create_horizontal_grid(cx, 200, cw, count=3, height=120, gap=16)
left, mid, right = row.cells       # each has .x .y .width .height
```

```python
col = create_vertical_grid(cx, 200, 240, count=3, height=110, gap=12)
```

Recompute these inside `on_layout` so they re-flow with the window:

```python
def layout(w, h):
    cx = app.content_origin_x(32)
    cw = max(420, w - cx - 32)
    row = create_horizontal_grid(cx, 200, cw, 3, 120, gap=16)
    for card, cell in zip((card_a, card_b, card_c), row.cells):
        card.x = cell.x
        card.width = cell.width
```

## A complete responsive example

```python
from guipi26 import (
    create_window, create_collapsible_nav_bar,
    create_card, create_label,
)

app = create_window("Responsive", 1100, 700)

create_collapsible_nav_bar(
    app, "App",
    [{"key": "home", "title": "Home"}],
    selected_key="home",
)

title = create_label(app, "Home", x=0, y=32, width=420, height=40,
                     style="title", tab="home")
card = create_card(app, "Visits", "42", x=0, y=120, width=0, height=120,
                   tab="home")

def layout(w, h):
    cx = app.content_origin_x(padding=32)
    cw = max(280, w - cx - 32)
    title.x = cx
    title.width = cw
    card.x = cx
    card.width = cw

app.on_layout(layout)
app.mainloop()
```

Drag the window edge — the title and card stretch to fill the new client width.
