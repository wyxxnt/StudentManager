from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from app.database import Base


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(String, default=now_text)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    full_name = Column(String, default="")
    university = Column(String, default="")
    faculty = Column(String, default="")
    group_name = Column(String, default="")
    study_year = Column(String, default="")
    semester_name = Column(String, default="")
    created_at = Column(String, default=now_text)
    updated_at = Column(String, default=now_text)


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String, nullable=False)
    day_of_week = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    room = Column(String, default="")
    teacher = Column(String, default="")


class Homework(Base):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    due_date = Column(String, nullable=False)
    priority = Column(String, default="Середній")
    status = Column(String, default="Не почато")
    created_at = Column(String, default=now_text)


class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    kind = Column(String, default="Інше")
    due_date = Column(String, nullable=False)
    note = Column(Text, default="")
    is_done = Column(Boolean, default=False)
    created_at = Column(String, default=now_text)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, default="")
    created_at = Column(String, default=now_text)
