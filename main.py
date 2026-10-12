"""Application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import Base, engine
from app.routes.students import router as students_router


# Locate the templates folder inside the project.
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the SQLite table automatically when the application starts.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Students Database CRUD API",
    description=(
        "A beginner-friendly FastAPI and SQLite project "
        "for managing student records."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Keep all existing student CRUD endpoints.
app.include_router(students_router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.get("/health", tags=["Health"], summary="Health check")
def health():
    return {"status": "ok"}
