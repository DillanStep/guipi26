"""GUIpi26 — Northwind Analytics

A single-file enterprise-style application that combines every GUIpi26
capability into one cohesive product:

* MenuBar  +  keyboard accelerators  +  message boxes  +  tooltips
* Collapsible sidebar with five workspaces (Overview, Customers, Orders,
  Reports, Settings)
* KPI cards, charts, grids, panels, list boxes, tree views
* Form controls (text input, dropdown, slider, switch, radio, progress)
* Live status bar, fully responsive layout, mock business data

Run::

    python examples/enterprise/app.py
"""

from datetime import datetime, timedelta
import random

import guipi26 as g


# ------------------------------------------------------------------ mock data
random.seed(42)

CUSTOMERS = [
    ("Acme Corporation",       "enterprise", "Active",   1284200, 142),
    ("Globex Industries",      "enterprise", "Active",    984300,  98),
    ("Initech Systems",        "pro",        "Active",    412800,  64),
    ("Umbrella Holdings",      "enterprise", "Trial",     780500,  41),
    ("Hooli Cloud",            "pro",        "Active",    345000,  73),
    ("Vandelay Imports",       "free",       "Lapsed",     12500,   8),
    ("Soylent Foods",          "pro",        "Active",    228700,  55),
    ("Stark Industries",       "enterprise", "Active",   1840000, 201),
    ("Wayne Enterprises",      "enterprise", "Active",   1620000, 188),
    ("Pied Piper",             "free",       "Trial",       8400,   6),
    ("Cyberdyne Systems",      "pro",        "Active",    560100,  77),
    ("Wonka Industries",       "pro",        "Active",    178000,  39),
]

ORDERS = []
_states = ("Shipped", "Processing", "Delivered", "Pending", "Refunded")
for _i in range(28):
    cust = random.choice(CUSTOMERS)[0]
    state = random.choice(_states)
    days = random.randint(0, 21)
    date = (datetime(2026, 4, 18) - timedelta(days=days)).strftime("%Y-%m-%d")
    total = random.randint(420, 14800)
    ORDERS.append([f"NW-{1000 + _i:04d}", cust, date, state, f"${total:,}"])

PROJECT_TREE = [
    ("Workspaces", [
        ("Sales", ["Pipeline", "Forecast", "Lost deals"]),
        ("Marketing", ["Campaigns", "Email", "Attribution"]),
        ("Support", ["Open tickets", "SLA report", "CSAT"]),
    ]),
    ("Reports", [
        "Q1 — Revenue.pdf",
        "Q1 — Churn.pdf",
        ("Archive", ["2025.pdf", "2024.pdf"]),
    ]),
    ("Integrations", ["Stripe", "HubSpot", "Slack", "PagerDuty"]),
]

WEEKLY_REVENUE = [
    ("Mon", 18200), ("Tue", 24100), ("Wed", 21800),
    ("Thu", 29400), ("Fri", 33700), ("Sat", 12400), ("Sun", 9800),
]
PIPELINE_BY_STAGE = [
    ("Discover", 42), ("Qualify", 31), ("Propose", 24),
    ("Negotiate", 17), ("Close", 11),
]
REGION_REVENUE = [
    ("AMER", 1_840_000), ("EMEA", 1_220_000), ("APAC", 730_000), ("LATAM", 410_000),
]


# ------------------------------------------------------------------ constants
PAD = 28
GAP = 18
HEADER_TOP = 24
HEADER_H = 38
SUBHEADER_H = 22
NAV_H = 54
STATUS_H = 36
CONTENT_TOP = HEADER_TOP + HEADER_H + 8 + SUBHEADER_H + 18 + NAV_H + 16


def _row(x, width, count, gap=GAP):
    cell = (width - gap * (count - 1)) // count
    return [(x + i * (cell + gap), cell) for i in range(count)]


# ------------------------------------------------------------------ app
def main():
    win = g.create_window("Northwind Analytics — GUIpi26", 1320, 820)
    win.set_min_size(1040, 680)
    g.set_theme(win, background="#f4f6fa", surface="#ffffff", accent="#2563eb")

    # ----- status bar (drawn before everything else so layout uses it) -----
    status_label = g.create_label(
        win, "Ready · Northwind Analytics · v0.1.0",
        x=0, y=0, width=0, height=STATUS_H, style="caption",
    )

    def status(text):
        status_label.text = text
        win.invalidate()

    # ----- menubar ---------------------------------------------------------
    def about():
        g.show_message_box(
            win,
            "Northwind Analytics\n\n"
            "A reference enterprise application built entirely on GUIpi26 — "
            "a custom-rendered, hardware-light Python UI engine for Windows.\n\n"
            "Every pixel here is drawn by GUIpi26.",
            title="About Northwind Analytics", style="info",
        )

    def confirm_quit():
        if g.show_message_box(
            win, "Sign out and quit Northwind Analytics?",
            title="Quit", style="question", buttons="yesno",
        ) == 6:
            win.destroy()

    def export_csv():
        status(f"Exported {len(ORDERS)} orders to ./orders.csv (mock).")
        g.show_message_box(
            win, f"Exported {len(ORDERS)} orders to orders.csv",
            title="Export complete", style="info",
        )

    def refresh_data():
        status("Data refreshed from mock backend.")

    g.create_menu_bar(win, [
        ("File", [
            ("New report",   lambda: status("New report draft."), "Ctrl+N"),
            ("Refresh",      refresh_data,                         "F5"),
            ("Export CSV…",  export_csv,                           "Ctrl+E"),
            ("Quit",         confirm_quit,                         "Ctrl+Q"),
        ]),
        ("Edit", [
            ("Find",   lambda: status("Find dialog (placeholder)."), "Ctrl+F"),
            ("Filter", lambda: status("Filter sidebar (placeholder)."), "Ctrl+Shift+F"),
        ]),
        ("View", [
            ("Toggle sidebar", lambda: status("Sidebar toggled."), "Ctrl+B"),
            ("Reset zoom",     lambda: status("Zoom reset."),       "Ctrl+0"),
        ]),
        ("Help", [
            ("Documentation", lambda: status("Opening docs (placeholder)."), None),
            ("About",         about,                                          None),
        ]),
    ])

    # ----- collapsible sidebar --------------------------------------------
    g.create_collapsible_nav_bar(
        win, "Northwind",
        [
            {"key": "overview",  "title": "Overview",  "subtitle": "KPIs"},
            {"key": "customers", "title": "Customers", "subtitle": "Accounts"},
            {"key": "orders",    "title": "Orders",    "subtitle": "Pipeline"},
            {"key": "reports",   "title": "Reports",   "subtitle": "Charts"},
            {"key": "settings",  "title": "Settings",  "subtitle": "Workspace"},
        ],
        width=240, collapsed_width=72, selected_key="overview",
    )

    # ----- shared headers per tab -----------------------------------------
    def header(title_text, subtitle_text, tab_key):
        title = g.create_label(
            win, title_text, x=0, y=HEADER_TOP, width=600, height=HEADER_H,
            style="title", tab=tab_key,
        )
        subtitle = g.create_label(
            win, subtitle_text,
            x=0, y=HEADER_TOP + HEADER_H + 6, width=800, height=SUBHEADER_H,
            style="caption", tab=tab_key,
        )
        return title, subtitle

    title_o, sub_o = header("Overview",
                            "Snapshot of the business — last 7 days.", "overview")
    title_c, sub_c = header("Customers",
                            "12 accounts · click any row to open the profile.", "customers")
    title_or, sub_or = header("Orders",
                              "Live pipeline · filter, sort, export.", "orders")
    title_r, sub_r = header("Reports",
                            "Build, save and share data views.", "reports")
    title_s, sub_s = header("Settings",
                            "Personalise your workspace and preferences.", "settings")

    # ============================== OVERVIEW ==============================
    nav_o = g.create_nav_bar(
        win, "This week", x=0, y=0, width=0,
        subtitle="Operational health across all workspaces.",
        actions=[{"text": "Share"}, {"text": "New report", "accent": True}],
        tab="overview",
    )
    kpi_revenue  = g.create_card(win, "Revenue (wk)",   "$149K", x=0, y=0, width=0,
                                 height=128, subtitle="↑ 12% vs prev",
                                 accent="#2563eb", tab="overview")
    kpi_orders   = g.create_card(win, "New orders",      "284",  x=0, y=0, width=0,
                                 height=128, subtitle="↑ 4% vs prev",
                                 accent="#16a34a", tab="overview")
    kpi_customers = g.create_card(win, "Active customers","12",   x=0, y=0, width=0,
                                  height=128, subtitle="2 trials open",
                                  accent="#7c3aed", tab="overview")
    kpi_churn    = g.create_card(win, "Churn risk",     "1",    x=0, y=0, width=0,
                                 height=128, subtitle="lapsed this week",
                                 accent="#dc2626", tab="overview")

    chart_revenue = g.create_chart(
        win, "Revenue by day ($)", WEEKLY_REVENUE,
        x=0, y=0, width=0, height=260, accent="#2563eb", tab="overview",
    )
    chart_pipeline = g.create_chart(
        win, "Pipeline by stage", PIPELINE_BY_STAGE,
        x=0, y=0, width=0, height=260, accent="#7c3aed", tab="overview",
    )

    panel_activity = g.create_panel(
        win, title="Recent activity",
        x=0, y=0, width=0, height=200,
        subtitle="Realtime feed across the workspace.",
        accent="#2563eb", tab="overview",
    )
    activity_lines = [
        "✓ Stark Industries renewed Enterprise plan — $84K ARR",
        "→ New order NW-1027 from Wayne Enterprises ($14,800)",
        "✓ Hooli Cloud added 4 seats",
        "! Vandelay Imports payment failed — invoice INV-883",
        "→ Pied Piper started a Pro trial",
    ]
    activity_labels = [
        g.create_label(win, line, x=0, y=0, width=0, height=22,
                       style="caption", tab="overview")
        for line in activity_lines
    ]

    # ============================== CUSTOMERS ==============================
    nav_c = g.create_nav_bar(
        win, "All customers", x=0, y=0, width=0,
        subtitle="Click a name on the left to view their profile.",
        actions=[{"text": "Import"}, {"text": "Add customer", "accent": True}],
        tab="customers",
    )

    customer_names = [c[0] for c in CUSTOMERS]
    cust_panel  = g.create_panel(win, title="Accounts",  x=0, y=0, width=0, height=420,
                                 subtitle=f"{len(customer_names)} total",
                                 accent="#2563eb", tab="customers")
    detail_panel = g.create_panel(win, title="Profile",   x=0, y=0, width=0, height=420,
                                  subtitle="Mock CRM record.",
                                  accent="#16a34a", tab="customers")

    cust_listbox = g.create_list_box(
        win, items=customer_names, selected_index=0,
        x=0, y=0, width=0, height=320,
        tooltip="Select a customer",
        tab="customers",
    )

    detail_name   = g.create_label(win, "", x=0, y=0, width=0, height=28,
                                   style="title", tab="customers")
    detail_plan   = g.create_label(win, "", x=0, y=0, width=0, height=22,
                                   style="caption", tab="customers")
    detail_status = g.create_label(win, "", x=0, y=0, width=0, height=22,
                                   style="caption", tab="customers")
    detail_arr    = g.create_label(win, "", x=0, y=0, width=0, height=22,
                                   style="body", tab="customers")
    detail_seats  = g.create_label(win, "", x=0, y=0, width=0, height=22,
                                   style="body", tab="customers")

    note_label = g.create_label(win, "Internal note", x=0, y=0, width=0, height=20,
                                style="caption", tab="customers")
    note_input = g.create_text_input(
        win, placeholder="Add a private note about this account…",
        x=0, y=0, width=0, height=38, tab="customers",
    )
    btn_save_note = g.create_button(
        win, "Save note", x=0, y=0, width=140, height=38,
        accent="#2563eb", tooltip="Save this note (mock)", tab="customers",
    )
    btn_email = g.create_button(
        win, "Email account", x=0, y=0, width=160, height=38,
        tooltip="Compose an email (mock)", tab="customers",
    )

    def render_customer(idx):
        name, plan, st, arr, seats = CUSTOMERS[idx]
        detail_name.text   = name
        detail_plan.text   = f"Plan:  {plan.title()}"
        detail_status.text = f"Status:  {st}"
        detail_arr.text    = f"Annual revenue:  ${arr:,}"
        detail_seats.text  = f"Seats:  {seats}"
        status(f"Customer → {name}")
        win.invalidate()

    cust_listbox.on_change = render_customer
    btn_save_note.command = lambda: (
        status(f"Note saved for {detail_name.text or 'customer'}."),
        g.show_message_box(win, "Note saved (mock).", title="Saved", style="info"),
    )
    btn_email.command = lambda: status(
        f"Drafting email to {detail_name.text or 'customer'}…"
    )

    # ============================== ORDERS ==============================
    nav_or = g.create_nav_bar(
        win, "Order pipeline", x=0, y=0, width=0,
        subtitle="Filter the live feed of orders below.",
        actions=[{"text": "Refresh", "accent": False},
                 {"text": "Export CSV", "accent": True}],
        tab="orders",
    )

    state_label = g.create_label(win, "State", x=0, y=0, width=80, height=22,
                                 style="caption", tab="orders")
    state_dropdown = g.create_dropdown(
        win, options=["All", *_states], placeholder="All",
        x=0, y=0, width=160, tab="orders",
    )
    min_label = g.create_label(win, "Min total ($)", x=0, y=0, width=120, height=22,
                               style="caption", tab="orders")
    min_slider = g.create_slider(
        win, value=0, minimum=0, maximum=15000,
        x=0, y=0, width=240, tab="orders",
    )
    min_value_label = g.create_label(win, "$0", x=0, y=0, width=80, height=22,
                                     style="caption", tab="orders")
    only_open_switch = g.create_switch(
        win, label="Hide refunded", on=False,
        x=0, y=0, width=180, tab="orders",
    )

    orders_grid = g.create_grid(
        win, ["Order #", "Customer", "Date", "State", "Total"], list(ORDERS),
        x=0, y=0, width=0, row_height=34, tab="orders",
    )

    filter_state = {"state": "All", "min": 0, "hide_refunded": False}

    def apply_filters():
        rows = []
        for row in ORDERS:
            order_state = row[3]
            total = int(row[4].replace("$", "").replace(",", ""))
            if filter_state["state"] != "All" and order_state != filter_state["state"]:
                continue
            if total < filter_state["min"]:
                continue
            if filter_state["hide_refunded"] and order_state == "Refunded":
                continue
            rows.append(row)
        orders_grid.rows = rows
        status(f"Showing {len(rows)} of {len(ORDERS)} orders.")
        win.invalidate()

    def on_state_pick(value):
        filter_state["state"] = value or "All"
        apply_filters()

    def on_min_change(value):
        filter_state["min"] = int(value)
        min_value_label.text = f"${int(value):,}"
        apply_filters()

    def on_only_open(value):
        filter_state["hide_refunded"] = bool(value)
        apply_filters()

    state_dropdown.on_change = on_state_pick
    min_slider.on_change = on_min_change
    only_open_switch.on_change = on_only_open

    # ============================== REPORTS ==============================
    nav_r = g.create_nav_bar(
        win, "Reports library", x=0, y=0, width=0,
        subtitle="Pre-built and saved reports across the workspace.",
        actions=[{"text": "New report", "accent": True}],
        tab="reports",
    )
    chart_region = g.create_chart(
        win, "Revenue by region ($)", REGION_REVENUE,
        x=0, y=0, width=0, height=300, accent="#2563eb", tab="reports",
    )
    chart_weekly = g.create_chart(
        win, "Weekly revenue ($)", WEEKLY_REVENUE,
        x=0, y=0, width=0, height=300, accent="#16a34a", tab="reports",
    )
    saved_panel = g.create_panel(
        win, title="Saved reports", x=0, y=0, width=0, height=260,
        subtitle="Pinned by you and your team.",
        accent="#7c3aed", tab="reports",
    )
    tree_reports = g.create_tree_view(
        win, nodes=PROJECT_TREE, x=0, y=0, width=0, height=200,
        on_select=lambda node: status(f"Report → {node.label}"),
        tooltip="Open a saved report",
        tab="reports",
    )

    # ============================== SETTINGS ==============================
    nav_s = g.create_nav_bar(
        win, "Workspace settings", x=0, y=0, width=0,
        subtitle="Personal preferences for this workstation.",
        tab="settings",
    )
    pref_panel = g.create_panel(
        win, title="Preferences", x=0, y=0, width=0, height=420,
        subtitle="Toggle features on or off.",
        accent="#2563eb", tab="settings",
    )
    profile_panel = g.create_panel(
        win, title="Profile", x=0, y=0, width=0, height=420,
        subtitle="Sign-in & contact information.",
        accent="#16a34a", tab="settings",
    )

    # preferences
    pref_dark   = g.create_switch(win, label="Dark mode preview",       on=False,
                                  x=0, y=0, width=0, tab="settings")
    pref_email  = g.create_switch(win, label="Email me weekly digests", on=True,
                                  x=0, y=0, width=0, tab="settings")
    pref_beta   = g.create_switch(win, label="Enable beta features",    on=False,
                                  x=0, y=0, width=0, tab="settings")

    density_label = g.create_label(win, "Display density", x=0, y=0, width=0, height=22,
                                   style="caption", tab="settings")
    density_radio = g.create_radio_group(
        win,
        options=[("comfy", "Comfortable"), ("cozy", "Cozy"), ("compact", "Compact")],
        selected="cozy", x=0, y=0, width=0, item_height=30, tab="settings",
    )

    progress_label = g.create_label(win, "Storage used", x=0, y=0, width=0, height=22,
                                    style="caption", tab="settings")
    progress_pct   = g.create_label(win, "62%", x=0, y=0, width=60, height=22,
                                    style="caption", tab="settings")
    progress_bar   = g.create_progress_bar(
        win, value=0.62, x=0, y=0, width=0, height=10, show_label=False,
        tab="settings",
    )

    # profile
    name_caption  = g.create_label(win, "Display name", x=0, y=0, width=0, height=22,
                                   style="caption", tab="settings")
    name_input    = g.create_text_input(
        win, placeholder="Jane Doe", x=0, y=0, width=0, height=38, tab="settings",
    )
    email_caption = g.create_label(win, "Email", x=0, y=0, width=0, height=22,
                                   style="caption", tab="settings")
    email_input   = g.create_text_input(
        win, placeholder="jane@northwind.example", x=0, y=0, width=0, height=38,
        tab="settings",
    )
    role_caption  = g.create_label(win, "Role", x=0, y=0, width=0, height=22,
                                   style="caption", tab="settings")
    role_dropdown = g.create_dropdown(
        win, options=["Admin", "Editor", "Viewer"], placeholder="Editor",
        x=0, y=0, width=0, tab="settings",
    )

    btn_save_settings = g.create_button(
        win, "Save changes", x=0, y=0, width=160, height=38,
        accent="#2563eb",
        command=lambda: (status("Settings saved."),
                         g.show_message_box(win, "Settings saved (mock).",
                                            title="Saved", style="info")),
        tab="settings",
    )
    btn_signout = g.create_button(
        win, "Sign out", x=0, y=0, width=120, height=38,
        command=confirm_quit, tab="settings",
    )

    pref_dark.on_change   = lambda v: status(f"Dark mode → {'on' if v else 'off'}")
    pref_email.on_change  = lambda v: status(f"Weekly digests → {'on' if v else 'off'}")
    pref_beta.on_change   = lambda v: status(f"Beta features → {'on' if v else 'off'}")
    density_radio.on_change = lambda k: status(f"Display density → {k}")
    role_dropdown.on_change = lambda v: status(f"Role → {v}")

    # ----- accelerators ---------------------------------------------------
    g.create_accelerator(win, "E", export_csv,   ctrl=True, description="Export CSV")
    g.create_accelerator(win, "Q", confirm_quit, ctrl=True, description="Quit")
    g.create_accelerator(win, "R", refresh_data, ctrl=True, description="Refresh")
    g.create_accelerator(win, 0x70, refresh_data, description="F5 refresh")  # VK_F1=0x70

    # ============================== LAYOUT ==============================
    def layout(w, h):
        cx = win.content_origin_x(padding=PAD)
        cw = max(640, w - cx - PAD)
        bottom_safe = h - STATUS_H - 12

        # status bar pinned to bottom across full width
        status_label.x = 0
        status_label.y = h - STATUS_H
        status_label.width = w

        # Headers
        for lbl in (title_o, title_c, title_or, title_r, title_s):
            lbl.x = cx; lbl.width = max(420, cw)
        for lbl in (sub_o, sub_c, sub_or, sub_r, sub_s):
            lbl.x = cx; lbl.width = max(420, cw)

        nav_y = HEADER_TOP + HEADER_H + 6 + SUBHEADER_H + 18
        for nav in (nav_o, nav_c, nav_or, nav_r, nav_s):
            nav.x = cx; nav.y = nav_y; nav.width = cw

        body_top = nav_y + NAV_H + 18

        # ----- OVERVIEW ----------------------------------------------------
        kc0, kc1, kc2, kc3 = _row(cx, cw, 4, gap=GAP)
        for card, (x, width) in zip(
            (kpi_revenue, kpi_orders, kpi_customers, kpi_churn),
            (kc0, kc1, kc2, kc3),
        ):
            card.x = x; card.width = width; card.y = body_top
        cards_bottom = body_top + kpi_revenue.height + GAP

        chart_w_left, chart_w_right = _row(cx, cw, 2, gap=GAP)
        chart_revenue.x, chart_revenue.width = chart_w_left
        chart_pipeline.x, chart_pipeline.width = chart_w_right
        chart_revenue.y = cards_bottom
        chart_pipeline.y = cards_bottom
        # Charts grow to fill remaining vertical space (above activity)
        activity_h = 180
        max_chart_bottom = bottom_safe - activity_h - GAP
        chart_h = max(180, max_chart_bottom - cards_bottom)
        chart_revenue.height = chart_h
        chart_pipeline.height = chart_h

        panel_activity.x = cx; panel_activity.width = cw
        panel_activity.y = chart_revenue.y + chart_revenue.height + GAP
        panel_activity.height = max(120, bottom_safe - panel_activity.y)
        line_x = cx + 20
        line_y = panel_activity.y + 70
        for label in activity_labels:
            label.x = line_x
            label.y = line_y
            label.width = cw - 40
            line_y += 24

        # ----- CUSTOMERS ---------------------------------------------------
        cust_w, det_w = _row(cx, cw, 2, gap=GAP)
        cust_panel.x, cust_panel.width = cust_w
        detail_panel.x, detail_panel.width = det_w
        cust_panel.y = body_top
        detail_panel.y = body_top
        # panels stretch to bottom safe area
        panel_h = max(360, bottom_safe - body_top)
        cust_panel.height = panel_h
        detail_panel.height = panel_h

        cust_listbox.x = cust_panel.x + 18
        cust_listbox.y = cust_panel.y + 70
        cust_listbox.width = cust_panel.width - 36
        cust_listbox.height = max(160, cust_panel.height - 88)

        # detail panel internals
        dx = detail_panel.x + 20
        dw = detail_panel.width - 40
        dy = detail_panel.y + 70
        for lbl in (detail_name, detail_plan, detail_status, detail_arr, detail_seats):
            lbl.x = dx; lbl.width = dw; lbl.y = dy
            dy += lbl.height + 6
        dy += 12
        note_label.x = dx; note_label.width = dw; note_label.y = dy; dy += 24
        note_input.x = dx; note_input.width = dw; note_input.y = dy
        dy += note_input.height + 14
        btn_save_note.x = dx; btn_save_note.y = dy
        btn_email.x = dx + btn_save_note.width + 10; btn_email.y = dy

        # ----- ORDERS ------------------------------------------------------
        # Filter row
        fy = body_top
        state_label.x = cx; state_label.y = fy; state_label.width = 80
        state_dropdown.x = cx; state_dropdown.y = fy + 22; state_dropdown.width = 160

        min_label.x = cx + 180; min_label.y = fy; min_label.width = 200
        min_slider.x = cx + 180; min_slider.y = fy + 24
        min_slider.width = max(200, min(360, cw - 540))
        min_value_label.x = min_slider.x + min_slider.width + 12
        min_value_label.y = fy + 22; min_value_label.width = 80

        only_open_switch.x = cx + cw - 200
        only_open_switch.y = fy + 18; only_open_switch.width = 200

        grid_y = fy + 70
        orders_grid.x = cx; orders_grid.width = cw
        orders_grid.y = grid_y

        # ----- REPORTS -----------------------------------------------------
        rc0, rc1 = _row(cx, cw, 2, gap=GAP)
        chart_region.x, chart_region.width = rc0
        chart_weekly.x, chart_weekly.width = rc1
        chart_region.y = body_top
        chart_weekly.y = body_top
        report_chart_h = max(220, min(320, (bottom_safe - body_top) // 2 - GAP // 2))
        chart_region.height = report_chart_h
        chart_weekly.height = report_chart_h

        saved_panel.x = cx; saved_panel.width = cw
        saved_panel.y = body_top + report_chart_h + GAP
        saved_panel.height = max(180, bottom_safe - saved_panel.y)
        tree_reports.x = saved_panel.x + 18
        tree_reports.y = saved_panel.y + 70
        tree_reports.width = saved_panel.width - 36
        tree_reports.height = max(120, saved_panel.height - 88)

        # ----- SETTINGS ----------------------------------------------------
        pc0, pc1 = _row(cx, cw, 2, gap=GAP)
        pref_panel.x, pref_panel.width = pc0
        profile_panel.x, profile_panel.width = pc1
        pref_panel.y = body_top
        profile_panel.y = body_top
        s_panel_h = max(380, bottom_safe - body_top)
        pref_panel.height = s_panel_h
        profile_panel.height = s_panel_h

        # preferences body
        px = pref_panel.x + 20
        pw = pref_panel.width - 40
        py = pref_panel.y + 70
        for sw in (pref_dark, pref_email, pref_beta):
            sw.x = px; sw.width = pw; sw.y = py
            py += sw.height + 14
        py += 8
        density_label.x = px; density_label.width = pw; density_label.y = py
        py += 26
        density_radio.x = px; density_radio.width = pw; density_radio.y = py
        py += density_radio.height + 18
        progress_label.x = px; progress_label.width = pw - 70; progress_label.y = py
        progress_pct.x = px + pw - 60; progress_pct.width = 60; progress_pct.y = py
        py += 24
        progress_bar.x = px; progress_bar.width = pw; progress_bar.y = py

        # profile body
        fx = profile_panel.x + 20
        fw = profile_panel.width - 40
        fy2 = profile_panel.y + 70
        for cap, inp in ((name_caption, name_input),
                         (email_caption, email_input),
                         (role_caption, role_dropdown)):
            cap.x = fx; cap.width = fw; cap.y = fy2; fy2 += 24
            inp.x = fx; inp.width = fw; inp.y = fy2
            fy2 += inp.height + 14
        fy2 += 6
        btn_save_settings.x = fx; btn_save_settings.y = fy2
        btn_signout.x = fx + btn_save_settings.width + 10; btn_signout.y = fy2

    win.on_layout(layout)

    # initial state
    render_customer(0)
    apply_filters()
    win.mainloop()


if __name__ == "__main__":
    main()
