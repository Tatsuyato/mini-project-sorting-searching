"""Service layer managing the student score collection and algorithm coordination."""
from typing import Any, Callable, Dict, List, Optional, Tuple
from models.student import Student
from algorithms.sorting import (
    SortMetrics,
    bubble_sort,
    insertion_sort,
    selection_sort,
    merge_sort,
)
from algorithms.searching import (
    SearchMetrics,
    sequential_search,
    binary_search,
    is_sorted,
)


class ScoreManager:
    """Manages student records and provides sorting & searching operations."""

    def __init__(self) -> None:
        self._students: List[Student] = []

    @property
    def count(self) -> int:
        return len(self._students)

    def get_all_students(self) -> List[Student]:
        """Return a shallow copy of the current student list."""
        return list(self._students)

    def add_student(self, student: Student) -> None:
        """Add a new student. Raises ValueError if student_id already exists."""
        if any(s.student_id == student.student_id for s in self._students):
            raise ValueError(f"Student ID '{student.student_id}' already exists.")
        self._students.append(student)

    def remove_student(self, student_id: str) -> bool:
        """Remove a student by ID. Returns True if removed, False otherwise."""
        target_id = student_id.strip()
        for idx, student in enumerate(self._students):
            if student.student_id == target_id:
                del self._students[idx]
                return True
        return False

    def get_student(self, student_id: str) -> Optional[Student]:
        """Retrieve a student by ID."""
        target_id = student_id.strip()
        for student in self._students:
            if student.student_id == target_id:
                return student
        return None

    def clear(self) -> None:
        """Clear all student records."""
        self._students.clear()

    def load_sample_data(self) -> int:
        """Populate the manager with realistic demo student records."""
        samples = [
            Student("6601001", "Somchai Jaidee", 85.5),
            Student("6601002", "Somsak Rakเรียน", 62.0),
            Student("6601003", "Wannisa Ploydee", 94.0),
            Student("6601004", "Anan Chaiyaphum", 48.0),
            Student("6601005", "Kanchana Suksan", 76.5),
            Student("6601006", "Nattapong Mekkala", 55.0),
            Student("6601007", "Pitchaya Wongthai", 71.0),
            Student("6601008", "Thanakorn Rattanapan", 67.5),
            Student("6601009", "Supaporn Maneewong", 81.0),
            Student("6601010", "Chanon Prasertsook", 53.0),
            Student("6601011", "Benjawan Kaewkla", 89.0),
            Student("6601012", "Teerapat Boonsri", 42.5),
        ]
        self._students = samples
        return len(self._students)

    @staticmethod
    def _get_key_extractor(key_field: str) -> Callable[[Student], Any]:
        valid_fields = {
            "score": lambda s: s.score,
            "student_id": lambda s: s.student_id,
            "name": lambda s: s.name.lower(),
        }
        if key_field not in valid_fields:
            raise ValueError(
                f"Invalid key field '{key_field}'. Must be one of: {list(valid_fields.keys())}"
            )
        return valid_fields[key_field]

    def sort_students(
        self,
        algorithm: str,
        key_field: str = "score",
        reverse: bool = False,
        update_state: bool = False,
        trace: bool = False,
    ) -> Tuple[List[Student], SortMetrics]:
        """Sort students using the specified algorithm.

        Args:
            algorithm: 'bubble', 'insertion', 'selection', or 'merge'
            key_field: 'score', 'student_id', or 'name'
            reverse: True for descending, False for ascending
            update_state: If True, updates internal list with the sorted list
            trace: If True, records step-by-step execution trace

        Returns:
            Tuple of (sorted_list, SortMetrics)
        """
        key_func = self._get_key_extractor(key_field)
        algo = algorithm.strip().lower()

        if algo == "bubble":
            sorted_list, metrics = bubble_sort(
                self._students, key=key_func, reverse=reverse, trace=trace
            )
        elif algo == "insertion":
            sorted_list, metrics = insertion_sort(
                self._students, key=key_func, reverse=reverse, trace=trace
            )
        elif algo == "selection":
            sorted_list, metrics = selection_sort(
                self._students, key=key_func, reverse=reverse, trace=trace
            )
        elif algo == "merge":
            sorted_list, metrics = merge_sort(
                self._students, key=key_func, reverse=reverse, trace=trace
            )
        else:
            raise ValueError(
                f"Unknown sorting algorithm '{algorithm}'. "
                "Supported: 'bubble', 'insertion', 'selection', 'merge'"
            )

        if update_state:
            self._students = sorted_list

        return sorted_list, metrics

    def search_students(
        self,
        algorithm: str,
        query: Any,
        key_field: str = "student_id",
        reverse: bool = False,
        trace: bool = False,
    ) -> Tuple[List[Student], SearchMetrics]:
        """Search students using Sequential Search or Binary Search.

        Args:
            algorithm: 'sequential' or 'binary'
            query: The target value (ID, name, or score)
            key_field: 'student_id', 'name', or 'score'
            reverse: Sort direction if using binary search on reverse sorted list
            trace: If True, records step-by-step examination trace

        Returns:
            Tuple of (matched_students, SearchMetrics)
        """
        algo = algorithm.strip().lower()
        key_func = self._get_key_extractor(key_field)

        # Type conversion for query if searching by score
        target_val = query
        if key_field == "score":
            try:
                target_val = float(query)
            except ValueError:
                raise ValueError(f"Score search query must be a valid number, got '{query}'.")

        if algo == "sequential":
            indices, metrics = sequential_search(
                self._students, target_val, key=key_func, trace=trace
            )
            matched = [self._students[i] for i in indices]
            return matched, metrics

        elif algo == "binary":
            # For binary search, verify or run on sorted array
            idx, metrics = binary_search(
                self._students,
                target_val,
                key=key_func,
                reverse=reverse,
                validate_sorted=True,
                trace=trace,
            )
            matched = [self._students[idx]] if idx is not None else []
            return matched, metrics
        else:
            raise ValueError(
                f"Unknown searching algorithm '{algorithm}'. "
                "Supported: 'sequential', 'binary'"
            )

    def is_current_list_sorted(self, key_field: str = "score", reverse: bool = False) -> bool:
        """Check if internal student list is currently sorted."""
        key_func = self._get_key_extractor(key_field)
        return is_sorted(self._students, key=key_func, reverse=reverse)

    def benchmark_sorting(
        self, key_field: str = "score", reverse: bool = False
    ) -> Dict[str, SortMetrics]:
        """Run all 4 sorting algorithms on identical copies and return metrics comparison."""
        results: Dict[str, SortMetrics] = {}
        for algo in ["bubble", "insertion", "selection", "merge"]:
            _, metrics = self.sort_students(
                algorithm=algo,
                key_field=key_field,
                reverse=reverse,
                update_state=False,
            )
            results[metrics.algorithm_name] = metrics
        return results
