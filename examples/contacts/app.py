"""Contacts — a small, responsive example app built with GUIpi26.

Resize the window: the layout reflows because positions are computed
inside an on_layout callback.
"""

from guipi26 import (
    create_button,
    create_card,
    create_collapsible_nav_bar,
    create_grid,
    create_label,
    create_nav_bar,
    create_panel,
    create_window,
    set_theme,
)


CONTACTS_ALL = [
    ["Ada Lovelace", "ada@analytical.dev", "London"],
    ["Alan Turing", "alan@bletchley.uk", "Manchester"],
    ["Grace Hopper", "grace@navy.mil", "New York"],
    ["Linus Torvalds", "linus@kernel.org", "Portland"],
    ["Margaret Hamilton", "margaret@nasa.gov", "Boston"],
    ["Tim Berners-Lee", "tim@w3.org", "Oxford"],
]
CONTACTS_FAVORITES = [
    ["Ada Lovelace", "ada@analytical.dev", "London"],
    ["Grace Hopper", "grace@navy.mil", "New York"],
    ["Tim Berners-Lee", "tim@w3.org", "Oxford"],
]
CONTACTS_RECENT = [
    ["Linus Torvalds", "linus@kernel.org", "today"],
    ["Margaret Hamilton", "margaret@nasa.gov", "yesterday"],
    ["Alan Turing", "alan@bletchley.uk", "2 days ago"],
]


def main():
    app = create_window("Contacts", 1180, 720)
    set_theme(app, background="#f5f6f8", surface="#ffffff", accent="#198754")

    create_collapsible_nav_bar(
        app, "Contacts",
        [
            {"key": "all", "title": "All contacts", "subtitle": f"{len(CONTACTS_ALL)} people"},
            {"key": "favorites", "title": "Favorites", "subtitle": f"{len(CONTACTS_FAVORITES)} starred"},
            {"key": "recent", "title": "Recent", "subtitle": "last 7 days"},
        ],
        width=240, collapsed_width=72, selected_key="all",
    )

    # Per-page headers
    title_all = create_label(app, "All contacts", x=0, y=32, width=420, height=40, style="title", tab="all")
    sub_all = create_label(app, "Everyone in your address book.", x=0, y=78, width=640, height=24, style="subtitle", tab="all")
    title_fav = create_label(app, "Favorites", x=0, y=32, width=420, height=40, style="title", tab="favorites")
    sub_fav = create_label(app, "The people you talk to most.", x=0, y=78, width=640, height=24, style="subtitle", tab="favorites")
    title_recent = create_label(app, "Recent", x=0, y=32, width=420, height=40, style="title", tab="recent")
    sub_recent = create_label(app, "Conversations from the last week.", x=0, y=78, width=640, height=24, style="subtitle", tab="recent")

    # All contacts
    nav_all = create_nav_bar(app, "Address book", x=0, y=130, width=0,
                             subtitle="Search, edit, or add a new contact.",
                             actions=[{"text": "Import"}, {"text": "New contact", "accent": True}],
                             tab="all")
    grid_all = create_grid(app, ["Name", "Email", "City"], CONTACTS_ALL, x=0, y=200, width=0, row_height=38, tab="all")
    card_people = create_card(app, "People", str(len(CONTACTS_ALL)), x=0, y=200, width=0, height=110, subtitle="in address book", accent="#198754", tab="all")
    card_cities = create_card(app, "Cities", "5", x=0, y=322, width=0, height=110, subtitle="around the world", accent="#0d6efd", tab="all")
    panel_tip = create_panel(app, "Tip", x=0, y=444, width=0, height=110, subtitle="Star a contact to keep them in Favorites.", accent="#fd7e14", tab="all")

    # Favorites
    nav_fav = create_nav_bar(app, "Favorites", x=0, y=130, width=0,
                             subtitle="The people you reach out to the most.",
                             actions=[{"text": "Sort"}, {"text": "Add favorite", "accent": True}],
                             tab="favorites")
    grid_fav = create_grid(app, ["Name", "Email", "City"], CONTACTS_FAVORITES, x=0, y=200, width=0, row_height=38, tab="favorites")
    panel_fav = create_panel(app, "Why favorites?", x=0, y=200, width=0, height=180,
                             subtitle="Pin contacts you message every day so they stay one click away.",
                             accent="#198754", tab="favorites")

    # Recent
    nav_recent = create_nav_bar(app, "Recent activity", x=0, y=130, width=0,
                                subtitle="People you've talked to lately.",
                                actions=[{"text": "Clear"}, {"text": "Compose", "accent": True}],
                                tab="recent")
    grid_recent = create_grid(app, ["Name", "Email", "When"], CONTACTS_RECENT, x=0, y=200, width=0, row_height=38, tab="recent")
    card_week = create_card(app, "This week", str(len(CONTACTS_RECENT)), x=0, y=200, width=0, height=110, subtitle="conversations", accent="#198754", tab="recent")
    btn_compose = create_button(app, "Compose new", x=0, y=322, width=0, height=44, accent="#198754", tab="recent")

    def layout(w, h):
        cx = app.content_origin_x(padding=32)
        cw = max(360, w - cx - 32)
        side_w = max(220, min(280, cw // 4))
        gap = 20
        grid_w = cw - side_w - gap
        side_x = cx + grid_w + gap

        # Move headers in line with content origin
        for label in (title_all, title_fav, title_recent):
            label.x = cx
            label.width = max(240, cw - 40)
        for label in (sub_all, sub_fav, sub_recent):
            label.x = cx
            label.width = max(280, cw - 40)

        # Page nav bars stretch to content width
        for nav in (nav_all, nav_fav, nav_recent):
            nav.x = cx
            nav.width = cw

        # Grids take left column
        for grid in (grid_all, grid_fav, grid_recent):
            grid.x = cx
            grid.width = grid_w

        # All-contacts side column
        card_people.x = side_x
        card_people.width = side_w
        card_cities.x = side_x
        card_cities.width = side_w
        panel_tip.x = side_x
        panel_tip.width = side_w

        # Favorites side panel
        panel_fav.x = side_x
        panel_fav.width = side_w

        # Recent side column
        card_week.x = side_x
        card_week.width = side_w
        btn_compose.x = side_x
        btn_compose.width = side_w

    app.on_layout(layout)
    app.mainloop()


if __name__ == "__main__":
    main()
