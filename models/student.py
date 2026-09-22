"""Student data model representing a student with ID, Name, Score, and Grade."""
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Student:
    student_id: str
    name: str
    score: float

    def __post_init__(self) -> None:
        if not isinstance(self.student_id, str) or not self.student_id.strip():
            raise ValueError("Student ID must be a non-empty string.")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Student name must be a non-empty string.")
        try:
            self.score = float(self.score)
        except (ValueError, TypeError):
            raise ValueError(f"Score must be a valid number, got: {self.score}")

        if not (0.0 <= self.score <= 100.0):
            raise ValueError(f"Score must be between 0.0 and 100.0, got: {self.score}")

        self.student_id = self.student_id.strip()
        self.name = self.name.strip()

    @property
    def grade(self) -> str:
        """Calculate letter grade based on standard scoring criteria."""
        if self.score >= 80.0:
            return "A"
        elif self.score >= 75.0:
            return "B+"
        elif self.score >= 70.0:
            return "B"
        elif self.score >= 65.0:
            return "C+"
        elif self.score >= 60.0:
            return "C"
        elif self.score >= 55.0:
            return "D+"
        elif self.score >= 50.0:
            return "D"
        else:
            return "F"

    def to_dict(self) -> Dict[str, Any]:
        """Convert student object to a dictionary."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "score": self.score,
            "grade": self.grade,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Create a Student instance from a dictionary."""
        return cls(
            student_id=str(data["student_id"]),
            name=str(data["name"]),
            score=float(data["score"]),
        )

    def __str__(self) -> str:
        return f"Student(ID: {self.student_id}, Name: {self.name}, Score: {self.score:.1f}, Grade: {self.grade})"
