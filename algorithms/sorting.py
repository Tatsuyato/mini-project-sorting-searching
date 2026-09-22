"""Sorting algorithms implementation with educational metrics tracking.

Includes:
- Bubble Sort (with early exit optimization)
- Insertion Sort
- Selection Sort
- Merge Sort (Divide and Conquer)
"""
from dataclasses import dataclass
import time
from typing import Any, Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")


@dataclass
class SortMetrics:
    algorithm_name: str
    comparisons: int
    swaps: int
    execution_time_ms: float

    def __str__(self) -> str:
        return (
            f"[{self.algorithm_name}] Comparisons: {self.comparisons}, "
            f"Swaps/Operations: {self.swaps}, Time: {self.execution_time_ms:.4f} ms"
        )


def _get_key_func(key: Optional[Callable[[T], Any]]) -> Callable[[T], Any]:
    return key if key is not None else (lambda x: x)


def bubble_sort(
    items: Sequence[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
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
    k = _get_key_func(key)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            val_a = k(arr[j])
            val_b = k(arr[j + 1])
            condition = (val_a < val_b) if reverse else (val_a > val_b)
            if condition:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SortMetrics("Bubble Sort", comparisons, swaps, elapsed_ms)
    return arr, metrics


def insertion_sort(
    items: Sequence[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
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
    k = _get_key_func(key)

    for i in range(1, n):
        current_item = arr[i]
        current_key = k(current_item)
        j = i - 1

        while j >= 0:
            comparisons += 1
            prev_key = k(arr[j])
            condition = (prev_key < current_key) if reverse else (prev_key > current_key)
            if condition:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break

        arr[j + 1] = current_item

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SortMetrics("Insertion Sort", comparisons, shifts, elapsed_ms)
    return arr, metrics


def selection_sort(
    items: Sequence[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
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
    k = _get_key_func(key)

    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            val_j = k(arr[j])
            val_target = k(arr[target_idx])
            condition = (val_j > val_target) if reverse else (val_j < val_target)
            if condition:
                target_idx = j

        if target_idx != i:
            arr[i], arr[target_idx] = arr[target_idx], arr[i]
            swaps += 1

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SortMetrics("Selection Sort", comparisons, swaps, elapsed_ms)
    return arr, metrics


def merge_sort(
    items: Sequence[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
) -> tuple[List[T], SortMetrics]:
    """Sort items using Merge Sort algorithm (Divide and Conquer).

    Time Complexity:
      - Best/Average/Worst: O(n log n)
    Space Complexity: O(n) auxiliary
    """
    start_time = time.perf_counter()
    comparisons = 0
    merges = 0
    k = _get_key_func(key)

    def _merge(left: List[T], right: List[T]) -> List[T]:
        nonlocal comparisons, merges
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
    metrics = SortMetrics("Merge Sort", comparisons, merges, elapsed_ms)
    return sorted_arr, metrics
