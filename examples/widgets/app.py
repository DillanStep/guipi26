"""GUIpi26 Win32 widgets showcase.

Polished, responsive demo of the Tier 1 Win32 widget wave:
ListBox, TreeView, MenuBar, Tooltips, MessageBox, keyboard accelerators.
"""

import guipi26 as g


# Layout constants — single source of truth so the on_layout callback can
# recompute everything when the user resizes the window.
PAD_X = 28
GUTTER = 20
MENU_H = 36
HEADER_TOP = MENU_H + 24
HEADER_H = 36
SUBHEADER_H = 22
SECTION_TOP_GAP = 22
SECTION_BODY_PAD = 16
SECTION_BODY_TOP = 80   # space inside panel before its first control
STATUS_BAR_H = 44


def main():
    win = g.create_window("GUIpi26 — Win32 widgets showcase", 1120, 740)
    win.set_min_size(900, 620)

    languages = ["Python", "Rust", "Go", "TypeScript", "C#", "Kotlin",
                 "Swift", "Ruby", "Elixir", "Zig", "C++", "Java",
                 "JavaScript", "Lua"]
    project_tree = [
        ("guipi26", [
            "window.py",
            "__init__.py",
            ("docs", ["index.md", "forms.md", "widgets.md"]),
        ]),
        ("examples", [
            ("forms", ["app.py"]),
            ("widgets", ["app.py"]),
        ]),
        ("benchmarks", [
            "bench_guipi26.py",
            "bench_tkinter.py",
            ("plots", ["summary.png", "speedup.png"]),
        ]),
    ]

    # ---------------- Status bar ----------------
    status_label = g.create_label(
        win, "Ready · hover any control for tooltips",
        x=0, y=0, width=0, height=STATUS_BAR_H, style="caption",
    )

    def set_status(text):
        status_label.text = text
        win.invalidate()

    # ---------------- MenuBar ----------------
    def on_about():
        g.show_message_box(
            win,
            "GUIpi26 — fast, custom-rendered Windows UI for Python.\n\n"
            "Tier 1 Win32 widgets are now live: ListBox, TreeView, MenuBar, "
            "Tooltips, MessageBox, accelerators, and cursor management.",
            title="About GUIpi26", style="info",
        )

    def on_save():
        set_status("Saved (pretend).")
        g.show_message_box(win, "Pretend save complete.", title="Saved", style="info")

    g.create_menu_bar(win, [
        ("File", [
            ("New",   lambda: set_status("New document."),            "Ctrl+N"),
            ("Open…", lambda: set_status("Open dialog placeholder."), "Ctrl+O"),
            ("Save",  on_save,                                         "Ctrl+S"),
            ("Quit",  win.destroy,                                     "Alt+F4"),
        ]),
        ("Edit", [
            ("Undo", lambda: set_status("Undo."), "Ctrl+Z"),
            ("Redo", lambda: set_status("Redo."), "Ctrl+Y"),
        ]),
        ("Help", [
            ("About GUIpi26", on_about, None),
        ]),
    ])

    # ---------------- Title block ----------------
    title_label = g.create_label(
        win, "Win32 UI elements showcase",
        x=PAD_X, y=HEADER_TOP, width=900, height=HEADER_H, style="title",
    )
    subtitle_label = g.create_label(
        win, "Hover any control for tooltips · Click items · Try Ctrl+S / Ctrl+M shortcuts.",
        x=PAD_X, y=HEADER_TOP + HEADER_H + 4, width=900, height=SUBHEADER_H, style="caption",
    )

    # ---------------- Section panels ----------------
    list_panel = g.create_panel(win, title="ListBox",
                                subtitle="Single-selection · scroll wheel · ↑/↓ keys",
                                x=PAD_X, y=0, width=320, height=420,
                                accent="#2563eb")
    tree_panel = g.create_panel(win, title="TreeView",
                                subtitle="Click chevron to expand · click row to select",
                                x=PAD_X, y=0, width=320, height=420,
                                accent="#10b981")
    dlg_panel  = g.create_panel(win, title="Dialogs",
                                subtitle="Native Win32 message boxes",
                                x=PAD_X, y=0, width=320, height=420,
                                accent="#f59e0b")

    # ---------------- ListBox ----------------
    list_status = g.create_label(
        win, f"Selected: {languages[0]}",
        x=PAD_X, y=0, width=280, height=22, style="caption",
    )

    def set_list_status(i):
        list_status.text = f"Selected: {languages[i]}"
        set_status(f"ListBox → {languages[i]}")
        win.invalidate()

    list_box = g.create_list_box(
        win, items=languages, selected_index=0,
        x=PAD_X, y=0, width=280, height=260,
        on_change=set_list_status,
        tooltip="Click or use ↑/↓ to select a language",
    )

    # ---------------- TreeView ----------------
    tree_status = g.create_label(
        win, "(no node selected)",
        x=PAD_X, y=0, width=280, height=22, style="caption",
    )

    def on_tree(node):
        tree_status.text = f"Selected: {node.label}"
        set_status(f"TreeView → {node.label}")
        win.invalidate()

    tree_view = g.create_tree_view(
        win, nodes=project_tree,
        x=PAD_X, y=0, width=280, height=260,
        on_select=on_tree,
        tooltip="Click chevron to expand · Click row to select",
    )

    # ---------------- Dialog buttons ----------------
    def confirm_quit():
        result = g.show_message_box(
            win, "Quit the application?", title="Confirm",
            style="question", buttons="yesno",
        )
        if result == 6:
            win.destroy()

    btn_info = g.create_button(
        win, "Information", x=PAD_X, y=0, width=240, height=42,
        command=lambda: g.show_message_box(win, "Heads up — this is informational.",
                                           title="Info", style="info"),
        accent="#2563eb", tooltip="Show an info dialog",
    )
    btn_warn = g.create_button(
        win, "Warning", x=PAD_X, y=0, width=240, height=42,
        command=lambda: g.show_message_box(win, "Be careful — proceed with caution.",
                                           title="Warning", style="warning"),
        tooltip="Show a warning dialog",
    )
    btn_err = g.create_button(
        win, "Error", x=PAD_X, y=0, width=240, height=42,
        command=lambda: g.show_message_box(win, "Something went wrong.",
                                           title="Error", style="error"),
        tooltip="Show an error dialog",
    )
    btn_yn = g.create_button(
        win, "Yes / No", x=PAD_X, y=0, width=240, height=42,
        command=confirm_quit, tooltip="Show a Yes/No confirm dialog",
    )

    # ---------------- Accelerators ----------------
    g.create_accelerator(win, "S", on_save, ctrl=True, description="Save")
    g.create_accelerator(win, "M",
                         lambda: g.show_message_box(win, "Hello from Ctrl+M!", title="Shortcut"),
                         ctrl=True, description="Show message")
    g.create_accelerator(win, 0x1B, win.destroy, description="Escape to quit")

    win.menu_bar.y = 0

    # ---------------- Responsive layout ----------------
    def relayout(width, height):
        usable = width - PAD_X * 2 - GUTTER * 2
        col_w = max(220, usable // 3)
        col_xs = [
            PAD_X,
            PAD_X + col_w + GUTTER,
            PAD_X + (col_w + GUTTER) * 2,
        ]

        title_label.width = width - PAD_X * 2
        subtitle_label.width = width - PAD_X * 2

        sections_top = HEADER_TOP + HEADER_H + 4 + SUBHEADER_H + SECTION_TOP_GAP
        # Reserve room for status bar + 12px breathing room
        max_section_bottom = height - STATUS_BAR_H - 12
        # Minimum panel height so controls always fit comfortably
        min_section_h = 380
        sections_bottom = max(sections_top + min_section_h, max_section_bottom)
        section_h = sections_bottom - sections_top
        body_top = sections_top + SECTION_BODY_TOP

        # Status bar pinned just below the panels
        status_label.x = PAD_X
        status_label.y = sections_bottom + 12
        status_label.width = width - PAD_X * 2

        # Column 1 — ListBox
        list_panel.x, list_panel.y = col_xs[0], sections_top
        list_panel.width, list_panel.height = col_w, section_h
        body_x = col_xs[0] + SECTION_BODY_PAD
        body_w = col_w - SECTION_BODY_PAD * 2
        list_status.x, list_status.width = body_x, body_w
        list_status.y = sections_top + section_h - 38
        list_box.x, list_box.width = body_x, body_w
        list_box.y = body_top
        list_box.height = max(80, (list_status.y - body_top) - 12)

        # Column 2 — TreeView
        tree_panel.x, tree_panel.y = col_xs[1], sections_top
        tree_panel.width, tree_panel.height = col_w, section_h
        body_x = col_xs[1] + SECTION_BODY_PAD
        body_w = col_w - SECTION_BODY_PAD * 2
        tree_status.x, tree_status.width = body_x, body_w
        tree_status.y = sections_top + section_h - 38
        tree_view.x, tree_view.width = body_x, body_w
        tree_view.y = body_top
        tree_view.height = max(80, (tree_status.y - body_top) - 12)

        # Column 3 — Dialog buttons (vertically centered in panel body)
        dlg_panel.x, dlg_panel.y = col_xs[2], sections_top
        dlg_panel.width, dlg_panel.height = col_w, section_h
        body_w = col_w - SECTION_BODY_PAD * 2
        btn_w = min(240, body_w)
        btn_x = col_xs[2] + (col_w - btn_w) // 2
        btn_gap = 14
        btns = (btn_info, btn_warn, btn_err, btn_yn)
        total_btn_h = btns[0].height * len(btns) + btn_gap * (len(btns) - 1)
        body_avail_h = section_h - SECTION_BODY_TOP - 24
        btn_y = body_top + max(0, (body_avail_h - total_btn_h) // 2)
        for index, btn in enumerate(btns):
            btn.width = btn_w
            btn.x = btn_x
            btn.y = btn_y + index * (btn.height + btn_gap)

    win.on_layout(relayout)
    relayout(*win.client_size())
    win.mainloop()


if __name__ == "__main__":
    main()
"""GUIpi26 Win32 widgets showcase.

Demonstrates the controls added in the Win32 UI elements wave:
ListBox, TreeView, MenuBar, Tooltip (via tooltip="..."), MessageBox,
keyboard accelerators, and cursor management.
"""

import guipi26 as g


def main():
    win = g.create_window("GUIpi26 — Win32 widgets showcase", 1080, 720)

    # ---------------- Menu bar ----------------
    def on_about():
        g.show_message_box(
            win,
            "GUIpi26 — fast, custom-rendered Windows UI for Python.\n\n"
            "Tier 1 Win32 widgets are now live: ListBox, TreeView, MenuBar, "
            "Tooltips, MessageBox, accelerators, and cursor management.",
            title="About GUIpi26",
            style="info",
        )

    def on_save():
        g.show_message_box(win, "Pretend save complete.", title="Saved", style="info")

    def on_quit():
        win.destroy()

    g.create_menu_bar(win, [
        ("File", [
            ("New",    lambda: g.show_message_box(win, "New document.", title="File"), "Ctrl+N"),
            ("Open…", lambda: g.show_message_box(win, "Open dialog placeholder.", title="File"), "Ctrl+O"),
            ("Save",   on_save, "Ctrl+S"),
            ("Quit",   on_quit, "Alt+F4"),
        ]),
        ("Edit", [
            ("Undo", lambda: None, "Ctrl+Z"),
            ("Redo", lambda: None, "Ctrl+Y"),
        ]),
        ("Help", [
            ("About GUIpi26", on_about, None),
        ]),
    ])

    # ---------------- Header label ----------------
    g.create_label(win, "Win32 UI elements showcase",
                   x=24, y=56, width=900, height=36, style="title")
    g.create_label(win,
                   "Hover for tooltips · Click items · Try Ctrl+S / Ctrl+M shortcuts.",
                   x=24, y=92, width=900, height=24, style="caption")

    # ---------------- ListBox ----------------
    g.create_label(win, "ListBox", x=24, y=132, width=280, height=22, style="body")
    languages = ["Python", "Rust", "Go", "TypeScript", "C#", "Kotlin", "Swift",
                 "Ruby", "Elixir", "Zig", "C++", "Java", "JavaScript", "Lua"]
    selected_label = g.create_label(win, "(no selection)",
                                    x=24, y=400, width=300, height=24, style="caption")

    def on_select(i):
        selected_label.text = f"Selected: {languages[i]}"
        win.invalidate()

    g.create_list_box(win, items=languages, selected_index=0,
                      x=24, y=160, width=300, height=230,
                      on_change=on_select,
                      tooltip="Click or use ↑/↓ to select a language")
    on_select(0)

    # ---------------- TreeView ----------------
    g.create_label(win, "TreeView", x=360, y=132, width=300, height=22, style="body")

    tree_status = g.create_label(win, "(no node selected)",
                                 x=360, y=440, width=340, height=24, style="caption")

    def on_tree(node):
        tree_status.text = f"Selected: {node.label}"
        win.invalidate()

    project_tree = [
        ("guipi26", [
            "window.py",
            "__init__.py",
            ("docs", ["index.md", "forms.md", "widgets.md"]),
        ]),
        ("examples", [
            ("forms", ["app.py"]),
            ("widgets", ["app.py"]),
        ]),
        ("benchmarks", [
            "bench_guipi26.py",
            "bench_tkinter.py",
            ("plots", ["summary.png", "speedup.png"]),
        ]),
    ]
    g.create_tree_view(win, nodes=project_tree,
                       x=360, y=160, width=340, height=270,
                       on_select=on_tree,
                       tooltip="Click chevron to expand · Click row to select")

    # ---------------- Buttons + tooltip + message box demos ----------------
    g.create_label(win, "Dialogs", x=740, y=132, width=300, height=22, style="body")

    def confirm_quit():
        result = g.show_message_box(
            win, "Quit the application?", title="Confirm",
            style="question", buttons="yesno",
        )
        if result == 6:  # IDYES
            win.destroy()

    g.create_button(win, "Info",     x=740, y=160, width=140, height=36,
                    command=lambda: g.show_message_box(win, "Heads up!", title="Info", style="info"),
                    accent="#2563eb", tooltip="Show an info dialog")
    g.create_button(win, "Warning",  x=740, y=204, width=140, height=36,
                    command=lambda: g.show_message_box(win, "Be careful.", title="Warning", style="warning"),
                    tooltip="Show a warning dialog")
    g.create_button(win, "Error",    x=740, y=248, width=140, height=36,
                    command=lambda: g.show_message_box(win, "Something went wrong.", title="Error", style="error"),
                    tooltip="Show an error dialog")
    g.create_button(win, "Yes / No", x=740, y=292, width=140, height=36,
                    command=confirm_quit, tooltip="Show a Yes/No confirm dialog")

    # ---------------- Keyboard accelerators ----------------
    g.create_label(win, "Try shortcuts:  Ctrl+S = Save · Ctrl+M = Message · Esc = Quit",
                   x=24, y=470, width=1000, height=24, style="caption")
    g.create_accelerator(win, "S", on_save, ctrl=True, description="Save")
    g.create_accelerator(win, "M",
                         lambda: g.show_message_box(win, "Hello from Ctrl+M!", title="Shortcut"),
                         ctrl=True, description="Show message")
    g.create_accelerator(win, 0x1B, win.destroy, description="Escape to quit")  # VK_ESCAPE

    # Tweak menu bar y-offset so it sits at the very top.
    win.menu_bar.y = 0

    win.mainloop()


if __name__ == "__main__":
    main()
