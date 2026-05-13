import os

from nicegui import ui

from app.database import create_tables
import app.pages.auth
import app.pages.dashboard
import app.pages.deadlines
import app.pages.homework
import app.pages.notes
import app.pages.schedule
import app.pages.settings

create_tables()

ui.run(
    title="Student Manager",
    storage_secret=os.getenv("STORAGE_SECRET", "studly-secret-key"),
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8080")),
)
