"""Regression tests for UI entry paths, interactive searching CLI, and input validations."""
import io
import sys
import unittest
from unittest.mock import patch

import main
from services.score_manager import ScoreManager


class TestSearchingCLIEntryPath(unittest.TestCase):
    """Test handle_searching UI entry path and error handling."""

    def setUp(self) -> None:
        self.manager = ScoreManager()
        self.manager.load_sample_data()

    def test_handle_searching_sequential_score_non_numeric_does_not_crash(self) -> None:
        """Regression test: Sequential search with non-numeric score query (e.g. 'Som')

        must handle ValueError gracefully without crashing and display a warning.
        """
        # Simulated inputs: 1 (Sequential), 2 (score), 'Som', 'y' (trace)
        simulated_inputs = ["1", "2", "Som", "y"]
        captured_output = io.StringIO()

        with patch("builtins.input", side_effect=simulated_inputs):
            with patch("sys.stdout", captured_output):
                main.handle_searching(self.manager)

        output_str = captured_output.getvalue()
        self.assertIn("เกิดข้อผิดพลาดในการค้นหา", output_str)
        self.assertIn("Score search query must be a valid number", output_str)

    def test_handle_searching_binary_score_non_numeric_does_not_crash(self) -> None:
        """Regression test: Binary search with non-numeric score query ('Som')

        must handle error gracefully without crashing.
        """
        # Simulated inputs: 2 (Binary), 2 (score), 'Som', 'y' (trace)
        simulated_inputs = ["2", "2", "Som", "y"]
        captured_output = io.StringIO()

        with patch("builtins.input", side_effect=simulated_inputs):
            with patch("sys.stdout", captured_output):
                main.handle_searching(self.manager)

        output_str = captured_output.getvalue()
        self.assertIn("เกิดข้อผิดพลาด", output_str)

    def test_handle_searching_empty_query_polite_message(self) -> None:
        """Regression test: empty search query must display polite Thai warning and return."""
        simulated_inputs = ["1", "1", ""]
        captured_output = io.StringIO()

        with patch("builtins.input", side_effect=simulated_inputs):
            with patch("sys.stdout", captured_output):
                main.handle_searching(self.manager)

        output_str = captured_output.getvalue()
        self.assertIn("คำค้นหาต้องไม่เป็นค่าว่าง", output_str)

    def test_handle_searching_invalid_algo_choice(self) -> None:
        """Regression test: invalid search algorithm choice displays polite warning and returns."""
        simulated_inputs = ["9"]
        captured_output = io.StringIO()

        with patch("builtins.input", side_effect=simulated_inputs):
            with patch("sys.stdout", captured_output):
                main.handle_searching(self.manager)

        output_str = captured_output.getvalue()
        self.assertIn("ตัวเลือกอัลกอริทึมการค้นหาไม่ถูกต้อง", output_str)

    def test_handle_searching_invalid_field_choice(self) -> None:
        """Regression test: invalid field choice displays polite warning and returns."""
        simulated_inputs = ["1", "9"]
        captured_output = io.StringIO()

        with patch("builtins.input", side_effect=simulated_inputs):
            with patch("sys.stdout", captured_output):
                main.handle_searching(self.manager)

        output_str = captured_output.getvalue()
        self.assertIn("ฟิลด์ที่เลือกไม่ถูกต้อง", output_str)

    def test_handle_searching_binary_with_name_field_validation(self) -> None:
        """Regression test: Binary search with name field displays polite warning and returns."""
        simulated_inputs = ["2", "3"]
        captured_output = io.StringIO()

        with patch("builtins.input", side_effect=simulated_inputs):
            with patch("sys.stdout", captured_output):
                main.handle_searching(self.manager)

        output_str = captured_output.getvalue()
        self.assertIn("การค้นหาด้วย Binary Search ในเมนูนี้รองรับรหัสนักเรียนและคะแนน", output_str)

    def test_handle_searching_not_found(self) -> None:
        """Regression test: searching for non-existent record displays not-found status without crash."""
        simulated_inputs = ["1", "2", "999.0", "n"]
        captured_output = io.StringIO()

        with patch("builtins.input", side_effect=simulated_inputs):
            with patch("sys.stdout", captured_output):
                main.handle_searching(self.manager)

        output_str = captured_output.getvalue()
        self.assertIn("ไม่พบข้อมูล", output_str)


class TestMainApplicationFlow(unittest.TestCase):
    """Test end-to-end interactive flow of main()."""

    def test_main_repro_sequential_score_som_then_exit_0(self) -> None:
        """Repro test matching user scenario:

        Menu 6 -> Sequential (1) -> score (2) -> Som -> trace y -> returns to menu -> Exit 0.
        Must exit with code 0.
        """
        inputs = ["6", "1", "2", "Som", "y", "0"]
        captured_output = io.StringIO()

        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", captured_output):
                with self.assertRaises(SystemExit) as exit_ctx:
                    main.main([])

        self.assertEqual(exit_ctx.exception.code, 0)
        output_str = captured_output.getvalue()
        self.assertIn("เกิดข้อผิดพลาดในการค้นหา", output_str)
        self.assertIn("ขอบคุณที่ใช้งานโปรแกรม", output_str)

    def test_main_repro_sequential_score_som_without_trace_key_then_exit_0(self) -> None:
        """Repro test where user inputs 0 directly after 'Som'."""
        inputs = ["6", "1", "2", "Som", "0"]
        captured_output = io.StringIO()

        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", captured_output):
                with self.assertRaises(SystemExit) as exit_ctx:
                    main.main([])

        self.assertEqual(exit_ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
