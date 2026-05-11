from datetime import datetime

from nicegui import app, ui
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_db
from app.models import User, UserProfile

WEEK_DAYS = [
    "Понеділок",
    "Вівторок",
    "Середа",
    "Четвер",
    "П'ятниця",
    "Субота",
    "Неділя",
]


def today_text():
    return datetime.now().strftime("%Y-%m-%d")


def today_for_humans():
    return datetime.now().strftime("%d.%m.%Y")


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def current_day_name():
    return WEEK_DAYS[datetime.now().weekday()]


def sort_lessons(lessons):
    return sorted(lessons, key=lambda l: (WEEK_DAYS.index(l.day_of_week), l.start_time))


def get_status_color(status):
    if status == "Готово":
        return "positive"
    if status == "В процесі":
        return "primary"
    return "warning"


def get_priority_color(priority):
    if priority == "Високий":
        return "negative"
    if priority == "Середній":
        return "warning"
    return "primary"


def login_user(user):
    app.storage.user["user_id"] = user.id
    app.storage.user["username"] = user.username


def logout_user():
    app.storage.user.clear()


def get_current_user():
    user_id = app.storage.user.get("user_id")
    if not user_id:
        return None

    db = get_db()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user


def require_user():
    user = get_current_user()
    if not user:
        ui.navigate.to("/login")
        return None
    return user


def register_new_user(username, email, password):
    username = username.strip()
    email = email.strip().lower()

    if len(username) < 2:
        return False, "Ім'я занадто коротке", None
    if "@" not in email:
        return False, "Введи нормальний email", None
    if len(password) < 4:
        return False, "Пароль має бути хоча б 4 символи", None

    db = get_db()
    if db.query(User).filter(User.email == email).first():
        db.close()
        return False, "Користувач з таким email вже існує", None

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return True, "Акаунт створено", user


def authenticate_user(email, password):
    email = email.strip().lower()

    db = get_db()
    user = db.query(User).filter(User.email == email).first()
    db.close()

    if not user:
        return False, "Такого користувача немає", None

    if not check_password_hash(user.password_hash, password):
        return False, "Неправильний пароль", None

    return True, "Вхід успішний", user


def get_or_create_profile(user_id):
    db = get_db()
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    db.close()
    return profile


def update_profile(user_id, full_name, university, faculty, group_name, study_year, semester_name):
    db = get_db()
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)

    profile.full_name = full_name.strip()
    profile.university = university.strip()
    profile.faculty = faculty.strip()
    profile.group_name = group_name.strip()
    profile.study_year = study_year.strip()
    profile.semester_name = semester_name.strip()
    profile.updated_at = now_text()

    db.commit()
    db.close()
