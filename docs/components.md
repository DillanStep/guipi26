# Components

Every control accepts an optional `tab="key"` argument that scopes it to a sidebar entry. Controls with no `tab` always render.

## Window

```python
app = create_window("My App", 1200, 760)
```

| Method | Description |
| --- | --- |
| `app.mainloop()` | Run the message loop until the window closes. |
| `app.destroy()` | Close the window from code. |
| `app.invalidate()` | Force a repaint (call this after mutating control attributes). |
| `app.client_size()` | `(width, height)` of the client area. |
| `app.content_origin_x(padding=24)` | First X to use for content (right of the sidebar). |
| `app.on_layout(callback)` | Register a `(width, height)` callback for responsive layout. |
| `app.set_card_collision_safety(enabled, card=None)` | Toggle [card overlap protection](collision-safety.md). |

## Label

```python
create_label(app, "Hello", x=40, y=40, width=400, height=40, style="title")
```

`style` is one of `"title"`, `"subtitle"`, or `"body"`.

## Button

```python
create_button(app, "Save", on_save, x=40, y=120, width=140, height=40,
              accent="#0d6efd")
```

The second positional argument is a callback. Pass `accent=...` for a filled button or `background=` / `border=` for a flat one.

## Sidebar (collapsible nav bar)

```python
create_collapsible_nav_bar(
    app, "MyApp",
    [
        {"key": "home", "title": "Home", "subtitle": "Start here"},
        {"key": "stats", "title": "Stats"},
    ],
    width=240, collapsed_width=72, selected_key="home",
)
```

Renders flush to the left edge as full-height app chrome. Click the toggle in the corner to collapse it.

## Page header (nav bar)

```python
create_nav_bar(
    app, "This week", x=cx, y=130, width=cw,
    subtitle="Snapshot of the last 7 days.",
    actions=[{"text": "Share"}, {"text": "Publish", "accent": True}],
    tab="home",
)
```

Use one per page. Pass `accent=True` on an action to render it as the primary button.

## Card

```python
create_card(app, "Sessions", "24", x=cx, y=200, width=240, height=110,
            subtitle="up 12%", accent="#0d6efd", tab="home")
```

Cards refuse to overlap by default — see [collision safety](collision-safety.md).

## Panel

```python
create_panel(app, "Notes", x=cx, y=200, width=320, height=200,
             subtitle="Drop quick reminders here.", accent="#6f42c1", tab="home")
```

A surface for grouping content. Add controls inside it by positioning them within its bounds.

## Grid (data table)

```python
create_grid(
    app,
    ["Name", "Email", "City"],
    [
        ["Ada", "ada@x.dev", "London"],
        ["Alan", "alan@x.uk", "Manchester"],
    ],
    x=cx, y=200, width=600, row_height=38, tab="home",
)
```

A simple table with a header row.

## Chart (bar)

```python
create_chart(
    app, "Frame budget (ms)",
    [("Idle", 16), ("Layout", 10), ("Paint", 12), ("Input", 7)],
    x=cx, y=200, width=400, height=280, accent="#0d6efd", tab="home",
)
```

Vertical bar chart. Each point is `(label, value)`.

## Layout helpers

```python
row = create_horizontal_grid(x=cx, y=200, total_width=cw, count=3, height=120, gap=16)
col = create_vertical_grid(x=cx, y=200, width=240, count=3, height=110, gap=12)

cell = row.cells[0]      # LayoutCell with .x, .y, .width, .height
```

Use these to lay out cards/panels without hand-computing offsets. See [layout](layout.md) for a full responsive example.
