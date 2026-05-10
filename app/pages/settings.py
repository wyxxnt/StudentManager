from nicegui import ui

from app.helpers import get_or_create_profile, require_user, update_profile
from app.layout import render_user_header, setup_theme


@ui.page("/settings")
def settings_page():
    setup_theme()
    user = require_user()
    if not user:
        return

    profile = get_or_create_profile(user.id)

    with ui.column().classes("page-shell"):
        render_user_header(
            user,
            "Налаштування профілю",
            "Оновлюй основні дані профілю та навчання.",
        )

        with ui.card().classes("content-card w-full"):
            ui.label("Основна інформація").classes("mid-title")
            full_name = ui.input("Повне ім'я").classes("w-full")
            full_name.value = profile.full_name or ""

            university = ui.input("Навчальний заклад").classes("w-full")
            university.value = profile.university or ""

            faculty = ui.input("Факультет / спеціальність").classes("w-full")
            faculty.value = profile.faculty or ""

            group_name = ui.input("Група").classes("w-full")
            group_name.value = profile.group_name or ""

            study_year = ui.select(["1", "2", "3", "4", "5", "6"], value=profile.study_year or "1", label="Курс").classes("w-full")
            semester_name = ui.input("Семестр").classes("w-full")
            semester_name.value = profile.semester_name or ""

            def save_settings():
                update_profile(
                    user.id,
                    full_name.value,
                    university.value,
                    faculty.value,
                    group_name.value,
                    study_year.value,
                    semester_name.value,
                )
                ui.notify("Налаштування збережено", color="positive")

            save_button = ui.button("Зберегти налаштування", on_click=save_settings)
            save_button.props("unelevated no-caps")
            save_button.classes("main-button")
