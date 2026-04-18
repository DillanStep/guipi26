# Form controls

GUIpi26 ships with a complete suite of interactive form controls, all custom-rendered, hover-aware, and themable.

| Control | Helper | Use case |
| --- | --- | --- |
| Text input | `create_text_input` | Single-line text entry, passwords, search boxes |
| Checkbox | `create_checkbox` | Boolean toggle with a label |
| Switch | `create_switch` | Modern on/off toggle |
| Radio group | `create_radio_group` | Mutually-exclusive choice |
| Slider | `create_slider` | Numeric range with click + drag |
| Dropdown | `create_dropdown` | Pick one option from a popup list |
| Progress bar | `create_progress_bar` | Non-interactive progress indicator |

Every control accepts the standard `tab="..."` keyword for sidebar / tab scoping (see [Layout](layout.md)).

## Text input

```python
def on_change(value):
    print("Now:", value)

guipi26.create_text_input(
    window,
    placeholder="Email",
    x=24, y=24, width=320, height=38,
    on_change=on_change,
    on_submit=lambda v: print("Enter:", v),
)
```

Supports keyboard editing (typing, Backspace, Delete, ←, →, Home, End) and `Tab` cycling between fields. Pass `password=True` to mask the value, or `max_length=N` to cap it.

## Checkbox

```python
guipi26.create_checkbox(
    window,
    label="Subscribe to release notes",
    checked=True,
    x=24, y=80,
    on_change=lambda v: print("subscribe:", v),
)
```

## Switch

```python
guipi26.create_switch(
    window,
    label="Dark mode",
    on=False,
    x=24, y=120,
    on_change=lambda v: print("dark:", v),
)
```

## Radio group

```python
guipi26.create_radio_group(
    window,
    options=[("free", "Free"), ("pro", "Pro"), ("enterprise", "Enterprise")],
    selected="pro",
    x=24, y=170,
    on_change=lambda key: print("plan:", key),
)
```

Options can be `(key, label)` tuples, `{"key": ..., "label": ...}` dicts, or plain strings.

## Slider

```python
guipi26.create_slider(
    window,
    value=42, minimum=0, maximum=100,
    x=24, y=260, width=320,
    on_change=lambda v: print("vol:", int(v)),
)
```

Click anywhere on the track to jump, or grab the handle to drag continuously. Pass `step=5` to snap to integer multiples.

## Dropdown

```python
guipi26.create_dropdown(
    window,
    options=["Apple", "Banana", "Cherry"],
    placeholder="Pick a fruit",
    x=24, y=320, width=240,
    on_change=lambda v: print("fruit:", v),
)
```

Click the header to expand; click an option to select. Click anywhere else to dismiss. The popup is painted last so it overlays any other content.

## Progress bar

```python
bar = guipi26.create_progress_bar(window, value=0.35, x=24, y=400, width=320, show_label=True)
bar.value = 0.8
window.invalidate()
```

`ProgressBar.value` is in the range `0.0`-`1.0`. Set `show_label=True` to render a `42%` caption above the track.

## Reading & writing values

Each helper returns a control instance. Read or write `.value` (text input, slider, progress bar), `.checked` (checkbox), `.on` (switch), or `.selected` (radio group, dropdown) directly, then call `window.invalidate()` to repaint:

```python
field = guipi26.create_text_input(window, x=24, y=24)
# ... later ...
print(field.value)
field.value = "preset"
window.invalidate()
```

## Demo

See [`examples/forms/app.py`](https://github.com/DillanStep/guipi26/blob/main/examples/forms/app.py) for a complete showcase of every control wired up to a live status panel.
