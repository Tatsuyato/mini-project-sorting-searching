"""Unit tests for sorting algorithms."""
import unittest
from algorithms.sorting import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    merge_sort,
)
from models.student import Student


class TestSortingAlgorithms(unittest.TestCase):
    """Test suite covering Bubble, Insertion, Selection, and Merge Sort."""

    def setUp(self) -> None:
        self.algorithms = [
            ("Bubble Sort", bubble_sort),
            ("Insertion Sort", insertion_sort),
            ("Selection Sort", selection_sort),
            ("Merge Sort", merge_sort),
        ]
        self.sample_numbers = [64, 34, 25, 12, 22, 11, 90]
        self.sorted_numbers = sorted(self.sample_numbers)
        self.reverse_sorted_numbers = sorted(self.sample_numbers, reverse=True)

    def test_empty_list(self) -> None:
        for name, algo in self.algorithms:
            with self.subTest(algorithm=name):
                result, metrics = algo([])
                self.assertEqual(result, [])
                self.assertEqual(metrics.comparisons, 0)

    def test_single_element(self) -> None:
        for name, algo in self.algorithms:
            with self.subTest(algorithm=name):
                result, metrics = algo([42])
                self.assertEqual(result, [42])

    def test_already_sorted(self) -> None:
        for name, algo in self.algorithms:
            with self.subTest(algorithm=name):
                result, metrics = algo(self.sorted_numbers)
                self.assertEqual(result, self.sorted_numbers)

    def test_reverse_sorted_input(self) -> None:
        for name, algo in self.algorithms:
            with self.subTest(algorithm=name):
                result, metrics = algo(self.reverse_sorted_numbers)
                self.assertEqual(result, self.sorted_numbers)

    def test_ascending_sort(self) -> None:
        for name, algo in self.algorithms:
            with self.subTest(algorithm=name):
                result, metrics = algo(self.sample_numbers)
                self.assertEqual(result, self.sorted_numbers)
                self.assertGreater(metrics.comparisons, 0)
                self.assertGreaterEqual(metrics.execution_time_ms, 0.0)

    def test_descending_sort(self) -> None:
        for name, algo in self.algorithms:
            with self.subTest(algorithm=name):
                result, metrics = algo(self.sample_numbers, reverse=True)
                self.assertEqual(result, self.reverse_sorted_numbers)

    def test_duplicates(self) -> None:
        data = [5, 1, 3, 5, 2, 5, 1]
        expected = sorted(data)
        for name, algo in self.algorithms:
            with self.subTest(algorithm=name):
                result, _ = algo(data)
                self.assertEqual(result, expected)

    def test_student_sorting_by_score(self) -> None:
        students = [
            Student("001", "Alice", 75.0),
            Student("002", "Bob", 92.5),
            Student("003", "Charlie", 60.0),
            Student("004", "David", 88.0),
        ]
        expected_ascending = ["Charlie", "Alice", "David", "Bob"]
        expected_descending = ["Bob", "David", "Alice", "Charlie"]

        for name, algo in self.algorithms:
            with self.subTest(algorithm=name, order="ascending"):
                result, _ = algo(students, key=lambda s: s.score)
                names = [s.name for s in result]
                self.assertEqual(names, expected_ascending)

            with self.subTest(algorithm=name, order="descending"):
                result, _ = algo(students, key=lambda s: s.score, reverse=True)
                names = [s.name for s in result]
                self.assertEqual(names, expected_descending)

    def test_student_sorting_by_id(self) -> None:
        students = [
            Student("C-100", "Charlie", 60.0),
            Student("A-100", "Alice", 75.0),
            Student("B-100", "Bob", 92.5),
        ]
        expected = ["A-100", "B-100", "C-100"]

        for name, algo in self.algorithms:
            with self.subTest(algorithm=name):
                result, _ = algo(students, key=lambda s: s.student_id)
                ids = [s.student_id for s in result]
                self.assertEqual(ids, expected)


if __name__ == "__main__":
    unittest.main()
