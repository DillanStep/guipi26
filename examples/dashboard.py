"""Responsive dashboard example for GUIpi26.

Resize the window to see the cards, panels, and charts reflow.
"""

from guipi26 import (
    create_button,
    create_card,
    create_chart,
    create_collapsible_nav_bar,
    create_grid,
    create_label,
    create_nav_bar,
    create_panel,
    create_window,
    set_theme,
)


def _row(x, width, count, gap=16):
    cell_w = (width - gap * (count - 1)) // count
    return [(x + i * (cell_w + gap), cell_w) for i in range(count)]


def main():
    app = create_window("GUIpi26 Dashboard", 1200, 760)
    app.set_min_size(960, 640)
    set_theme(app, background="#f5f6f8", surface="#ffffff", accent="#0d6efd")

    create_collapsible_nav_bar(
        app, "GUIpi26",
        [
            {"key": "overview", "title": "Overview", "subtitle": "Home"},
            {"key": "controls", "title": "Controls", "subtitle": "Components"},
            {"key": "motion", "title": "Charts", "subtitle": "Data"},
        ],
        width=240, collapsed_width=72, selected_key="overview",
    )

    # Headers
    title_o = create_label(app, "Overview", x=0, y=32, width=420, height=40, style="title", tab="overview")
    sub_o = create_label(app, "What's happening across your workspace today.", x=0, y=78, width=640, height=24, style="subtitle", tab="overview")
    title_c = create_label(app, "Controls", x=0, y=32, width=420, height=40, style="title", tab="controls")
    sub_c = create_label(app, "Every component shipped with GUIpi26.", x=0, y=78, width=640, height=24, style="subtitle", tab="controls")
    title_m = create_label(app, "Charts", x=0, y=32, width=420, height=40, style="title", tab="motion")
    sub_m = create_label(app, "Plot data without leaving the engine.", x=0, y=78, width=640, height=24, style="subtitle", tab="motion")

    # Overview
    nav_o = create_nav_bar(app, "This week", x=0, y=130, width=0,
                           subtitle="Snapshot of the last 7 days.",
                           actions=[{"text": "Share"}, {"text": "New report", "accent": True}],
                           tab="overview")
    card_sessions = create_card(app, "Sessions", "24", x=0, y=200, width=0, height=118, subtitle="up 12% vs last week", accent="#0d6efd", tab="overview")
    card_users = create_card(app, "Active users", "312", x=0, y=200, width=0, height=118, subtitle="online right now", accent="#198754", tab="overview")
    card_errors = create_card(app, "Errors", "3", x=0, y=200, width=0, height=118, subtitle="in the last hour", accent="#dc3545", tab="overview")
    panel_activity = create_panel(app, "Recent activity", x=0, y=338, width=0, height=200, subtitle="A feed of the latest events from your team.", accent="#0d6efd", tab="overview")
    panel_notes = create_panel(app, "Notes", x=0, y=338, width=0, height=200, subtitle="Drop quick reminders here while you work.", accent="#6f42c1", tab="overview")
    btn_report = create_button(app, "Open report", x=0, y=338, width=0, height=44, accent="#0d6efd", tab="overview")
    btn_invite = create_button(app, "Invite teammate", x=0, y=394, width=0, height=44, background="#ffffff", border="#dee2e6", tab="overview")

    # Controls
    nav_c = create_nav_bar(app, "Component library", x=0, y=130, width=0,
                           subtitle="Mix and match these to build a screen.",
                           actions=[{"text": "Refresh"}, {"text": "Add component", "accent": True}],
                           tab="controls")
    grid_components = create_grid(app, ["Component", "Group", "Status"],
                                  [["Sidebar", "Shell", "Stable"], ["Panel", "Layout", "Stable"], ["Card", "Data", "Stable"], ["Chart", "Data", "Beta"]],
                                  x=0, y=200, width=0, row_height=38, tab="controls")
    card_total = create_card(app, "Total", "12", x=0, y=200, width=0, height=140, subtitle="components", accent="#0d6efd", tab="controls")
    card_beta = create_card(app, "Beta", "1", x=0, y=360, width=0, height=140, subtitle="not yet final", accent="#fd7e14", tab="controls")
    btn_save = create_button(app, "Save", x=0, y=440, width=140, height=40, accent="#0d6efd", tab="controls")
    btn_cancel = create_button(app, "Cancel", x=0, y=440, width=140, height=40, background="#ffffff", border="#dee2e6", tab="controls")

    # Charts
    nav_m = create_nav_bar(app, "Performance", x=0, y=130, width=0,
                           subtitle="Frame timings from the last render pass.",
                           actions=[{"text": "Export CSV"}, {"text": "Reset", "accent": True}],
                           tab="motion")
    chart_frame = create_chart(app, "Frame budget (ms)", [("Idle", 16), ("Layout", 10), ("Paint", 12), ("Input", 7)],
                               x=0, y=200, width=0, height=280, accent="#0d6efd", tab="motion")
    chart_count = create_chart(app, "Components rendered", [("Cards", 6), ("Panels", 2), ("Buttons", 4), ("Grids", 1)],
                               x=0, y=200, width=0, height=280, accent="#6f42c1", tab="motion")
    btn_close = create_button(app, "Close", app.destroy, x=0, y=500, width=140, height=40, accent="#0d6efd", tab="motion")

    def layout(w, h):
        cx = app.content_origin_x(padding=32)
        cw = max(420, w - cx - 32)

        for lbl in (title_o, title_c, title_m):
            lbl.x = cx
            lbl.width = max(280, cw - 40)
        for lbl in (sub_o, sub_c, sub_m):
            lbl.x = cx
            lbl.width = max(280, cw - 40)
        for nav in (nav_o, nav_c, nav_m):
            nav.x = cx
            nav.width = cw

        # Overview: 3 cards across, 2 panels + button stack
        c0, c1, c2 = _row(cx, cw, 3, gap=16)
        for card, (x, width) in zip((card_sessions, card_users, card_errors), (c0, c1, c2)):
            card.x = x
            card.width = width

        p0, p1, p2 = _row(cx, cw, 3, gap=16)
        panel_activity.x, panel_activity.width = p0
        panel_notes.x, panel_notes.width = p1
        btn_report.x, btn_report.width = p2
        btn_invite.x, btn_invite.width = p2

        # Controls: grid + side stack (3-col layout, grid spans 2)
        col0, col1, col2 = _row(cx, cw, 3, gap=20)
        grid_components.x = col0[0]
        grid_components.width = col0[1] + col1[1] + 20
        card_total.x, card_total.width = col2
        card_total.y = 200
        card_beta.x, card_beta.width = col2
        card_beta.y = card_total.y + card_total.height + 20
        btn_save.x = col0[0]
        btn_cancel.x = col0[0] + 156

        # Charts: 2 across
        ch0, ch1 = _row(cx, cw, 2, gap=20)
        chart_frame.x, chart_frame.width = ch0
        chart_count.x, chart_count.width = ch1
        btn_close.x = cx

    app.on_layout(layout)
    app.mainloop()


if __name__ == "__main__":
    main()
