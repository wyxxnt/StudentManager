from nicegui import ui

from app.helpers import authenticate_user, get_current_user, login_user, logout_user, register_new_user
from app.layout import render_auth_header, setup_theme


@ui.page("/")
def index_page():
    setup_theme()
    user = get_current_user()
    if user:
        ui.navigate.to("/dashboard")
        return
    ui.navigate.to("/login")


def build_login_form():
    with ui.card().classes("auth-card"):
        render_auth_header(
            "Вхід",
            "Увійди в акаунт і далі вже працюй зі своїм розкладом, ДЗ і дедлайнами.",
        )

        email = ui.input("Email").classes("w-full")
        password = ui.input("Пароль").classes("w-full")
        password.props("type=password")

        def do_login():
            ok, message, user = authenticate_user(email.value, password.value)
            if not ok:
                ui.notify(message, color="negative")
                return

            login_user(user)
            ui.notify(message, color="positive")
            ui.navigate.to("/dashboard")

        with ui.row().classes("auth-actions"):
            login_button = ui.button("Увійти", on_click=do_login)
            login_button.props("unelevated no-caps")
            login_button.classes("main-button")

            register_button = ui.button("Створити акаунт", on_click=lambda: ui.navigate.to("/register"))
            register_button.props("flat no-caps")
            register_button.classes("auth-link-button")


def build_register_form():
    with ui.card().classes("auth-card"):
        render_auth_header(
            "Реєстрація",
            "Створи акаунт і після цього одразу перейдеш у свій кабінет.",
        )

        username = ui.input("Ім'я").classes("w-full")
        email = ui.input("Email").classes("w-full")
        password = ui.input("Пароль").classes("w-full")
        password.props("type=password")
        confirm_password = ui.input("Повтори пароль").classes("w-full")
        confirm_password.props("type=password")

        def do_register():
            if password.value != confirm_password.value:
                ui.notify("Паролі не співпадають", color="negative")
                return

            ok, message, user = register_new_user(username.value, email.value, password.value)
            if not ok:
                ui.notify(message, color="negative")
                return

            login_user(user)
            ui.notify(message, color="positive")
            ui.navigate.to("/dashboard")

        with ui.row().classes("auth-actions"):
            create_button = ui.button("Зареєструватися", on_click=do_register)
            create_button.props("unelevated no-caps")
            create_button.classes("main-button")

            login_button = ui.button("У мене вже є акаунт", on_click=lambda: ui.navigate.to("/login"))
            login_button.props("flat no-caps")
            login_button.classes("auth-link-button")


@ui.page("/register")
def register_page():
    setup_theme()
    if get_current_user():
        ui.navigate.to("/dashboard")
        return

    with ui.column().classes("auth-shell"):
        build_register_form()


@ui.page("/login")
def login_page():
    setup_theme()
    if get_current_user():
        ui.navigate.to("/dashboard")
        return

    with ui.column().classes("auth-shell"):
        build_login_form()


@ui.page("/logout")
def logout_page():
    logout_user()
    ui.navigate.to("/login")
