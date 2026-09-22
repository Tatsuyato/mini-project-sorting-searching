"""Unit tests for synthetic mock data generation, CLI arguments, and regression."""
import io
import re
import unittest
from unittest.mock import patch

from main import main, parse_args
from services.mock_data import DEFAULT_MOCK_COUNT, generate_mock_students
from services.score_manager import ScoreManager


class TestMockDataGenerator(unittest.TestCase):
    """Test synthetic mock student data generation."""

    def test_default_count(self) -> None:
        students = generate_mock_students()
        self.assertEqual(len(students), DEFAULT_MOCK_COUNT)
        self.assertEqual(len(students), 12)

    def test_custom_count(self) -> None:
        self.assertEqual(len(generate_mock_students(10)), 10)
        self.assertEqual(len(generate_mock_students(50)), 50)

    def test_invalid_count_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            generate_mock_students(0)
        with self.assertRaises(ValueError):
            generate_mock_students(-10)
        with self.assertRaises(ValueError):
            generate_mock_students(1_000_001)

    def test_max_count_is_supported_by_validation(self) -> None:
        from services.mock_data import MAX_MOCK_COUNT
        self.assertEqual(MAX_MOCK_COUNT, 1_000_000)

    def test_synthetic_id_format(self) -> None:
        students = generate_mock_students(35)
        pattern = re.compile(r"^TEST\d{4}$")
        for s in students:
            self.assertRegex(
                s.student_id,
                pattern,
                f"Student ID '{s.student_id}' must follow TEST0000 format",
            )

    def test_synthetic_name_format(self) -> None:
        students = generate_mock_students(35)
        pattern = re.compile(r"^นักเรียนทดสอบ \d{3,}$")
        for s in students:
            self.assertRegex(
                s.name,
                pattern,
                f"Student name '{s.name}' must follow dummy pattern",
            )

    def test_no_duplicate_ids(self) -> None:
        students = generate_mock_students(50)
        ids = [s.student_id for s in students]
        self.assertEqual(len(ids), len(set(ids)), "Mock IDs must be strictly unique")

    def test_score_range_and_grade_diversity(self) -> None:
        students = generate_mock_students(35)
        grades_found = set()
        for s in students:
            self.assertGreaterEqual(s.score, 0.0)
            self.assertLessEqual(s.score, 100.0)
            grades_found.add(s.grade)

        # Diverse grade distribution across all standard bands
        expected_grades = {"A", "B+", "B", "C+", "C", "D+", "D", "F"}
        self.assertTrue(
            expected_grades.issubset(grades_found),
            f"Expected all grade bands to be represented, got: {grades_found}",
        )

    def test_mock_data_not_pre_sorted(self) -> None:
        students = generate_mock_students(35)
        scores = [s.score for s in students]
        self.assertNotEqual(scores, sorted(scores), "Scores should not be pre-sorted ascending")
        self.assertNotEqual(
            scores,
            sorted(scores, reverse=True),
            "Scores should not be pre-sorted descending",
        )


class TestScoreManagerMockIntegration(unittest.TestCase):
    """Test ScoreManager integration with mock data."""

    def setUp(self) -> None:
        self.manager = ScoreManager()

    def test_load_mock_data(self) -> None:
        count = self.manager.load_mock_data()
        self.assertEqual(count, DEFAULT_MOCK_COUNT)
        self.assertEqual(self.manager.count, DEFAULT_MOCK_COUNT)
        students = self.manager.get_all_students()
        self.assertTrue(all(s.student_id.startswith("TEST") for s in students))

    def test_sorting_on_mock_data(self) -> None:
        self.manager.load_mock_data()
        sorted_list, metrics = self.manager.sort_students(
            "merge", key_field="score", reverse=True, update_state=True
        )
        scores = [s.score for s in sorted_list]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertGreater(metrics.comparisons, 0)
        self.assertGreater(metrics.swaps, 0)

    def test_searching_on_mock_data(self) -> None:
        self.manager.load_mock_data()
        # Sequential search
        matched_seq, metrics_seq = self.manager.search_students(
            "sequential", "TEST0010", key_field="student_id"
        )
        self.assertEqual(len(matched_seq), 1)
        self.assertEqual(matched_seq[0].student_id, "TEST0010")
        self.assertTrue(metrics_seq.found)

        # Binary search (sort by student_id first)
        self.manager.sort_students(
            "merge", key_field="student_id", reverse=False, update_state=True
        )
        matched_bin, metrics_bin = self.manager.search_students(
            "binary", "TEST0010", key_field="student_id"
        )
        self.assertEqual(len(matched_bin), 1)
        self.assertEqual(matched_bin[0].student_id, "TEST0010")
        self.assertTrue(metrics_bin.found)

    def test_benchmark_sorting_on_mock_data(self) -> None:
        self.manager.load_mock_data()
        results = self.manager.benchmark_sorting(key_field="score", reverse=True)
        self.assertIn("Bubble Sort", results)
        self.assertIn("Insertion Sort", results)
        self.assertIn("Selection Sort", results)
        self.assertIn("Merge Sort", results)

        for name, metrics in results.items():
            self.assertGreater(metrics.comparisons, 0, f"{name} comparisons should be > 0")
            self.assertGreater(metrics.execution_time_ms, 0.0)


class TestNormalModeRegression(unittest.TestCase):
    """Verify normal mode (sample data) behavior is completely preserved."""

    def setUp(self) -> None:
        self.manager = ScoreManager()

    def test_load_sample_data_unaffected(self) -> None:
        count = self.manager.load_sample_data()
        self.assertEqual(count, 12)
        self.assertEqual(self.manager.count, 12)

        first = self.manager.get_all_students()[0]
        self.assertEqual(first.student_id, "6601001")
        self.assertEqual(first.name, "Somchai Jaidee")
        self.assertEqual(first.score, 85.5)
        self.assertEqual(first.grade, "A")


class TestCLIArguments(unittest.TestCase):
    """Test command line argument parsing."""

    def test_parse_args_default(self) -> None:
        args = parse_args([])
        self.assertFalse(args.mock_data)
        self.assertEqual(args.mock_count, 12)

    def test_parse_args_mock_data_flag(self) -> None:
        args = parse_args(["--mock-data"])
        self.assertTrue(args.mock_data)
        self.assertEqual(args.mock_count, 12)

    def test_parse_args_data_test_single_dash_flag(self) -> None:
        args = parse_args(["-data-test"])
        self.assertTrue(args.mock_data)
        self.assertEqual(args.mock_count, 12)

    def test_parse_args_data_test_double_dash_flag(self) -> None:
        args = parse_args(["--data-test"])
        self.assertTrue(args.mock_data)
        self.assertEqual(args.mock_count, 12)

    def test_parse_args_mock_alias_flag(self) -> None:
        args = parse_args(["--mock"])
        self.assertTrue(args.mock_data)
        self.assertEqual(args.mock_count, 12)

    def test_parse_args_custom_mock_count(self) -> None:
        args = parse_args(["--mock-data", "--mock-count", "25"])
        self.assertTrue(args.mock_data)
        self.assertEqual(args.mock_count, 25)

    def test_parse_args_data_test_custom_count(self) -> None:
        args = parse_args(["-data-test", "--mock-count", "20"])
        self.assertTrue(args.mock_data)
        self.assertEqual(args.mock_count, 20)

    @patch("builtins.input", return_value="0")
    def test_main_default_exit(self, mock_input) -> None:
        out = io.StringIO()
        with patch("sys.stdout", out):
            with self.assertRaises(SystemExit) as cm:
                main([])
            self.assertEqual(cm.exception.code, 0)
        output_str = out.getvalue()
        self.assertIn("โหลดชุดข้อมูลตัวอย่างเรียบร้อยแล้ว (12 รายการ)", output_str)

    @patch("builtins.input", return_value="0")
    def test_main_mock_data_flag_exit(self, mock_input) -> None:
        out = io.StringIO()
        with patch("sys.stdout", out):
            with self.assertRaises(SystemExit) as cm:
                main(["--mock-data"])
            self.assertEqual(cm.exception.code, 0)
        output_str = out.getvalue()
        self.assertIn("เริ่มต้นระบบในโหมดข้อมูลจำลอง (Mock Data)", output_str)
        self.assertIn("12 รายการ", output_str)

    @patch("builtins.input", return_value="0")
    def test_main_data_test_single_dash_exit(self, mock_input) -> None:
        out = io.StringIO()
        with patch("sys.stdout", out):
            with self.assertRaises(SystemExit) as cm:
                main(["-data-test"])
            self.assertEqual(cm.exception.code, 0)
        output_str = out.getvalue()
        self.assertIn("เริ่มต้นระบบในโหมดข้อมูลจำลอง (Mock Data)", output_str)
        self.assertIn("12 รายการ", output_str)

    @patch("builtins.input", return_value="0")
    def test_main_data_test_double_dash_exit(self, mock_input) -> None:
        out = io.StringIO()
        with patch("sys.stdout", out):
            with self.assertRaises(SystemExit) as cm:
                main(["--data-test"])
            self.assertEqual(cm.exception.code, 0)
        output_str = out.getvalue()
        self.assertIn("เริ่มต้นระบบในโหมดข้อมูลจำลอง (Mock Data)", output_str)
        self.assertIn("12 รายการ", output_str)

    @patch("builtins.input", return_value="0")
    def test_main_mock_alias_exit(self, mock_input) -> None:
        out = io.StringIO()
        with patch("sys.stdout", out):
            with self.assertRaises(SystemExit) as cm:
                main(["--mock"])
            self.assertEqual(cm.exception.code, 0)
        output_str = out.getvalue()
        self.assertIn("เริ่มต้นระบบในโหมดข้อมูลจำลอง (Mock Data)", output_str)
        self.assertIn("12 รายการ", output_str)

