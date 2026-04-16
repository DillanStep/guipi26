# Getting started

GUIpi26 is **Windows-only** and requires **Python 3.8+**. It has no runtime dependencies — everything is built on `ctypes` calls into Win32 and GDI.

## Install

```
pip install guipi26
```

For local development from a clone:

```
pip install -e .
```

## Your first window

```python
from guipi26 import create_window, create_label

app = create_window("Hello GUIpi26", 800, 500)
create_label(app, "Hello, world!", x=40, y=40, width=400, height=40, style="title")
app.mainloop()
```

`create_window(title, width, height)` returns a `Window` object. Every other helper takes that window as its first argument and returns the control it created.

`app.mainloop()` blocks until the window is closed (or you call `app.destroy()`).

## Sections via the sidebar

Most apps use a sidebar to switch between sections. Tag any control with `tab="key"` and it will only render while that sidebar entry is selected.

```python
from guipi26 import (
    create_window, create_collapsible_nav_bar,
    create_label, create_card,
)

app = create_window("Demo", 1000, 600)
create_collapsible_nav_bar(
    app, "Demo",
    [{"key": "a", "title": "A"}, {"key": "b", "title": "B"}],
    selected_key="a",
)

cx = app.content_origin_x(padding=32)
create_label(app, "Page A", x=cx, y=32, width=400, height=40, style="title", tab="a")
create_card(app, "Visits", "42", x=cx, y=120, width=240, height=110, tab="a")

create_label(app, "Page B", x=cx, y=32, width=400, height=40, style="title", tab="b")

app.mainloop()
```

`app.content_origin_x(padding=32)` returns the first X coordinate to the right of the sidebar, so your content lines up regardless of whether the sidebar is collapsed.

## Where to next

- [Components](components.md) for every available control
- [Layout & responsiveness](layout.md) for resizable windows
- [Theming](theming.md) to change colors
