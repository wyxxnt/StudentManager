from nicegui import ui

from app.database import get_db
from app.helpers import get_priority_color, get_status_color, require_user
from app.layout import render_user_header, setup_theme
from app.models import Homework


@ui.page("/homework")
def homework_page():
    setup_theme()
    user = require_user()
    if not user:
        return

    def add_homework():
        if not subject.value or not title.value or not due_date.value:
            ui.notify("Заповни предмет, назву і дату", color="negative")
            return

        db = get_db()
        work = Homework(
            user_id=user.id,
            subject=subject.value.strip(),
            title=title.value.strip(),
            description=description.value.strip(),
            due_date=due_date.value,
            priority=priority.value,
        )
        db.add(work)
        db.commit()
        db.close()

        ui.notify("Домашнє завдання додано", color="positive")
        subject.value = ""
        title.value = ""
        description.value = ""
        due_date.value = ""
        priority.value = "Середній"
        homework_list.refresh()

    def open_edit_homework(homework_id):
        db = get_db()
        work = db.query(Homework).filter(Homework.id == homework_id, Homework.user_id == user.id).first()
        db.close()

        if not work:
            ui.notify("Завдання не знайдено", color="negative")
            return

        with ui.dialog() as dialog, ui.card().classes("auth-card"):
            ui.label("Редагувати ДЗ").classes("mid-title")
            edit_subject = ui.input("Предмет", value=work.subject).classes("w-full")
            edit_title = ui.input("Назва завдання", value=work.title).classes("w-full")
            edit_description = ui.textarea("Опис", value=work.description).classes("w-full")
            edit_due_date = ui.input("Дедлайн", value=work.due_date).classes("w-full")
            edit_due_date.props("type=date")
            edit_priority = ui.select(["Низький", "Середній", "Високий"], value=work.priority, label="Пріоритет").classes("w-full")

            def save_homework():
                if not edit_subject.value or not edit_title.value or not edit_due_date.value:
                    ui.notify("Заповни предмет, назву і дату", color="negative")
                    return

                db = get_db()
                work = db.query(Homework).filter(Homework.id == homework_id, Homework.user_id == user.id).first()
                if work:
                    work.subject = edit_subject.value.strip()
                    work.title = edit_title.value.strip()
                    work.description = edit_description.value.strip()
                    work.due_date = edit_due_date.value
                    work.priority = edit_priority.value
                    db.commit()
                db.close()

                dialog.close()
                ui.notify("Завдання оновлено", color="positive")
                homework_list.refresh()

            save_button = ui.button("Зберегти", on_click=save_homework)
            save_button.props("unelevated no-caps")
            save_button.classes("main-button")

        dialog.open()

    def update_status(homework_id, new_status):
        db = get_db()
        work = db.query(Homework).filter(Homework.id == homework_id, Homework.user_id == user.id).first()
        if work:
            work.status = new_status
            db.commit()
        db.close()
        homework_list.refresh()

    def delete_homework(homework_id):
        db = get_db()
        work = db.query(Homework).filter(Homework.id == homework_id, Homework.user_id == user.id).first()
        if work:
            db.delete(work)
            db.commit()
        db.close()
        ui.notify("ДЗ видалено", color="warning")
        homework_list.refresh()

    @ui.refreshable
    def homework_list():
        db = get_db()
        works = db.query(Homework).filter(Homework.user_id == user.id).all()
        db.close()
        works = sorted(works, key=lambda w: (w.status == "Готово", w.due_date, w.subject))

        with ui.column().classes("w-full gap-4"):
            if not works:
                with ui.card().classes("content-card w-full"):
                    ui.label("ДЗ поки немає").classes("mid-title")
                    ui.label("Додай завдання і слідкуй за ним тут.").classes("muted-text")

            for work in works:
                with ui.card().classes("content-card w-full"):
                    with ui.row().classes("w-full").style("justify-content: space-between; gap: 16px; align-items: center;"):
                        with ui.column().classes("gap-1"):
                            ui.label(f"{work.subject}: {work.title}").classes("mid-title")
                            ui.label(f"До {work.due_date}").classes("muted-text")
                        with ui.row().style("gap: 8px; flex-wrap: wrap;"):
                            ui.badge(work.priority, color=get_priority_color(work.priority))
                            ui.badge(work.status, color=get_status_color(work.status))

                    if work.description:
                        ui.label(work.description).classes("muted-text")

                    with ui.row().classes("w-full").style("gap: 10px; flex-wrap: wrap;"):
                        edit_button = ui.button("Редагувати", on_click=lambda i=work.id: open_edit_homework(i))
                        edit_button.props("flat no-caps")

                        start_button = ui.button("Не почато", on_click=lambda i=work.id: update_status(i, "Не почато"))
                        start_button.props("flat no-caps")

                        process_button = ui.button("В процесі", on_click=lambda i=work.id: update_status(i, "В процесі"))
                        process_button.props("flat no-caps")

                        done_button = ui.button("Готово", on_click=lambda i=work.id: update_status(i, "Готово"))
                        done_button.props("flat no-caps color=positive")

                        delete_button = ui.button("Видалити", on_click=lambda i=work.id: delete_homework(i))
                        delete_button.props("flat no-caps color=negative")

    with ui.column().classes("page-shell"):
        render_user_header(user)

        with ui.row().classes("wide-row"):
            with ui.card().classes("content-card grow-one"):
                ui.label("Додати ДЗ").classes("mid-title")
                subject = ui.input("Предмет").classes("w-full")
                title = ui.input("Назва завдання").classes("w-full")
                description = ui.textarea("Опис").classes("w-full")
                due_date = ui.input("Дедлайн").classes("w-full")
                due_date.props("type=date")
                priority = ui.select(["Низький", "Середній", "Високий"], value="Середній", label="Пріоритет").classes("w-full")

                add_button = ui.button("Додати завдання", on_click=add_homework)
                add_button.props("unelevated no-caps")
                add_button.classes("main-button")

            with ui.column().classes("grow-two"):
                homework_list()
