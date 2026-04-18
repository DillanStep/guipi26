# GUIpi26 documentation

A fast, custom-rendered Windows UI engine for Python. No Tkinter, no Qt — just `ctypes` over Win32 + GDI with a Bootstrap-style sidebar shell.

## Contents

- [Getting started](getting-started.md) — install and your first window
- [Components](components.md) — every control with a short example
- [Layout & responsiveness](layout.md) — `on_layout`, grids, sidebar reflow
- [Theming](theming.md) — colors and typography
- [Card collision safety](collision-safety.md) — how cards avoid overlap
- [API reference](api-reference.md) — full public function reference
- [Publishing](publishing.md) — building and uploading to PyPI

## At a glance

```python
from guipi26 import (
    create_window, set_theme, create_collapsible_nav_bar,
    create_label, create_card,
)

app = create_window("My App", 1100, 720)
set_theme(app, accent="#0d6efd")

create_collapsible_nav_bar(
    app, "MyApp",
    [
        {"key": "home", "title": "Home"},
        {"key": "stats", "title": "Stats"},
    ],
    selected_key="home",
)

cx = app.content_origin_x(padding=32)
create_label(app, "Home", x=cx, y=32, width=420, height=40, style="title", tab="home")
create_card(app, "Sessions", "24", x=cx, y=120, width=240, height=110,
            subtitle="up 12%", accent="#0d6efd", tab="home")

app.mainloop()
```
