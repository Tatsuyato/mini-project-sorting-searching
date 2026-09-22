"""Unit tests for Student model and ScoreManager service."""
import unittest
from models.student import Student
from services.score_manager import ScoreManager


class TestStudentModel(unittest.TestCase):
    """Test Student dataclass and grade calculations."""

    def test_grade_boundaries(self) -> None:
        test_cases = [
            (80.0, "A"),
            (100.0, "A"),
            (79.9, "B+"),
            (75.0, "B+"),
            (74.9, "B"),
            (70.0, "B"),
            (69.9, "C+"),
            (65.0, "C+"),
            (64.9, "C"),
            (60.0, "C"),
            (59.9, "D+"),
            (55.0, "D+"),
            (54.9, "D"),
            (50.0, "D"),
            (49.9, "F"),
            (0.0, "F"),
        ]
        for score, expected_grade in test_cases:
            with self.subTest(score=score, expected=expected_grade):
                s = Student("101", "Test", score)
                self.assertEqual(s.grade, expected_grade)

    def test_invalid_score_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Student("101", "Test", -1.0)
        with self.assertRaises(ValueError):
            Student("101", "Test", 100.5)
        with self.assertRaises(ValueError):
            Student("101", "Test", "not-a-number")  # type: ignore

    def test_invalid_id_or_name(self) -> None:
        with self.assertRaises(ValueError):
            Student("", "Test", 80)
        with self.assertRaises(ValueError):
            Student("101", "  ", 80)

    def test_dict_serialization(self) -> None:
        s = Student("6601", "Somchai", 85.0)
        d = s.to_dict()
        self.assertEqual(d["student_id"], "6601")
        self.assertEqual(d["grade"], "A")
        s2 = Student.from_dict(d)
        self.assertEqual(s, s2)


class TestScoreManagerService(unittest.TestCase):
    """Test ScoreManager CRUD, sorting, and searching functionality."""

    def setUp(self) -> None:
        self.manager = ScoreManager()

    def test_add_and_get_student(self) -> None:
        s = Student("6601", "Somchai", 85.0)
        self.manager.add_student(s)
        self.assertEqual(self.manager.count, 1)
        retrieved = self.manager.get_student("6601")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Somchai")

    def test_duplicate_student_id_raises_error(self) -> None:
        s1 = Student("6601", "Somchai", 85.0)
        s2 = Student("6601", "Another Person", 90.0)
        self.manager.add_student(s1)
        with self.assertRaises(ValueError):
            self.manager.add_student(s2)

    def test_remove_student(self) -> None:
        s = Student("6601", "Somchai", 85.0)
        self.manager.add_student(s)
        self.assertTrue(self.manager.remove_student("6601"))
        self.assertEqual(self.manager.count, 0)
        self.assertFalse(self.manager.remove_student("6601"))

    def test_load_sample_data_and_clear(self) -> None:
        count = self.manager.load_sample_data()
        self.assertGreater(count, 0)
        self.assertEqual(self.manager.count, count)
        self.manager.clear()
        self.assertEqual(self.manager.count, 0)

    def test_sort_without_updating_state(self) -> None:
        self.manager.load_sample_data()
        original_first_id = self.manager.get_all_students()[0].student_id
        sorted_list, metrics = self.manager.sort_students(
            "merge", key_field="score", reverse=False, update_state=False
        )
        # Original state is untouched
        self.assertEqual(self.manager.get_all_students()[0].student_id, original_first_id)
        # Result list is sorted
        scores = [s.score for s in sorted_list]
        self.assertEqual(scores, sorted(scores))

    def test_sort_with_updating_state(self) -> None:
        self.manager.load_sample_data()
        sorted_list, metrics = self.manager.sort_students(
            "bubble", key_field="score", reverse=True, update_state=True
        )
        current_scores = [s.score for s in self.manager.get_all_students()]
        self.assertEqual(current_scores, sorted(current_scores, reverse=True))

    def test_benchmark_all_sorting(self) -> None:
        self.manager.load_sample_data()
        results = self.manager.benchmark_sorting(key_field="score")
        self.assertEqual(len(results), 4)
        self.assertIn("Bubble Sort", results)
        self.assertIn("Insertion Sort", results)
        self.assertIn("Selection Sort", results)
        self.assertIn("Merge Sort", results)

    def test_search_integration(self) -> None:
        self.manager.load_sample_data()
        # Sequential search by ID
        matches, metrics = self.manager.search_students("sequential", "6601003", key_field="student_id")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].name, "Wannisa Ploydee")

        # Binary search on sorted list
        self.manager.sort_students("merge", key_field="student_id", update_state=True)
        matches, metrics = self.manager.search_students("binary", "6601003", key_field="student_id")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].name, "Wannisa Ploydee")

    def test_sort_students_trace(self) -> None:
        """Verify ScoreManager forwards trace flag to all sorting algorithms."""
        self.manager.load_sample_data()
        for algo in ["bubble", "insertion", "selection", "merge"]:
            with self.subTest(algorithm=algo):
                _, metrics = self.manager.sort_students(algo, key_field="score", trace=True)
                self.assertGreater(len(metrics.traces), 0)

    def test_search_students_trace(self) -> None:
        """Verify ScoreManager forwards trace flag to sequential and binary search."""
        self.manager.load_sample_data()
        # Sequential search trace
        _, seq_metrics = self.manager.search_students(
            "sequential", "6601003", key_field="student_id", trace=True
        )
        self.assertGreater(len(seq_metrics.traces), 0)

        # Binary search trace
        self.manager.sort_students("merge", key_field="student_id", update_state=True)
        _, bin_metrics = self.manager.search_students(
            "binary", "6601003", key_field="student_id", trace=True
        )
        self.assertGreater(len(bin_metrics.traces), 0)

    def test_benchmark_sorting_not_affected_by_trace(self) -> None:
        """Verify benchmark maintains clean metrics and empty trace lists."""
        self.manager.load_sample_data()
        results = self.manager.benchmark_sorting(key_field="score")
        for name, metrics in results.items():
            self.assertEqual(metrics.traces, [], f"Benchmark for {name} should not retain traces")
            self.assertGreater(metrics.comparisons, 0)
            self.assertGreaterEqual(metrics.swaps, 0)

    def test_search_score_invalid_query_raises_value_error(self) -> None:
        """Regression test: non-numeric query for score search must raise ValueError consistently."""
        self.manager.load_sample_data()
        invalid_queries = ["Som", "abc", "", "   ", None, [], {"score": 80}]
        for query in invalid_queries:
            for algo in ["sequential", "binary"]:
                with self.subTest(algorithm=algo, query=query):
                    with self.assertRaises(ValueError) as ctx:
                        self.manager.search_students(algo, query, key_field="score")
                    self.assertIn("Score search query must be a valid number", str(ctx.exception))

    def test_search_score_valid_query_formats(self) -> None:
        """Verify that score search accepts valid string numbers, floats, and integers."""
        self.manager.load_sample_data()
        # Sequential
        matches, metrics = self.manager.search_students("sequential", "85.5", key_field="score")
        self.assertTrue(metrics.found)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].name, "Somchai Jaidee")

        matches_float, _ = self.manager.search_students("sequential", 85.5, key_field="score")
        self.assertEqual(len(matches_float), 1)

        # Binary (ensure sorted first)
        self.manager.sort_students("merge", key_field="score", reverse=False, update_state=True)
        matches_bin, bin_metrics = self.manager.search_students("binary", "85.5", key_field="score")
        self.assertTrue(bin_metrics.found)
        self.assertEqual(len(matches_bin), 1)
        self.assertEqual(matches_bin[0].name, "Somchai Jaidee")

    def test_search_not_found_returns_empty(self) -> None:
        """Verify searching for non-existent score or ID safely returns empty list."""
        self.manager.load_sample_data()
        # Score not found
        matches, metrics = self.manager.search_students("sequential", 999.0, key_field="score")
        self.assertEqual(matches, [])
        self.assertFalse(metrics.found)

        # ID not found in binary
        self.manager.sort_students("merge", key_field="student_id", reverse=False, update_state=True)
        matches_bin, bin_metrics = self.manager.search_students("binary", "9999999", key_field="student_id")
        self.assertEqual(matches_bin, [])
        self.assertFalse(bin_metrics.found)

    def test_search_invalid_algorithm_or_field_raises_value_error(self) -> None:
        """Verify invalid algorithm names or key fields raise ValueError consistently."""
        self.manager.load_sample_data()
        with self.assertRaises(ValueError):
            self.manager.search_students("quick", "6601001", key_field="student_id")
        with self.assertRaises(ValueError):
            self.manager.search_students(None, "6601001", key_field="student_id")  # type: ignore
        with self.assertRaises(ValueError):
            self.manager.search_students("sequential", "6601001", key_field="invalid_field")
        with self.assertRaises(ValueError):
            self.manager.sort_students("unknown_algo", key_field="score")

    def test_remove_and_get_student_safe_inputs(self) -> None:
        """Verify remove_student and get_student safely handle empty or non-string inputs."""
        self.manager.load_sample_data()
        # get_student
        self.assertIsNone(self.manager.get_student(""))
        self.assertIsNone(self.manager.get_student("   "))
        self.assertIsNone(self.manager.get_student(None))  # type: ignore
        self.assertIsNone(self.manager.get_student(12345))  # type: ignore

        # remove_student
        self.assertFalse(self.manager.remove_student(""))
        self.assertFalse(self.manager.remove_student("   "))
        self.assertFalse(self.manager.remove_student(None))  # type: ignore
        self.assertFalse(self.manager.remove_student(999))  # type: ignore


if __name__ == "__main__":
    unittest.main()
