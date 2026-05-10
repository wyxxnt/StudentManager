from nicegui import ui

from app.database import get_db
from app.helpers import require_user
from app.layout import render_user_header, setup_theme
from app.models import Note


@ui.page("/notes")
def notes_page():
    setup_theme()
    user = require_user()
    if not user:
        return

    def add_note():
        if not title.value or not content.value:
            ui.notify("Заповни назву і текст нотатки", color="negative")
            return

        db = get_db()
        item = Note(
            user_id=user.id,
            title=title.value.strip(),
            content=content.value.strip(),
        )
        db.add(item)
        db.commit()
        db.close()

        ui.notify("Нотатку збережено", color="positive")
        title.value = ""
        content.value = ""
        notes_list.refresh()

    def open_edit_note(note_id):
        db = get_db()
        item = db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()
        db.close()

        if not item:
            ui.notify("Нотатку не знайдено", color="negative")
            return

        with ui.dialog() as dialog, ui.card().classes("auth-card"):
            ui.label("Редагувати нотатку").classes("mid-title")
            edit_title = ui.input("Назва", value=item.title).classes("w-full")
            edit_content = ui.textarea("Текст", value=item.content).classes("w-full")

            def save_note():
                if not edit_title.value or not edit_content.value:
                    ui.notify("Заповни назву і текст нотатки", color="negative")
                    return

                db = get_db()
                item = db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()
                if item:
                    item.title = edit_title.value.strip()
                    item.content = edit_content.value.strip()
                    db.commit()
                db.close()

                dialog.close()
                ui.notify("Нотатку оновлено", color="positive")
                notes_list.refresh()

            save_button = ui.button("Зберегти", on_click=save_note)
            save_button.props("unelevated no-caps")
            save_button.classes("main-button")

        dialog.open()

    def delete_note(note_id):
        db = get_db()
        item = db.query(Note).filter(Note.id == note_id, Note.user_id == user.id).first()
        if item:
            db.delete(item)
            db.commit()
        db.close()
        ui.notify("Нотатку видалено", color="warning")
        notes_list.refresh()

    @ui.refreshable
    def notes_list():
        db = get_db()
        items = db.query(Note).filter(Note.user_id == user.id).all()
        db.close()
        items = sorted(items, key=lambda i: i.created_at, reverse=True)

        with ui.column().classes("w-full gap-4"):
            if not items:
                with ui.card().classes("content-card w-full"):
                    ui.label("Нотаток поки немає").classes("mid-title")
                    ui.label("Записуй сюди ідеї, нагадування або короткі конспекти.").classes("muted-text")

            for item in items:
                with ui.card().classes("content-card w-full"):
                    with ui.row().classes("w-full").style("justify-content: space-between; gap: 16px; align-items: center;"):
                        with ui.column().classes("gap-1"):
                            ui.label(item.title).classes("mid-title")
                            ui.label(item.created_at).classes("muted-text")
                        with ui.row().style("gap: 8px;"):
                            edit_button = ui.button("Редагувати", on_click=lambda i=item.id: open_edit_note(i))
                            edit_button.props("flat no-caps")

                            delete_button = ui.button("Видалити", on_click=lambda i=item.id: delete_note(i))
                            delete_button.props("flat no-caps color=negative")
                    ui.label(item.content).classes("muted-text")

    with ui.column().classes("page-shell"):
        render_user_header(
            user,
            "Нотатки",
            "Місце для коротких ідей, нагадувань і всього, що не хочеться загубити.",
        )

        with ui.row().classes("wide-row"):
            with ui.card().classes("content-card grow-one"):
                ui.label("Нова нотатка").classes("mid-title")
                title = ui.input("Назва").classes("w-full")
                content = ui.textarea("Текст").classes("w-full")

                add_button = ui.button("Зберегти нотатку", on_click=add_note)
                add_button.props("unelevated no-caps")
                add_button.classes("main-button")

            with ui.column().classes("grow-two"):
                notes_list()
