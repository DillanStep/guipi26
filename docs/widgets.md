# Win32 widgets

GUIpi26 ships a growing catalog of Win32-style UI elements. The Tier 1 widget
wave (added in the unreleased development build) covers list boxes, tree views,
menu bars, tooltips, message boxes, keyboard accelerators, and cursor
management. All controls follow the same pattern as the rest of the engine:
custom-rendered, dataclass-driven, and exposed both as `Window.add_*`
instance methods and as module-level `create_*` helpers.

A complete runnable showcase lives in [`examples/widgets/app.py`](../examples/widgets/app.py).

## ListBox

A vertically scrolling list with single-row selection.

```python
import guipi26 as g

win = g.create_window("ListBox demo", 480, 400)
items = ["Python", "Rust", "Go", "TypeScript", "C#"]
g.create_list_box(
    win, items, selected_index=0,
    x=24, y=24, width=300, height=240,
    on_change=lambda i: print("selected:", items[i]),
    tooltip="Click a row or use the up/down arrow keys",
)
win.show()
win.run()
```

The mouse wheel scrolls the hovered list. Up/Down arrow keys move the
selection while the cursor is inside the list. A subtle thumb track is
drawn on the right edge whenever the list overflows.

## TreeView

A hierarchical view with collapsible nodes. Nodes can be passed as nested
tuples, dicts, strings, or `TreeNode` instances.

```python
g.create_tree_view(win, nodes=[
    ("Project", [
        "README.md",
        ("src", ["app.py", "utils.py"]),
        ("docs", ["index.md", "widgets.md"]),
    ]),
])
```

Click the chevron (`▸ / ▾`) to expand/collapse. Clicking a row anywhere
else selects it and fires `on_select(node)`.

## MenuBar

A horizontal menu bar with cascading dropdown panels. Items accept an
optional shortcut display string.

```python
g.create_menu_bar(win, [
    ("File", [
        ("New",   on_new,  "Ctrl+N"),
        ("Open…", on_open, "Ctrl+O"),
        ("Save",  on_save, "Ctrl+S"),
    ]),
    ("Help", [("About", on_about)]),
])
```

The shortcut string is purely visual — register the actual handler with
`create_accelerator` (see below).

## Tooltips

Any control that exposes a `tooltip` parameter (currently `Button`,
`ListBox`, `TreeView`) shows a delayed popup when the cursor lingers
over it.

```python
g.create_button(win, "Save", command=on_save, tooltip="Save the document (Ctrl+S)")
```

## MessageBox

`show_message_box` wraps the native Win32 `MessageBoxW` API and returns
the standard button id (`1=OK`, `2=Cancel`, `6=Yes`, `7=No`).

```python
result = g.show_message_box(
    win, "Quit the application?", title="Confirm",
    style="question", buttons="yesno",
)
if result == 6:
    win.destroy()
```

Supported `style` values: `info`, `warning`, `error`, `question`, `none`.
Supported `buttons` values: `ok`, `okcancel`, `yesno`, `yesnocancel`.

## Keyboard accelerators

Register global shortcuts on the window. The key can be a single
character or a virtual-key code.

```python
g.create_accelerator(win, "S", on_save,  ctrl=True)
g.create_accelerator(win, "Q", win.destroy, ctrl=True)
g.create_accelerator(win, 0x1B, win.destroy)  # VK_ESCAPE
```

Accelerators run before any focused text input receives the key,
so they will fire even while the user is typing.

## Cursor management

Cursors are switched automatically based on the hovered control:

| Hovered                                   | Cursor       |
| ----------------------------------------- | ------------ |
| Button, tab, switch, slider, list/tree    | hand pointer |
| `TextInput`                               | I-beam       |
| Empty space                               | arrow        |

No code is required — it just works once you call `Window.show()`.
