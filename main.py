"""Application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.routes.students import router as students_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the SQLite table automatically when the application starts.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Students Database CRUD API",
    description="A beginner-friendly FastAPI and SQLite project for managing student records.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(students_router)


@app.get("/", tags=["Health"], summary="Check API status")
def home():
    return {"message": "Students Database CRUD API is running", "docs": "/docs"}


@app.get("/health", tags=["Health"], summary="Health check")
def health():
    return {"status": "ok"}
