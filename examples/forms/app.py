"""Form controls showcase for GUIpi26.

Demonstrates every interactive form control: text input, checkbox, switch,
radio group, slider, dropdown, and progress bar. Live-updates a status panel
when the user interacts with each control. Fully responsive — resize the
window and everything reflows.

Run::

    python examples/forms/app.py
"""

import guipi26


PADDING = 32
ROW_GAP = 18
SECTION_GAP = 28
RIGHT_PANEL_WIDTH = 320
RIGHT_PANEL_GAP = 32
MIN_FORM_WIDTH = 320
MAX_FORM_WIDTH = 520


def main():
    window = guipi26.create_window("GUIpi26 — Forms", 1080, 760)
    window.set_min_size(720, 620)
    guipi26.set_theme(window, accent="#005fb8")

    title = guipi26.create_label(
        window, text="Form controls",
        x=PADDING, y=24, width=600, height=42, style="title",
    )
    subtitle = guipi26.create_label(
        window,
        text="Every control here is custom-rendered, hover-aware, themable, and reflows on resize.",
        x=PADDING, y=68, width=720, height=24, style="body",
    )

    # ----- Live status panel (right column) ------------------------------
    status_panel = guipi26.create_panel(
        window, title="Live state",
        x=0, y=0, width=RIGHT_PANEL_WIDTH, height=620,
        subtitle="Live values appear below",
    )
    status_lines = [
        guipi26.create_label(window, text="", x=0, y=0, width=RIGHT_PANEL_WIDTH - 40, height=22, style="body")
        for _ in range(7)
    ]

    # ----- Form column ---------------------------------------------------
    name_label = guipi26.create_label(window, text="Name", x=PADDING, y=0, width=200, height=22, style="caption")
    name_input = guipi26.create_text_input(
        window, placeholder="Your name",
        x=PADDING, y=0, width=400, height=38,
    )

    subscribe = guipi26.create_checkbox(
        window, label="Subscribe to release notes", checked=True,
        x=PADDING, y=0, width=400,
    )
    dark_mode = guipi26.create_switch(
        window, label="Dark mode preview", on=False,
        x=PADDING, y=0, width=400,
    )

    plan_label = guipi26.create_label(window, text="Plan", x=PADDING, y=0, width=200, height=22, style="caption")
    plan_group = guipi26.create_radio_group(
        window,
        options=[("free", "Free"), ("pro", "Pro"), ("enterprise", "Enterprise")],
        selected="pro",
        x=PADDING, y=0, width=240, item_height=30,
    )

    volume_label = guipi26.create_label(window, text="Volume", x=PADDING, y=0, width=200, height=22, style="caption")
    volume_slider = guipi26.create_slider(
        window, value=42, minimum=0, maximum=100,
        x=PADDING, y=0, width=400,
    )

    fruit_label = guipi26.create_label(window, text="Favourite fruit", x=PADDING, y=0, width=200, height=22, style="caption")
    fruit_dropdown = guipi26.create_dropdown(
        window,
        options=["Apple", "Banana", "Cherry", "Durian", "Mango"],
        placeholder="Choose…",
        x=PADDING, y=0, width=320,
    )

    progress_label = guipi26.create_label(window, text="Upload progress", x=PADDING, y=0, width=200, height=22, style="caption")
    progress_pct = guipi26.create_label(
        window, text="35%", x=PADDING, y=0, width=80, height=22, style="caption",
    )
    progress_bar = guipi26.create_progress_bar(
        window, value=0.35,
        x=PADDING, y=0, width=400, height=10,
        show_label=False,  # we render the % label ourselves to avoid overlap
    )

    bump_button = guipi26.create_button(
        window, text="Bump +10%", x=PADDING, y=0, width=140, height=38, accent="#005fb8",
    )
    reset_button = guipi26.create_button(
        window, text="Reset", x=PADDING, y=0, width=120, height=38,
    )

    # ----- State + handlers ---------------------------------------------
    state = {
        "name": "",
        "subscribe": True,
        "dark_mode": False,
        "plan": "pro",
        "volume": 42.0,
        "fruit": None,
    }

    def refresh_status():
        lines = [
            f"Name:  {state['name'] or '—'}",
            f"Subscribe:  {'yes' if state['subscribe'] else 'no'}",
            f"Dark mode:  {'on' if state['dark_mode'] else 'off'}",
            f"Plan:  {state['plan']}",
            f"Volume:  {int(state['volume'])}",
            f"Fruit:  {state['fruit'] or '—'}",
            f"Upload:  {int(progress_bar.value * 100)}%",
        ]
        for label, text in zip(status_lines, lines):
            label.text = text
        progress_pct.text = f"{int(progress_bar.value * 100)}%"
        window.invalidate()

    def on_name(value):
        state["name"] = value
        refresh_status()

    def on_subscribe(value):
        state["subscribe"] = value
        refresh_status()

    def on_dark(value):
        state["dark_mode"] = value
        refresh_status()

    def on_plan(key):
        state["plan"] = key
        refresh_status()

    def on_volume(value):
        state["volume"] = value
        refresh_status()

    def on_fruit(value):
        state["fruit"] = value
        refresh_status()

    def bump():
        progress_bar.value = min(1.0, progress_bar.value + 0.1)
        refresh_status()

    def reset():
        progress_bar.value = 0.0
        refresh_status()

    name_input.on_change = on_name
    subscribe.on_change = on_subscribe
    dark_mode.on_change = on_dark
    plan_group.on_change = on_plan
    volume_slider.on_change = on_volume
    fruit_dropdown.on_change = on_fruit
    bump_button.command = bump
    reset_button.command = reset

    # ----- Responsive layout --------------------------------------------
    def layout(width, height):
        # Right-hand status panel hugs the right edge; the form column takes
        # the remaining width up to MAX_FORM_WIDTH. If too narrow, stack.
        stacked = width < (MIN_FORM_WIDTH + RIGHT_PANEL_WIDTH + RIGHT_PANEL_GAP + PADDING * 2)
        if stacked:
            form_width = max(MIN_FORM_WIDTH, width - PADDING * 2)
            right_panel_x = PADDING  # placeholder, recomputed below
        else:
            right_panel_x = width - RIGHT_PANEL_WIDTH - PADDING
            form_width = max(MIN_FORM_WIDTH, min(MAX_FORM_WIDTH, right_panel_x - RIGHT_PANEL_GAP - PADDING))

        # Title + subtitle
        title.width = max(400, width - PADDING * 2)
        subtitle.width = max(400, width - PADDING * 2)

        # Vertical cursor for the form column.
        y = 110

        name_label.x = PADDING; name_label.y = y; name_label.width = form_width
        y += 26
        name_input.x = PADDING; name_input.y = y; name_input.width = form_width
        y += name_input.height + SECTION_GAP

        subscribe.x = PADDING; subscribe.y = y; subscribe.width = form_width
        y += subscribe.height + ROW_GAP

        dark_mode.x = PADDING; dark_mode.y = y; dark_mode.width = form_width
        y += dark_mode.height + SECTION_GAP

        plan_label.x = PADDING; plan_label.y = y; plan_label.width = form_width
        y += 26
        plan_group.x = PADDING; plan_group.y = y; plan_group.width = form_width
        y += plan_group.height + SECTION_GAP

        volume_label.x = PADDING; volume_label.y = y; volume_label.width = form_width
        y += 26
        volume_slider.x = PADDING; volume_slider.y = y; volume_slider.width = form_width
        y += volume_slider.height + SECTION_GAP

        fruit_label.x = PADDING; fruit_label.y = y; fruit_label.width = form_width
        y += 26
        fruit_dropdown.x = PADDING; fruit_dropdown.y = y
        fruit_dropdown.width = min(form_width, 360)
        y += fruit_dropdown.height + SECTION_GAP

        progress_label.x = PADDING; progress_label.y = y; progress_label.width = form_width - 90
        progress_pct.x = PADDING + form_width - 80; progress_pct.y = y; progress_pct.width = 80
        y += 26
        progress_bar.x = PADDING; progress_bar.y = y; progress_bar.width = form_width
        y += progress_bar.height + ROW_GAP + 4  # extra breathing room before buttons

        bump_button.x = PADDING; bump_button.y = y
        reset_button.x = PADDING + bump_button.width + 12; reset_button.y = y
        form_bottom = y + bump_button.height + PADDING

        # Status panel positioning.
        if stacked:
            status_panel.x = PADDING
            status_panel.y = form_bottom
            status_panel.width = max(MIN_FORM_WIDTH, width - PADDING * 2)
            status_panel.height = max(220, height - status_panel.y - PADDING)
        else:
            status_panel.x = right_panel_x
            status_panel.y = 110
            status_panel.width = RIGHT_PANEL_WIDTH
            status_panel.height = max(280, min(form_bottom - 110, height - 110 - PADDING))

        # Status lines stacked inside the panel, below its title + subtitle.
        line_x = status_panel.x + 20
        line_y = status_panel.y + 80
        line_w = status_panel.width - 40
        for label in status_lines:
            label.x = line_x
            label.y = line_y
            label.width = line_w
            line_y += 26

    window.on_layout(layout)
    refresh_status()
    window.mainloop()


if __name__ == "__main__":
    main()
