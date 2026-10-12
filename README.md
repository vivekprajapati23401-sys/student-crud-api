# Students Database CRUD API

A Python backend mini-project for the EWB internship assignment. It uses **FastAPI**, **SQLite**, and **SQLAlchemy** to create, read, update, search, and delete student records.

## Features

- Create student records
- List all students with optional search by name, email, or course
- Retrieve one student by ID
- Update all or selected fields
- Delete a student
- Input validation and useful HTTP error responses
- SQLite data persists between server restarts
- Interactive API documentation with Swagger UI

## Student fields

- `student_id`: automatically generated unique ID
- `name` and `date_of_birth`: required
- `email` and `phone`: provide at least one
- `course`, `address`, and `enrollment_date`: optional

Use only dummy/sample data while testing. Do not upload real students' personal information.

## Requirements

- Python 3.10 or newer
- pip

## Setup on Windows (PowerShell)

Open a terminal in this project folder and run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
venv\Scripts\activate.bat
```

Then run the installation and Uvicorn commands above.

## Open the API

- API home: http://127.0.0.1:8000/
- Swagger UI (test endpoints): http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

The `students.db` SQLite database and its table are created automatically on first startup.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/students` | Create a student |
| `GET` | `/students` | List students |
| `GET` | `/students?search=aarav` | Search by name, email, or course |
| `GET` | `/students/{student_id}` | Get one student |
| `PUT` | `/students/{student_id}` | Update supplied fields |
| `PATCH` | `/students/{student_id}` | Partially update supplied fields |
| `DELETE` | `/students/{student_id}` | Delete a student |

## Sample create request

In Swagger UI, open `POST /students`, click **Try it out**, and submit:

```json
{
  "name": "Aarav Sharma",
  "date_of_birth": "2005-06-15",
  "email": "aarav@example.com",
  "phone": "9876543210",
  "course": "B.E. AIML",
  "address": "Mumbai",
  "enrollment_date": "2026-07-01"
}
```

## Sample update request

For `PATCH /students/1`, send only the fields to change:

```json
{
  "course": "B.E. Artificial Intelligence and Machine Learning"
}
```

## Common responses

- `201 Created`: student created
- `200 OK`: data returned or updated
- `204 No Content`: student deleted
- `404 Not Found`: student ID does not exist
- `409 Conflict`: duplicate email
- `422 Unprocessable Entity`: invalid input

## GitHub submission checklist

1. Create a public GitHub repository, for example `student-crud-api`.
2. Upload the project source files; do not upload `venv/`, `students.db`, or personal data.
3. Keep this README and `requirements.txt` in the repository.
4. Copy the repository URL into the EWB submission form's GitHub Link field.
5. The assignment's optional Ollama AI extension is not included in this core version. Complete and test CRUD first; add AI only if time and hardware allow.
