"""Searching algorithms implementation with educational metrics tracking.

Includes:
- Sequential Search (Linear Search)
- Binary Search (with precondition check for sorted list)
"""
from dataclasses import dataclass
import time
from typing import Any, Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")


@dataclass
class SearchMetrics:
    algorithm_name: str
    comparisons: int
    execution_time_ms: float
    found: bool
    is_sorted_validated: Optional[bool] = None

    def __str__(self) -> str:
        status = "Found" if self.found else "Not Found"
        return (
            f"[{self.algorithm_name}] Status: {status}, "
            f"Comparisons: {self.comparisons}, Time: {self.execution_time_ms:.4f} ms"
        )


def _get_key_func(key: Optional[Callable[[T], Any]]) -> Callable[[T], Any]:
    return key if key is not None else (lambda x: x)


def is_sorted(
    items: Sequence[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
) -> bool:
    """Check whether a sequence is sorted according to the given key and direction."""
    if len(items) <= 1:
        return True
    k = _get_key_func(key)
    for i in range(len(items) - 1):
        val_curr = k(items[i])
        val_next = k(items[i + 1])
        if reverse:
            if val_curr < val_next:
                return False
        else:
            if val_curr > val_next:
                return False
    return True


def sequential_search(
    items: Sequence[T],
    target_value: Any,
    key: Optional[Callable[[T], Any]] = None,
) -> tuple[List[int], SearchMetrics]:
    """Search for all occurrences of target_value using Sequential (Linear) Search.

    Time Complexity: O(n)
    Space Complexity: O(k) where k is the number of matches
    """
    start_time = time.perf_counter()
    k = _get_key_func(key)
    matched_indices: List[int] = []
    comparisons = 0

    for idx, item in enumerate(items):
        comparisons += 1
        item_val = k(item)
        # Normalize strings for comparison if both are strings
        if isinstance(item_val, str) and isinstance(target_value, str):
            if item_val.strip().lower() == target_value.strip().lower():
                matched_indices.append(idx)
        else:
            if item_val == target_value:
                matched_indices.append(idx)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SearchMetrics(
        algorithm_name="Sequential Search",
        comparisons=comparisons,
        execution_time_ms=elapsed_ms,
        found=len(matched_indices) > 0,
        is_sorted_validated=None,
    )
    return matched_indices, metrics


def binary_search(
    items: Sequence[T],
    target_value: Any,
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    validate_sorted: bool = True,
) -> tuple[Optional[int], SearchMetrics]:
    """Search for target_value using Binary Search on a sorted sequence.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Raises:
        ValueError: If validate_sorted is True and the sequence is not sorted.
    """
    start_time = time.perf_counter()
    k = _get_key_func(key)

    sorted_valid = None
    if validate_sorted:
        sorted_valid = is_sorted(items, key=key, reverse=reverse)
        if not sorted_valid:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            raise ValueError(
                "Binary Search requires items to be sorted before searching. "
                "Please sort the list first!"
            )

    low = 0
    high = len(items) - 1
    comparisons = 0
    found_index: Optional[int] = None

    # Handle string comparison normalization if target is str
    def _normalize(v: Any) -> Any:
        return v.strip().lower() if isinstance(v, str) else v

    normalized_target = _normalize(target_value)

    while low <= high:
        mid = (low + high) // 2
        mid_val = _normalize(k(items[mid]))
        comparisons += 1

        if mid_val == normalized_target:
            found_index = mid
            break

        # Check search direction
        if not reverse:
            # Ascending order
            if mid_val < normalized_target:
                low = mid + 1
            else:
                high = mid - 1
        else:
            # Descending order
            if mid_val > normalized_target:
                low = mid + 1
            else:
                high = mid - 1

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SearchMetrics(
        algorithm_name="Binary Search",
        comparisons=comparisons,
        execution_time_ms=elapsed_ms,
        found=found_index is not None,
        is_sorted_validated=sorted_valid,
    )
    return found_index, metrics
