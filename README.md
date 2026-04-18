# GUIpi26

[![CI](https://github.com/DillanStep/guipi26/actions/workflows/ci.yml/badge.svg)](https://github.com/DillanStep/guipi26/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/guipi26?include_prereleases)](https://pypi.org/project/guipi26/)
[![Python](https://img.shields.io/pypi/pyversions/guipi26)](https://pypi.org/project/guipi26/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **Early preview (alpha).** This is a proof of concept — expect breaking API changes between releases. Pin a specific version if you build on it.

A fast, custom-rendered Windows UI engine for Python. No Tkinter, no Qt — just `ctypes` over Win32 and GDI, with a small set of modern controls and a Bootstrap-style sidebar shell.

> Windows only. Python 3.8+.

## Install

```
pip install --pre guipi26
```

(`--pre` is required while GUIpi26 is in alpha. Plain `pip install guipi26` will skip pre-releases.)

## Hello, sidebar

```python
from guipi26 import (
    create_window, set_theme, create_collapsible_nav_bar,
    create_label, create_card, create_nav_bar,
)

app = create_window("My App", 1200, 760)
set_theme(app, background="#f5f6f8", surface="#ffffff", accent="#0d6efd")

create_collapsible_nav_bar(
    app, "MyApp",
    [
        {"key": "home", "title": "Home", "subtitle": "Start here"},
        {"key": "stats", "title": "Stats", "subtitle": "Numbers"},
    ],
    width=240, collapsed_width=72, selected_key="home",
)

cx = app.content_origin_x(padding=32)

create_label(app, "Home", x=cx, y=32, width=420, height=40, style="title", tab="home")
create_nav_bar(app, "Today", x=cx, y=130, width=800, subtitle="A quick look.", tab="home")
create_card(app, "Sessions", "24", x=cx, y=200, width=240, height=110, subtitle="up 12%", accent="#0d6efd", tab="home")

create_label(app, "Stats", x=cx, y=32, width=420, height=40, style="title", tab="stats")

app.mainloop()
```

## What's in the box

- `create_window` — the host window
- `create_collapsible_nav_bar` — full-height left sidebar with collapse toggle
- `create_nav_bar` — page header with title, subtitle, and action buttons
- `create_label`, `create_button`
- `create_card`, `create_panel`
- `create_grid` — simple data grid
- `create_chart` — bar chart
- `create_horizontal_grid`, `create_vertical_grid` — layout helpers
- `set_theme` — background, surface, accent, etc.

Tag any control with `tab="key"` to scope it to a sidebar entry. The shell only paints controls whose tag matches the active sidebar key (or controls with no tag).

## Example

A full dashboard example lives in [`examples/dashboard.py`](examples/dashboard.py):

```
python examples/dashboard.py
```

## License

MIT — see [LICENSE](LICENSE).

## Documentation

Full docs live in [`docs/`](docs/README.md):

- [Getting started](docs/getting-started.md)
- [Components](docs/components.md)
- [Layout & responsiveness](docs/layout.md)
- [Theming](docs/theming.md)
- [Card collision safety](docs/collision-safety.md)
- [API reference](docs/api-reference.md)
- [Publishing](docs/publishing.md)

## Benchmarks

GUIpi26 vs Tkinter (Windows 11, Python 3.9, 200 controls, median of 2 runs):

| metric | GUIpi26 | Tkinter | winner |
| --- | --- | --- | --- |
| cold start | 101 ms | 1430 ms | **14.0x** GUIpi26 |
| create 200 controls | 49 ms | 205 ms | **4.2x** GUIpi26 |
| paint avg | 21 ms | 32 ms | **1.5x** GUIpi26 |
| sustainable FPS | 47.6 | 30.9 | **1.5x** GUIpi26 |

Reproduce with `python benchmarks/run_all.py` — see [benchmarks/README.md](benchmarks/README.md) for methodology.
