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
