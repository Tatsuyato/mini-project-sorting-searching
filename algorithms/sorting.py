"""Sorting algorithms implementation with educational metrics tracking.

Includes:
- Bubble Sort (with early exit optimization)
- Insertion Sort
- Selection Sort
- Merge Sort (Divide and Conquer)
"""
from dataclasses import dataclass, field
import time
from typing import Any, Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")


@dataclass
class SortMetrics:
    algorithm_name: str
    comparisons: int
    swaps: int
    execution_time_ms: float
    traces: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"[{self.algorithm_name}] Comparisons: {self.comparisons}, "
            f"Swaps/Operations: {self.swaps}, Time: {self.execution_time_ms:.4f} ms"
        )


def _get_key_func(key: Optional[Callable[[T], Any]]) -> Callable[[T], Any]:
    return key if key is not None else (lambda x: x)


def _format_sequence(items: Sequence[T], key: Callable[[T], Any], max_items: int = 8) -> str:
    """Format a sequence into a compact readable string representation."""
    def _repr_val(x: T) -> str:
        v = key(x)
        if isinstance(v, float):
            return f"{v:.1f}"
        return str(v)

    if len(items) <= max_items:
        return "[" + ", ".join(_repr_val(x) for x in items) + "]"

    half = max_items // 2
    left_str = ", ".join(_repr_val(x) for x in items[:half])
    right_str = ", ".join(_repr_val(x) for x in items[-half:])
    return f"[{left_str}, ..., {right_str}] ({len(items)} รายการ)"


def bubble_sort(
    items: Sequence[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    trace: bool = False,
) -> tuple[List[T], SortMetrics]:
    """Sort items using Bubble Sort algorithm with early exit optimization.

    Time Complexity:
      - Best: O(n) when already sorted
      - Average/Worst: O(n^2)
    Space Complexity: O(n) for copy, O(1) auxiliary
    """
    start_time = time.perf_counter()
    arr = list(items)
    n = len(arr)
    comparisons = 0
    swaps = 0
    traces: List[str] = []
    k = _get_key_func(key)

    if trace:
        traces.append(f"เริ่มต้น: {_format_sequence(arr, k)}")

    for i in range(n):
        swapped = False
        pass_swaps = 0
        for j in range(0, n - i - 1):
            comparisons += 1
            val_a = k(arr[j])
            val_b = k(arr[j + 1])
            condition = (val_a < val_b) if reverse else (val_a > val_b)
            if condition:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                pass_swaps += 1
                swapped = True

        if trace:
            pass_num = i + 1
            if swapped:
                traces.append(
                    f"Pass {pass_num:02d}: สลับ {pass_swaps} ครั้ง -> {_format_sequence(arr, k)}"
                )
            else:
                traces.append(
                    f"Pass {pass_num:02d}: ไม่มีการสลับค่า (Early Exit: จัดเรียงเรียบร้อยแล้ว)"
                )

        if not swapped:
            break

    if n <= 1 and trace and not traces:
        traces.append(f"Pass 01: มีข้อมูล {n} รายการ (เรียงลำดับอยู่แล้ว)")

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SortMetrics("Bubble Sort", comparisons, swaps, elapsed_ms, traces)
    return arr, metrics


def insertion_sort(
    items: Sequence[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    trace: bool = False,
) -> tuple[List[T], SortMetrics]:
    """Sort items using Insertion Sort algorithm.

    Time Complexity:
      - Best: O(n) when already sorted
      - Average/Worst: O(n^2)
    Space Complexity: O(n) for copy, O(1) auxiliary
    """
    start_time = time.perf_counter()
    arr = list(items)
    n = len(arr)
    comparisons = 0
    shifts = 0
    traces: List[str] = []
    k = _get_key_func(key)

    if trace:
        traces.append(f"เริ่มต้น: {_format_sequence(arr, k)}")

    for i in range(1, n):
        current_item = arr[i]
        current_key = k(current_item)
        j = i - 1
        shift_count = 0

        while j >= 0:
            comparisons += 1
            prev_key = k(arr[j])
            condition = (prev_key < current_key) if reverse else (prev_key > current_key)
            if condition:
                arr[j + 1] = arr[j]
                shifts += 1
                shift_count += 1
                j -= 1
            else:
                break

        arr[j + 1] = current_item

        if trace:
            val_repr = f"{current_key:.1f}" if isinstance(current_key, float) else str(current_key)
            if shift_count > 0:
                traces.append(
                    f"Step {i:02d}: แทรกค่า '{val_repr}' ไว้ที่ index {j + 1} (เลื่อน {shift_count} ตำแหน่ง) -> {_format_sequence(arr, k)}"
                )
            else:
                traces.append(
                    f"Step {i:02d}: ค่า '{val_repr}' อยู่ตำแหน่งที่ถูกต้องแล้ว (index {i}) -> {_format_sequence(arr, k)}"
                )

    if n <= 1 and trace and not traces:
        traces.append(f"Step 01: มีข้อมูล {n} รายการ (เรียงลำดับอยู่แล้ว)")

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SortMetrics("Insertion Sort", comparisons, shifts, elapsed_ms, traces)
    return arr, metrics


def selection_sort(
    items: Sequence[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    trace: bool = False,
) -> tuple[List[T], SortMetrics]:
    """Sort items using Selection Sort algorithm.

    Time Complexity:
      - Best/Average/Worst: O(n^2)
    Space Complexity: O(n) for copy, O(1) auxiliary
    """
    start_time = time.perf_counter()
    arr = list(items)
    n = len(arr)
    comparisons = 0
    swaps = 0
    traces: List[str] = []
    k = _get_key_func(key)

    if trace:
        traces.append(f"เริ่มต้น: {_format_sequence(arr, k)}")

    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            val_j = k(arr[j])
            val_target = k(arr[target_idx])
            condition = (val_j > val_target) if reverse else (val_j < val_target)
            if condition:
                target_idx = j

        if trace:
            target_val = k(arr[target_idx])
            val_repr = f"{target_val:.1f}" if isinstance(target_val, float) else str(target_val)
            target_desc = "มากที่สุด" if reverse else "น้อยที่สุด"

        if target_idx != i:
            if trace:
                curr_val = k(arr[i])
                curr_repr = f"{curr_val:.1f}" if isinstance(curr_val, float) else str(curr_val)
            arr[i], arr[target_idx] = arr[target_idx], arr[i]
            swaps += 1
            if trace:
                traces.append(
                    f"Step {i + 1:02d}: สลับค่า{target_desc} '{val_repr}' (index {target_idx}) กับ index {i} ('{curr_repr}') -> {_format_sequence(arr, k)}"
                )
        else:
            if trace and i < n - 1:
                traces.append(
                    f"Step {i + 1:02d}: ค่า{target_desc} '{val_repr}' อยู่ที่ index {i} อยู่แล้ว -> {_format_sequence(arr, k)}"
                )

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SortMetrics("Selection Sort", comparisons, swaps, elapsed_ms, traces)
    return arr, metrics


def merge_sort(
    items: Sequence[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    trace: bool = False,
) -> tuple[List[T], SortMetrics]:
    """Sort items using Merge Sort algorithm (Divide and Conquer).

    Time Complexity:
      - Best/Average/Worst: O(n log n)
    Space Complexity: O(n) auxiliary
    """
    start_time = time.perf_counter()
    comparisons = 0
    merges = 0
    traces: List[str] = []
    k = _get_key_func(key)
    merge_step = 0

    if trace:
        traces.append(f"เริ่มต้น: {_format_sequence(list(items), k)}")

    def _merge(left: List[T], right: List[T]) -> List[T]:
        nonlocal comparisons, merges, merge_step
        result: List[T] = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comparisons += 1
            val_l = k(left[i])
            val_r = k(right[j])
            # Stability: use <= for ascending, >= for descending
            condition = (val_l >= val_r) if reverse else (val_l <= val_r)
            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            merges += 1

        while i < len(left):
            result.append(left[i])
            i += 1
            merges += 1

        while j < len(right):
            result.append(right[j])
            j += 1
            merges += 1

        if trace:
            merge_step += 1
            traces.append(
                f"Merge #{merge_step:02d}: ผสาน {_format_sequence(left, k)} + {_format_sequence(right, k)} -> {_format_sequence(result, k)}"
            )

        return result

    def _sort(lst: List[T]) -> List[T]:
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left_half = _sort(lst[:mid])
        right_half = _sort(lst[mid:])
        return _merge(left_half, right_half)

    sorted_arr = _sort(list(items))
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SortMetrics("Merge Sort", comparisons, merges, elapsed_ms, traces)
    return sorted_arr, metrics
