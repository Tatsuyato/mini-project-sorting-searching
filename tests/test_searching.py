"""Unit tests for searching algorithms."""
import unittest
from algorithms.searching import (
    sequential_search,
    binary_search,
    is_sorted,
)
from models.student import Student


class TestSearchingAlgorithms(unittest.TestCase):
    """Test suite covering Sequential Search and Binary Search."""

    def setUp(self) -> None:
        self.sorted_numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        self.reverse_sorted_numbers = [90, 80, 70, 60, 50, 40, 30, 20, 10]
        self.unsorted_numbers = [50, 20, 80, 10, 90, 30]

    def test_is_sorted_helper(self) -> None:
        self.assertTrue(is_sorted([]))
        self.assertTrue(is_sorted([42]))
        self.assertTrue(is_sorted(self.sorted_numbers))
        self.assertFalse(is_sorted(self.unsorted_numbers))
        self.assertTrue(is_sorted(self.reverse_sorted_numbers, reverse=True))

    def test_sequential_search_basic(self) -> None:
        # Found single
        indices, metrics = sequential_search(self.sorted_numbers, 40)
        self.assertEqual(indices, [3])
        self.assertTrue(metrics.found)
        self.assertEqual(metrics.comparisons, 9)

        # Not found
        indices, metrics = sequential_search(self.sorted_numbers, 999)
        self.assertEqual(indices, [])
        self.assertFalse(metrics.found)
        self.assertEqual(metrics.comparisons, 9)

        # Multiple matches
        data = [10, 20, 30, 20, 40, 20]
        indices, _ = sequential_search(data, 20)
        self.assertEqual(indices, [1, 3, 5])

    def test_sequential_search_empty_and_single(self) -> None:
        indices, metrics = sequential_search([], 10)
        self.assertEqual(indices, [])
        self.assertFalse(metrics.found)

        indices, metrics = sequential_search([5], 5)
        self.assertEqual(indices, [0])
        self.assertTrue(metrics.found)

    def test_sequential_search_students(self) -> None:
        students = [
            Student("S1", "Alice", 85.0),
            Student("S2", "Bob", 70.0),
            Student("S3", "Charlie", 85.0),
        ]
        # Search by score (multiple matches)
        indices, _ = sequential_search(students, 85.0, key=lambda s: s.score)
        self.assertEqual(indices, [0, 2])

        # Search by ID
        indices, _ = sequential_search(students, "S2", key=lambda s: s.student_id)
        self.assertEqual(indices, [1])

    def test_binary_search_found(self) -> None:
        # Target at start
        idx, metrics = binary_search(self.sorted_numbers, 10)
        self.assertEqual(idx, 0)
        self.assertTrue(metrics.found)

        # Target at middle
        idx, metrics = binary_search(self.sorted_numbers, 50)
        self.assertEqual(idx, 4)
        self.assertTrue(metrics.found)

        # Target at end
        idx, metrics = binary_search(self.sorted_numbers, 90)
        self.assertEqual(idx, 8)
        self.assertTrue(metrics.found)

    def test_binary_search_not_found(self) -> None:
        # Smaller than min
        idx, metrics = binary_search(self.sorted_numbers, 5)
        self.assertIsNone(idx)
        self.assertFalse(metrics.found)

        # In-between
        idx, metrics = binary_search(self.sorted_numbers, 25)
        self.assertIsNone(idx)
        self.assertFalse(metrics.found)

        # Larger than max
        idx, metrics = binary_search(self.sorted_numbers, 100)
        self.assertIsNone(idx)
        self.assertFalse(metrics.found)

    def test_binary_search_reverse_sorted(self) -> None:
        idx, metrics = binary_search(self.reverse_sorted_numbers, 70, reverse=True)
        self.assertEqual(idx, 2)
        self.assertTrue(metrics.found)

    def test_binary_search_unsorted_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            binary_search(self.unsorted_numbers, 20, validate_sorted=True)

    def test_binary_search_students(self) -> None:
        students = [
            Student("6601001", "Alice", 50.0),
            Student("6601002", "Bob", 70.0),
            Student("6601003", "Charlie", 85.0),
            Student("6601004", "David", 95.0),
        ]
        # Search by score
        idx, metrics = binary_search(students, 85.0, key=lambda s: s.score)
        self.assertEqual(idx, 2)
        self.assertEqual(students[idx].name, "Charlie")

        # Search by ID
        idx, _ = binary_search(students, "6601004", key=lambda s: s.student_id)
        self.assertEqual(idx, 3)
        self.assertEqual(students[idx].name, "David")


if __name__ == "__main__":
    unittest.main()
