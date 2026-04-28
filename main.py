import os
import secrets

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


def get_storage_secret():
    storage_secret = os.getenv("STORAGE_SECRET", "")
    is_railway_runtime = bool(os.getenv("RAILWAY_PROJECT_ID") or os.getenv("RAILWAY_ENVIRONMENT_ID"))

    if is_railway_runtime and not storage_secret:
        raise RuntimeError("STORAGE_SECRET is missing on Railway")

    return storage_secret or secrets.token_hex(32)


ui.run(
    title="Studly",
    storage_secret=get_storage_secret(),
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8080")),
)

