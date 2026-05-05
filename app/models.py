from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from app.database import Base


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(60), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(String(30), default=now_text)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    full_name = Column(String(120), default="")
    university = Column(String(120), default="")
    faculty = Column(String(120), default="")
    group_name = Column(String(80), default="")
    study_year = Column(String(20), default="")
    semester_name = Column(String(40), default="")
    created_at = Column(String(30), default=now_text)
    updated_at = Column(String(30), default=now_text)


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    day_of_week = Column(String(20), nullable=False)
    start_time = Column(String(10), nullable=False)
    end_time = Column(String(10), nullable=False)
    room = Column(String(100), default="")
    teacher = Column(String(100), default="")


class Homework(Base):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    title = Column(String(120), nullable=False)
    description = Column(Text, default="")
    due_date = Column(String(20), nullable=False)
    priority = Column(String(20), default="Середній")
    status = Column(String(20), default="Не почато")
    created_at = Column(String(30), default=now_text)


class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(120), nullable=False)
    kind = Column(String(40), default="Інше")
    due_date = Column(String(20), nullable=False)
    note = Column(Text, default="")
    is_done = Column(Boolean, default=False)
    created_at = Column(String(30), default=now_text)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(120), nullable=False)
    content = Column(Text, default="")
    created_at = Column(String(30), default=now_text)
