"""Form controls showcase for GUIpi26.

Demonstrates every interactive form control: text input, checkbox, switch,
radio group, slider, dropdown, and progress bar. Live-updates a status panel
when the user interacts with each control.

Run::

    python examples/forms/app.py
"""

import guipi26


def main():
    window = guipi26.create_window("GUIpi26 — Forms", 980, 720)
    guipi26.set_theme(window, accent="#005fb8")

    guipi26.create_label(
        window,
        text="Form controls",
        x=32,
        y=24,
        width=600,
        height=42,
        style="title",
    )
    guipi26.create_label(
        window,
        text="Every control here is custom-rendered, hover-aware, and themable.",
        x=32,
        y=68,
        width=720,
        height=24,
        style="body",
    )

    # Live status panel on the right.
    status = guipi26.create_card(
        window,
        title="Live state",
        value="—",
        subtitle="Interact with any control to update",
        x=620,
        y=120,
        width=320,
        height=560,
        accent="#005fb8",
    )

    state = {
        "name": "",
        "subscribe": True,
        "dark_mode": False,
        "plan": "pro",
        "volume": 42.0,
        "fruit": None,
        "progress": 0.35,
    }

    def refresh_status():
        lines = [
            f"name={state['name'] or '∅'}",
            f"subscribe={state['subscribe']}",
            f"dark={state['dark_mode']}",
            f"plan={state['plan']}",
            f"vol={int(state['volume'])}",
            f"fruit={state['fruit'] or '∅'}",
        ]
        status.value = " · ".join(lines)
        window.invalidate()

    # Text input
    guipi26.create_label(window, text="Name", x=32, y=128, width=200, height=22, style="caption")

    def on_name(value):
        state["name"] = value
        refresh_status()

    guipi26.create_text_input(
        window,
        placeholder="Your name",
        x=32,
        y=152,
        width=420,
        height=38,
        on_change=on_name,
    )

    # Checkbox
    def on_subscribe(checked):
        state["subscribe"] = checked
        refresh_status()

    guipi26.create_checkbox(
        window,
        label="Subscribe to release notes",
        checked=True,
        x=32,
        y=212,
        width=400,
        on_change=on_subscribe,
    )

    # Switch
    def on_dark(value):
        state["dark_mode"] = value
        refresh_status()

    guipi26.create_switch(
        window,
        label="Dark mode preview",
        on=False,
        x=32,
        y=252,
        width=400,
        on_change=on_dark,
    )

    # Radio group
    guipi26.create_label(window, text="Plan", x=32, y=304, width=200, height=22, style="caption")

    def on_plan(key):
        state["plan"] = key
        refresh_status()

    guipi26.create_radio_group(
        window,
        options=[("free", "Free"), ("pro", "Pro"), ("enterprise", "Enterprise")],
        selected="pro",
        x=32,
        y=330,
        width=240,
        item_height=30,
        on_change=on_plan,
    )

    # Slider
    guipi26.create_label(window, text="Volume", x=32, y=434, width=200, height=22, style="caption")

    def on_volume(value):
        state["volume"] = value
        refresh_status()

    guipi26.create_slider(
        window,
        value=42,
        minimum=0,
        maximum=100,
        x=32,
        y=460,
        width=420,
        on_change=on_volume,
    )

    # Dropdown
    guipi26.create_label(window, text="Favourite fruit", x=32, y=512, width=200, height=22, style="caption")

    def on_fruit(value):
        state["fruit"] = value
        refresh_status()

    guipi26.create_dropdown(
        window,
        options=["Apple", "Banana", "Cherry", "Durian", "Mango"],
        placeholder="Choose…",
        x=32,
        y=538,
        width=320,
        on_change=on_fruit,
    )

    # Progress
    guipi26.create_label(window, text="Upload progress", x=32, y=602, width=200, height=22, style="caption")
    progress = guipi26.create_progress_bar(
        window,
        value=state["progress"],
        x=32,
        y=636,
        width=420,
        height=10,
        show_label=True,
    )

    def bump():
        progress.value = min(1.0, progress.value + 0.1)
        window.invalidate()

    def reset():
        progress.value = 0.0
        window.invalidate()

    guipi26.create_button(window, text="Bump +10%", command=bump, x=32, y=664, width=140, accent="#005fb8")
    guipi26.create_button(window, text="Reset", command=reset, x=184, y=664, width=120)

    refresh_status()
    window.mainloop()


if __name__ == "__main__":
    main()
