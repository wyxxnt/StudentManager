from nicegui import ui

from app.helpers import today_for_humans

NAV_ITEMS = [
    ("/dashboard", "Дашборд"),
    ("/schedule", "Розклад"),
    ("/homework", "ДЗ"),
    ("/deadlines", "Дедлайни"),
    ("/notes", "Нотатки"),
    ("/settings", "Налаштування"),
]


def setup_theme():
    ui.colors(
        primary="#176b5b",
        secondary="#f59f00",
        accent="#2f6fed",
        positive="#2b8a3e",
        negative="#c92a2a",
        warning="#e67700",
    )

    ui.add_css(
        """
        body {
            font-family: sans-serif;
            color: #17324d;
            background: #f3f5f7;
        }

        .page-shell {
            width: 100%;
            max-width: 1180px;
            margin: 0 auto;
            padding: 24px 18px 48px 18px;
            gap: 18px;
        }

        .auth-shell {
            width: 100%;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .hero-card, .content-card, .stat-card, .auth-card {
            border-radius: 26px;
            border: 1px solid #e7edf5;
            background: #ffffff;
            box-shadow: 0 18px 40px rgba(30, 41, 59, 0.08);
        }

        .hero-card {
            padding: 24px;
        }

        .content-card, .auth-card {
            padding: 20px;
        }

        .auth-card {
            width: 100%;
            max-width: 430px;
            padding: 24px;
        }

        .auth-actions {
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-top: 8px;
        }

        .stat-card {
            padding: 18px;
            min-width: 0;
            flex: 1;
            height: 100%;
        }

        .big-title {
            font-size: 34px;
            font-weight: 800;
        }

        .mid-title {
            font-size: 24px;
            font-weight: 800;
        }

        .small-title {
            font-size: 18px;
            font-weight: 700;
        }

        .auth-title {
            font-size: 28px;
            font-weight: 800;
        }

        .muted-text {
            color: #5f738a;
            line-height: 1.6;
        }

        .main-button {
            background: #176b5b;
            color: white;
            border-radius: 16px;
            padding: 10px 18px;
            font-weight: 700;
        }

        .auth-link-button {
            padding: 0 18px;
            min-height: 44px;
            background: #eef4f1;
            color: #176b5b;
            font-weight: 700;
            border: 1px solid #b8d3cc;
            border-radius: 16px;
        }

        .item-box {
            border: 1px solid #e7edf5;
            border-radius: 18px;
            background: #f9fbff;
            padding: 14px;
        }

        .wide-row {
            width: 100%;
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            align-items: stretch;
        }

        .grow-one {
            flex: 1;
            min-width: 300px;
        }

        .grow-two {
            flex: 2;
            min-width: 320px;
        }

        .hero-layout {
            width: 100%;
            display: flex;
            justify-content: space-between;
            gap: 24px;
            align-items: flex-start;
        }

        .hero-side {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 10px;
            min-width: 220px;
        }

        .header-actions {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            flex-wrap: wrap;
        }

        .stats-grid {
            width: 100%;
            display: grid !important;
            gap: 16px;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        }

        .dashboard-top-grid {
            width: 100%;
            display: grid !important;
            gap: 16px;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            align-items: stretch;
        }

        .dashboard-bottom-grid {
            width: 100%;
            display: grid !important;
            gap: 16px;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            align-items: stretch;
        }

        @media (max-width: 900px) {
            .hero-layout {
                flex-direction: column;
            }

            .hero-side {
                width: 100%;
                align-items: flex-start;
            }

            .header-actions {
                justify-content: flex-start;
            }

            .dashboard-top-grid,
            .dashboard-bottom-grid {
                grid-template-columns: 1fr;
            }
        }
        """
    )


def render_auth_header(title, subtitle):
    with ui.column().classes("w-full gap-1"):
        ui.label("Studly").style("color: #176b5b; font-size: 13px; font-weight: 800;")
        ui.label(title).classes("auth-title")
        ui.label(subtitle).classes("muted-text")


def render_user_header(user, settings_path=None):
    with ui.card().classes("hero-card w-full"):
        with ui.row().classes("hero-layout"):
            with ui.column().classes("gap-1").style("flex: 1; min-width: 0;"):
                ui.label("Studly").classes("big-title")
            with ui.column().classes("hero-side"):
                ui.label(f"Привіт, {user.username}").classes("small-title")
                ui.label(f"Сьогодні {today_for_humans()}").classes("muted-text")
                with ui.row().classes("header-actions"):
                    if settings_path:
                        action_button = ui.button(on_click=lambda: ui.navigate.to(settings_path), icon="settings")
                        action_button.props("unelevated no-caps")
                        action_button.style("width: 44px; height: 44px; padding: 0; border-radius: 14px; background: #eef4fb; color: #17324d;")

                    with ui.button(icon="menu") as menu_button:
                        menu_button.props("unelevated no-caps")
                        menu_button.classes("main-button")
                        menu_button.style("width: 44px; height: 44px; padding: 0; border-radius: 14px;")
                        with ui.menu():
                            for path, label in NAV_ITEMS:
                                ui.menu_item(label, on_click=lambda path=path: ui.navigate.to(path))
                            ui.menu_item("Вийти", on_click=lambda: ui.navigate.to("/logout"))


def render_stat_card(title, value):
    with ui.card().classes("stat-card"):
        ui.label(title).style("color: #176b5b; font-size: 12px; font-weight: 800; text-transform: uppercase;")
        ui.label(value).style("font-size: 34px; font-weight: 800;")
