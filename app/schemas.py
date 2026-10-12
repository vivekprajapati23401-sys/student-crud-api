"""Request and response validation schemas."""
import re
from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StudentBase(BaseModel):
    name: str = Field(min_length=2, max_length=100, examples=["Aarav Sharma"])
    date_of_birth: date = Field(examples=["2005-06-15"])
    email: str | None = Field(default=None, max_length=254, examples=["aarav@example.com"])
    phone: str | None = Field(default=None, max_length=25, examples=["9876543210"])
    course: str | None = Field(default=None, max_length=100, examples=["B.E. AIML"])
    address: str | None = Field(default=None, max_length=250)
    enrollment_date: date | None = None

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None or not value.strip():
            return None
        value = value.strip().lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
            raise ValueError("Enter a valid email address")
        return value

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, value: str | None) -> str | None:
        if value is None or not value.strip():
            return None
        value = value.strip()
        if not re.fullmatch(r"[+0-9() -]{7,25}", value):
            raise ValueError("Phone can contain digits, spaces, +, parentheses and hyphens")
        return value

    @model_validator(mode="after")
    def require_contact(self):
        if not self.email and not self.phone:
            raise ValueError("Provide at least an email address or phone number")
        return self


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    date_of_birth: date | None = None
    email: str | None = Field(default=None, max_length=254)
    phone: str | None = Field(default=None, max_length=25)
    course: str | None = Field(default=None, max_length=100)
    address: str | None = Field(default=None, max_length=250)
    enrollment_date: date | None = None

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = " ".join(value.split())
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None or not value.strip():
            return None
        value = value.strip().lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
            raise ValueError("Enter a valid email address")
        return value

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, value: str | None) -> str | None:
        if value is None or not value.strip():
            return None
        value = value.strip()
        if not re.fullmatch(r"[+0-9() -]{7,25}", value):
            raise ValueError("Phone can contain digits, spaces, +, parentheses and hyphens")
        return value


class StudentRead(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    student_id: int
