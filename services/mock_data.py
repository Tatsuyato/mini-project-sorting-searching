"""Synthetic mock student data generation for sorting and searching demonstrations."""
from __future__ import annotations

from models.student import Student

DEFAULT_MOCK_COUNT = 12
MAX_MOCK_COUNT = 1_000_000

# Predefined varied scores across 35 items representing realistic grade distribution:
# A (>=80), B+ (75-79.9), B (70-74.9), C+ (65-69.9), C (60-64.9), D+ (55-59.9), D (50-54.9), F (<50)
_BASE_SCORES = [
    78.5, 52.0, 91.5, 64.0, 83.0, 47.5, 73.0, 68.5, 58.0, 88.0,
    42.0, 95.5, 61.0, 76.0, 54.5, 81.5, 69.0, 71.5, 59.0, 86.5,
    49.0, 93.0, 63.5, 77.0, 56.5, 84.0, 66.5, 72.0, 51.5, 89.5,
    45.0, 96.0, 60.5, 79.0, 85.0,
]


def generate_mock_students(count: int = DEFAULT_MOCK_COUNT) -> list[Student]:
    """Generate a deterministic list of synthetic student records for demonstration.

    All generated records use clearly synthetic identifiers (e.g. TEST0001) and
    synthetic names (e.g. นักเรียนทดสอบ 001). No real personal student data is used.

    Args:
        count: Number of synthetic student records to generate (must be >= 1).

    Returns:
        List of Student instances.

    Raises:
        ValueError: If count < 1.
    """
    if count < 1 or count > MAX_MOCK_COUNT:
        raise ValueError(f"Count must be between 1 and {MAX_MOCK_COUNT:,}.")

    students: list[Student] = []
    base_len = len(_BASE_SCORES)

    for i in range(1, count + 1):
        student_id = f"TEST{i:04d}"
        name = f"นักเรียนทดสอบ {i:03d}"
        if i <= base_len:
            score = _BASE_SCORES[i - 1]
        else:
            # Deterministic variation for counts beyond default 35
            base = _BASE_SCORES[(i - 1) % base_len]
            offset = ((i * 7) % 11) - 5  # -5 to +5 variation
            score = max(30.0, min(99.0, round(base + (offset * 0.5), 1)))

        students.append(Student(student_id=student_id, name=name, score=score))

    return students
