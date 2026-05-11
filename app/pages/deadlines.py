from nicegui import ui

from app.database import get_db
from app.helpers import require_user
from app.layout import render_user_header, setup_theme
from app.models import Deadline


@ui.page("/deadlines")
def deadlines_page():
    setup_theme()
    user = require_user()
    if not user:
        return

    def add_deadline():
        if not title.value or not due_date.value:
            ui.notify("Заповни назву і дату", color="negative")
            return

        db = get_db()
        item = Deadline(
            user_id=user.id,
            title=title.value.strip(),
            kind=kind.value,
            due_date=due_date.value,
            note=note.value.strip(),
        )
        db.add(item)
        db.commit()
        db.close()

        ui.notify("Дедлайн додано", color="positive")
        title.value = ""
        kind.value = "Інше"
        due_date.value = ""
        note.value = ""
        deadlines_list.refresh()

    def open_edit_deadline(deadline_id):
        db = get_db()
        item = db.query(Deadline).filter(Deadline.id == deadline_id, Deadline.user_id == user.id).first()
        db.close()

        if not item:
            ui.notify("Дедлайн не знайдено", color="negative")
            return

        with ui.dialog() as dialog, ui.card().classes("auth-card"):
            ui.label("Редагувати дедлайн").classes("mid-title")
            edit_title = ui.input("Назва", value=item.title).classes("w-full")
            edit_kind = ui.select(["Контрольна", "Проєкт", "Екзамен", "Залік", "Інше"], value=item.kind, label="Тип").classes("w-full")
            edit_due_date = ui.input("Дата", value=item.due_date).classes("w-full")
            edit_due_date.props("type=date")
            edit_note = ui.textarea("Нотатка", value=item.note).classes("w-full")

            def save_deadline():
                if not edit_title.value or not edit_due_date.value:
                    ui.notify("Заповни назву і дату", color="negative")
                    return

                db = get_db()
                item = db.query(Deadline).filter(Deadline.id == deadline_id, Deadline.user_id == user.id).first()
                if item:
                    item.title = edit_title.value.strip()
                    item.kind = edit_kind.value
                    item.due_date = edit_due_date.value
                    item.note = edit_note.value.strip()
                    db.commit()
                db.close()

                dialog.close()
                ui.notify("Дедлайн оновлено", color="positive")
                deadlines_list.refresh()

            save_button = ui.button("Зберегти", on_click=save_deadline)
            save_button.props("unelevated no-caps")
            save_button.classes("main-button")

        dialog.open()

    def toggle_deadline(deadline_id):
        db = get_db()
        item = db.query(Deadline).filter(Deadline.id == deadline_id, Deadline.user_id == user.id).first()
        if item:
            item.is_done = not item.is_done
            db.commit()
        db.close()
        deadlines_list.refresh()

    def delete_deadline(deadline_id):
        db = get_db()
        item = db.query(Deadline).filter(Deadline.id == deadline_id, Deadline.user_id == user.id).first()
        if item:
            db.delete(item)
            db.commit()
        db.close()
        ui.notify("Дедлайн видалено", color="warning")
        deadlines_list.refresh()

    @ui.refreshable
    def deadlines_list():
        db = get_db()
        items = db.query(Deadline).filter(Deadline.user_id == user.id).all()
        db.close()
        items = sorted(items, key=lambda i: (i.is_done, i.due_date))

        with ui.column().classes("w-full gap-4"):
            if not items:
                with ui.card().classes("content-card w-full"):
                    ui.label("Дедлайнів поки немає").classes("mid-title")
                    ui.label("Записуй сюди контрольні, проєкти, заліки і все важливе.").classes("muted-text")

            for item in items:
                with ui.card().classes("content-card w-full"):
                    with ui.row().classes("w-full").style("justify-content: space-between; gap: 16px; align-items: center;"):
                        with ui.column().classes("gap-1"):
                            ui.label(item.title).classes("mid-title")
                            ui.label(f"{item.kind} • {item.due_date}").classes("muted-text")
                        ui.badge("Готово" if item.is_done else "Активно", color="positive" if item.is_done else "warning")

                    if item.note:
                        ui.label(item.note).classes("muted-text")

                    with ui.row().classes("w-full").style("gap: 10px; flex-wrap: wrap;"):
                        edit_button = ui.button("Редагувати", on_click=lambda i=item.id: open_edit_deadline(i))
                        edit_button.props("flat no-caps")

                        toggle_button = ui.button("Перемкнути статус", on_click=lambda i=item.id: toggle_deadline(i))
                        toggle_button.props("flat no-caps")

                        delete_button = ui.button("Видалити", on_click=lambda i=item.id: delete_deadline(i))
                        delete_button.props("flat no-caps color=negative")

    with ui.column().classes("page-shell"):
        render_user_header(user)

        with ui.row().classes("wide-row"):
            with ui.card().classes("content-card grow-one"):
                ui.label("Додати дедлайн").classes("mid-title")
                title = ui.input("Назва").classes("w-full")
                kind = ui.select(["Контрольна", "Проєкт", "Екзамен", "Залік", "Інше"], value="Інше", label="Тип").classes("w-full")
                due_date = ui.input("Дата").classes("w-full")
                due_date.props("type=date")
                note = ui.textarea("Нотатка").classes("w-full")

                add_button = ui.button("Додати дедлайн", on_click=add_deadline)
                add_button.props("unelevated no-caps")
                add_button.classes("main-button")

            with ui.column().classes("grow-two"):
                deadlines_list()
