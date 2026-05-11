from nicegui import ui

from app.database import get_db
from app.helpers import (
    current_day_name,
    get_status_color,
    require_user,
    today_text,
)
from app.layout import render_stat_card, render_user_header, setup_theme
from app.models import Deadline, Homework, Lesson, Note


@ui.page("/dashboard")
def dashboard_page():
    setup_theme()
    user = require_user()
    if not user:
        return

    today = today_text()
    day_name = current_day_name()

    db = get_db()
    lessons = db.query(Lesson).filter(Lesson.user_id == user.id).all()
    homeworks = db.query(Homework).filter(Homework.user_id == user.id).all()
    deadlines = db.query(Deadline).filter(Deadline.user_id == user.id).all()
    notes = db.query(Note).filter(Note.user_id == user.id).all()
    db.close()

    open_homeworks = [h for h in homeworks if h.status != "Готово"]
    overdue_homeworks = [h for h in open_homeworks if h.due_date < today]
    upcoming_homeworks = [h for h in open_homeworks if h.due_date >= today]
    active_deadlines = [d for d in deadlines if not d.is_done]
    upcoming_deadlines = [d for d in active_deadlines if d.due_date >= today]
    today_lessons = [l for l in lessons if l.day_of_week == day_name]

    today_lessons = sorted(today_lessons, key=lambda l: l.start_time)
    upcoming_homeworks = sorted(upcoming_homeworks, key=lambda h: h.due_date)[:5]
    overdue_homeworks = sorted(overdue_homeworks, key=lambda h: h.due_date)[:5]
    upcoming_deadlines = sorted(upcoming_deadlines, key=lambda d: d.due_date)[:5]
    last_notes = sorted(notes, key=lambda n: n.created_at, reverse=True)[:3]

    with ui.column().classes("page-shell"):
        render_user_header(user, settings_path="/settings")

        with ui.row().classes("stats-grid"):
            render_stat_card("Пари в розкладі", str(len(lessons)))
            render_stat_card("Активне ДЗ", str(len(open_homeworks)))
            render_stat_card("Дедлайни", str(len(active_deadlines)))
            render_stat_card("Прострочене", str(len(overdue_homeworks)))

        with ui.row().classes("dashboard-top-grid"):
            with ui.card().classes("content-card w-full").style("height: 100%;"):
                ui.label("Пари на сьогодні").classes("mid-title")
                if not today_lessons:
                    ui.label("На сьогодні пар поки немає.").classes("muted-text")
                for lesson in today_lessons:
                    with ui.card().classes("item-box w-full"):
                        ui.label(f"{lesson.start_time} - {lesson.end_time}").classes("small-title")
                        ui.label(lesson.subject)
                        if lesson.room:
                            ui.label(f"Аудиторія: {lesson.room}").classes("muted-text")
                        if lesson.teacher:
                            ui.label(f"Викладач: {lesson.teacher}").classes("muted-text")

        with ui.row().classes("dashboard-bottom-grid"):
            with ui.card().classes("content-card w-full").style("height: 100%;"):
                ui.label("Домашні завдання").classes("mid-title")
                if not overdue_homeworks and not upcoming_homeworks:
                    ui.label("Активного ДЗ зараз немає.").classes("muted-text")
                if overdue_homeworks:
                    ui.label("Спочатку зверни увагу на прострочені завдання.").classes("muted-text")
                    for work in overdue_homeworks:
                        with ui.card().classes("item-box w-full").style("border-color: #ffd8d8; background: #fff5f5;"):
                            ui.label(f"{work.subject}: {work.title}").classes("small-title")
                            ui.label(f"Було до {work.due_date}").classes("muted-text")
                for work in upcoming_homeworks:
                    with ui.card().classes("item-box w-full"):
                        with ui.row().classes("w-full").style("justify-content: space-between; align-items: center;"):
                            ui.label(f"{work.subject}: {work.title}").classes("small-title")
                            ui.badge(work.status, color=get_status_color(work.status))
                        ui.label(f"До {work.due_date}").classes("muted-text")

            with ui.card().classes("content-card w-full").style("height: 100%;"):
                ui.label("Найближчі дедлайни").classes("mid-title")
                if not upcoming_deadlines:
                    ui.label("Список дедлайнів поки пустий.").classes("muted-text")
                for deadline in upcoming_deadlines:
                    with ui.card().classes("item-box w-full"):
                        ui.label(deadline.title).classes("small-title")
                        ui.label(f"{deadline.kind} • {deadline.due_date}").classes("muted-text")
                        if deadline.note:
                            ui.label(deadline.note).classes("muted-text")

            with ui.card().classes("content-card w-full").style("height: 100%;"):
                ui.label("Останні нотатки").classes("mid-title")
                if not last_notes:
                    ui.label("Нотаток ще немає.").classes("muted-text")
                for note in last_notes:
                    with ui.card().classes("item-box w-full"):
                        ui.label(note.title).classes("small-title")
                        text = note.content
                        if len(text) > 160:
                            text = text[:160] + "..."
                        ui.label(text).classes("muted-text")
