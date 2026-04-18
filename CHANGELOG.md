# Changelog

All notable changes to GUIpi26 are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [PEP 440](https://peps.python.org/pep-0440/) versioning.

## [Unreleased]

## [0.1.0a1] - 2026-04-18

First public preview.

### Added
- Custom Win32/GDI rendering engine (`guipi26.window.Window`).
- Bootstrap-style sidebar shell via `create_collapsible_nav_bar()` with collapse toggle and per-page tagging (`tab="key"`).
- Controls: `create_label`, `create_button`, `create_card`, `create_panel`, `create_grid`, `create_chart`, `create_nav_bar`, `create_tabs`.
- Layout helpers: `create_horizontal_grid`, `create_vertical_grid`.
- Theming via `set_theme(...)` with light/dark surface, accent, and text colors.
- Responsive layout system: `Window.on_layout(callback)`, `Window.client_size()`, `Window.content_origin_x()`.
- Card collision safety: `collision_safety` flag plus `Window.set_card_collision_safety()`.
- Two example apps: `examples/dashboard.py`, `examples/contacts/app.py`.
- Benchmark suite under `benchmarks/` comparing GUIpi26 to Tkinter.
- Documentation in `docs/`.

### Notes
- **Windows-only.** Requires Python 3.8+.
- This is an early preview — install with `pip install --pre guipi26`.

[Unreleased]: https://github.com/DillanStep/guipi26/compare/v0.1.0a1...HEAD
[0.1.0a1]: https://github.com/DillanStep/guipi26/releases/tag/v0.1.0a1
