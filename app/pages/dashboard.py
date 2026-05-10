from datetime import datetime

from nicegui import ui

from app.database import get_db
from app.helpers import (
    current_day_name,
    get_or_create_profile,
    get_profile_completion,
    get_status_color,
    require_user,
)
from app.layout import render_stat_card, render_user_header, setup_theme
from app.models import Deadline, Homework, Lesson, Note


@ui.page("/dashboard")
def dashboard_page():
    setup_theme()
    user = require_user()
    if not user:
        return

    today = datetime.now().strftime("%Y-%m-%d")
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

    profile = get_or_create_profile(user.id)
    filled_count, total_count = get_profile_completion(profile)

    today_lessons = sorted(today_lessons, key=lambda l: l.start_time)
    upcoming_homeworks = sorted(upcoming_homeworks, key=lambda h: h.due_date)[:5]
    overdue_homeworks = sorted(overdue_homeworks, key=lambda h: h.due_date)[:5]
    upcoming_deadlines = sorted(upcoming_deadlines, key=lambda d: d.due_date)[:5]
    last_notes = sorted(notes, key=lambda n: n.created_at, reverse=True)[:3]

    profile_parts = []
    if profile.faculty:
        profile_parts.append(profile.faculty)
    if profile.group_name:
        profile_parts.append(f"Група {profile.group_name}")
    if profile.study_year:
        profile_parts.append(f"{profile.study_year} курс")
    if profile.semester_name:
        profile_parts.append(profile.semester_name)

    with ui.column().classes("page-shell"):
        render_user_header(
            user,
            "Твій навчальний простір",
            "Розклад, завдання, дедлайни, нотатки та профіль в одному місці.",
            settings_path="/settings",
        )

        with ui.row().classes("stats-grid"):
            render_stat_card("Пари в розкладі", str(len(lessons)), "Скільки всього записано занять")
            render_stat_card("Активне ДЗ", str(len(open_homeworks)), "Що ще не завершено")
            render_stat_card("Дедлайни", str(len(active_deadlines)), "Справи, які ще попереду")
            render_stat_card("Профіль", f"{filled_count}/{total_count}", "Налаштування твого студентського профілю")
            render_stat_card("Прострочене", str(len(overdue_homeworks)), "Завдання, які вже прострочені")

        with ui.row().classes("dashboard-top-grid"):
            with ui.card().classes("content-card w-full").style("height: 100%;"):
                ui.label("Твій профіль").classes("mid-title")
                if filled_count == 0:
                    ui.label("Профіль ще не заповнений. Додай основні дані про себе, щоб сайт був більш персональним і зручним.").classes("muted-text")
                else:
                    if profile.full_name:
                        ui.label(profile.full_name).classes("small-title")
                    if profile.university:
                        ui.label(profile.university).classes("muted-text")
                    if profile_parts:
                        ui.label(" • ".join(profile_parts)).classes("muted-text")
                    ui.label(f"Заповнено {filled_count} з {total_count} полів").classes("muted-text")

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
