"""CRUD endpoints for student records."""
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Student
from ..schemas import StudentCreate, StudentRead, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED, summary="Create a student")
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    student = Student(**payload.model_dump())
    db.add(student)
    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    return student


@router.get("", response_model=list[StudentRead], summary="List or search students")
def list_students(
    search: str | None = Query(default=None, description="Search by student name, email, or course"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    statement = select(Student).order_by(Student.student_id)
    if search and search.strip():
        term = f"%{search.strip()}%"
        statement = statement.where(or_(Student.name.ilike(term), Student.email.ilike(term), Student.course.ilike(term)))
    return list(db.scalars(statement.offset(skip).limit(limit)).all())


@router.get("/{student_id}", response_model=StudentRead, summary="Get a student by ID")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentRead, summary="Update a student's details")
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(student, field, value)
    # Do not allow a record to lose all contact information.
    if not (student.email or student.phone):
        raise HTTPException(status_code=422, detail="A student must have an email address or phone number")
    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A student with this email already exists")
    return student


@router.patch("/{student_id}", response_model=StudentRead, summary="Partially update a student's details")
def patch_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    return update_student(student_id, payload, db)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a student")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
