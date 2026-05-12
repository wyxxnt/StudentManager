from nicegui import ui

from app.database import get_db
from app.helpers import WEEK_DAYS, require_user, sort_lessons
from app.layout import render_user_header, setup_theme
from app.models import Lesson


@ui.page("/schedule")
def schedule_page():
    setup_theme()
    user = require_user()
    if not user:
        return

    def add_lesson():
        if not subject.value or not day_of_week.value or not start_time.value or not end_time.value:
            ui.notify("Заповни предмет, день і час", color="negative")
            return

        db = get_db()
        lesson = Lesson(
            user_id=user.id,
            subject=subject.value.strip(),
            day_of_week=day_of_week.value,
            start_time=start_time.value,
            end_time=end_time.value,
            room=room.value.strip(),
            teacher=teacher.value.strip(),
        )
        db.add(lesson)
        db.commit()
        db.close()

        ui.notify("Пару додано", color="positive")
        subject.value = ""
        start_time.value = ""
        end_time.value = ""
        room.value = ""
        teacher.value = ""
        lessons_list.refresh()

    def open_edit_lesson(lesson_id):
        db = get_db()
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.user_id == user.id).first()
        db.close()

        if not lesson:
            ui.notify("Запис не знайдено", color="negative")
            return

        with ui.dialog() as dialog, ui.card().classes("auth-card"):
            ui.label("Редагувати пару").classes("mid-title")
            edit_subject = ui.input("Предмет", value=lesson.subject).classes("w-full")
            edit_day = ui.select(WEEK_DAYS, value=lesson.day_of_week, label="День тижня").classes("w-full")
            edit_start = ui.input("Початок", value=lesson.start_time).classes("w-full")
            edit_start.props("type=time")
            edit_end = ui.input("Кінець", value=lesson.end_time).classes("w-full")
            edit_end.props("type=time")
            edit_room = ui.input("Аудиторія", value=lesson.room).classes("w-full")
            edit_teacher = ui.input("Викладач", value=lesson.teacher).classes("w-full")

            def save_lesson():
                if not edit_subject.value or not edit_day.value or not edit_start.value or not edit_end.value:
                    ui.notify("Заповни предмет, день і час", color="negative")
                    return

                db = get_db()
                lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.user_id == user.id).first()
                if lesson:
                    lesson.subject = edit_subject.value.strip()
                    lesson.day_of_week = edit_day.value
                    lesson.start_time = edit_start.value
                    lesson.end_time = edit_end.value
                    lesson.room = edit_room.value.strip()
                    lesson.teacher = edit_teacher.value.strip()
                    db.commit()
                db.close()

                dialog.close()
                ui.notify("Пару оновлено", color="positive")
                lessons_list.refresh()

            save_button = ui.button("Зберегти", on_click=save_lesson)
            save_button.props("unelevated no-caps")
            save_button.classes("main-button")

        dialog.open()

    def delete_lesson(lesson_id):
        db = get_db()
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.user_id == user.id).first()
        if lesson:
            db.delete(lesson)
            db.commit()
        db.close()

        ui.notify("Запис видалено", color="warning")
        lessons_list.refresh()

    @ui.refreshable
    def lessons_list():
        db = get_db()
        lessons = db.query(Lesson).filter(Lesson.user_id == user.id).all()
        db.close()
        lessons = sort_lessons(lessons)

        with ui.column().classes("w-full gap-4"):
            if not lessons:
                with ui.card().classes("content-card w-full"):
                    ui.label("Розклад поки пустий").classes("mid-title")
                    ui.label("Додай хоча б одну пару, і вона з'явиться тут.").classes("muted-text")

            for day in WEEK_DAYS:
                day_lessons = [l for l in lessons if l.day_of_week == day]
                if not day_lessons:
                    continue

                with ui.card().classes("content-card w-full"):
                    ui.label(day).classes("mid-title")
                    for lesson in day_lessons:
                        with ui.card().classes("item-box w-full"):
                            with ui.row().classes("w-full").style("justify-content: space-between; gap: 12px; align-items: center;"):
                                with ui.column().classes("gap-1"):
                                    ui.label(f"{lesson.start_time} - {lesson.end_time}").classes("small-title")
                                    ui.label(lesson.subject)
                                    extra = []
                                    if lesson.room:
                                        extra.append(f"Аудиторія: {lesson.room}")
                                    if lesson.teacher:
                                        extra.append(f"Викладач: {lesson.teacher}")
                                    if extra:
                                        ui.label(" | ".join(extra)).classes("muted-text")

                                edit_button = ui.button("Редагувати", on_click=lambda i=lesson.id: open_edit_lesson(i))
                                edit_button.props("flat no-caps")

                                delete_button = ui.button("Видалити", on_click=lambda i=lesson.id: delete_lesson(i))
                                delete_button.props("flat no-caps color=negative")

    with ui.column().classes("page-shell"):
        render_user_header(user)

        with ui.row().classes("wide-row"):
            with ui.card().classes("content-card grow-one"):
                ui.label("Додати пару").classes("mid-title")
                subject = ui.input("Предмет").classes("w-full")
                day_of_week = ui.select(WEEK_DAYS, value="Понеділок", label="День тижня").classes("w-full")
                start_time = ui.input("Початок").classes("w-full")
                start_time.props("type=time")
                end_time = ui.input("Кінець").classes("w-full")
                end_time.props("type=time")
                room = ui.input("Аудиторія").classes("w-full")
                teacher = ui.input("Викладач").classes("w-full")

                add_button = ui.button("Додати в розклад", on_click=add_lesson)
                add_button.props("unelevated no-caps")
                add_button.classes("main-button")

            with ui.column().classes("grow-two"):
                lessons_list()
