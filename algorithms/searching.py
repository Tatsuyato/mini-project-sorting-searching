"""Searching algorithms implementation with educational metrics tracking.

Includes:
- Sequential Search (Linear Search)
- Binary Search (with precondition check for sorted list)
"""
from dataclasses import dataclass, field
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
    traces: List[str] = field(default_factory=list)

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
    trace: bool = False,
    max_trace_lines: int = 15,
) -> tuple[List[int], SearchMetrics]:
    """Search for all occurrences of target_value using Sequential (Linear) Search.

    Time Complexity: O(n)
    Space Complexity: O(k) where k is the number of matches
    """
    start_time = time.perf_counter()
    k = _get_key_func(key)
    matched_indices: List[int] = []
    comparisons = 0
    traces: List[str] = []

    def _repr_v(v: Any) -> str:
        return f"{v:.1f}" if isinstance(v, float) else str(v)

    target_repr = _repr_v(target_value)
    if trace:
        traces.append(f"เริ่มต้น Sequential Search: ค้นหาเป้าหมาย '{target_repr}' ในข้อมูล {len(items)} รายการ")

    skipped_count = 0
    for idx, item in enumerate(items):
        comparisons += 1
        item_val = k(item)
        val_repr = _repr_v(item_val)

        # Normalize strings for comparison if both are strings
        if isinstance(item_val, str) and isinstance(target_value, str):
            is_match = item_val.strip().lower() == target_value.strip().lower()
        else:
            is_match = item_val == target_value

        if is_match:
            matched_indices.append(idx)

        if trace:
            if idx < max_trace_lines or is_match:
                status_str = "[✓ พบข้อมูลที่ตรงกัน]" if is_match else "[ยังไม่ตรง]"
                traces.append(f"Step {idx + 1:02d}: Index {idx:02d} -> ค่า '{val_repr}' {status_str}")
            else:
                skipped_count += 1

    if trace:
        if skipped_count > 0:
            traces.append(f"... (ย่อการแสดงผล {skipped_count} รายการที่ไม่ตรง เพื่อไม่ให้หน้าจอล้น)")
        traces.append(
            f"สรุป: ตรวจสอบครบ {comparisons} รายการ, พบข้อมูลทั้งหมด {len(matched_indices)} รายการ"
        )

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SearchMetrics(
        algorithm_name="Sequential Search",
        comparisons=comparisons,
        execution_time_ms=elapsed_ms,
        found=len(matched_indices) > 0,
        is_sorted_validated=None,
        traces=traces,
    )
    return matched_indices, metrics


def binary_search(
    items: Sequence[T],
    target_value: Any,
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
    validate_sorted: bool = True,
    trace: bool = False,
) -> tuple[Optional[int], SearchMetrics]:
    """Search for target_value using Binary Search on a sorted sequence.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Raises:
        ValueError: If validate_sorted is True and the sequence is not sorted.
    """
    start_time = time.perf_counter()
    k = _get_key_func(key)
    traces: List[str] = []

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

    def _repr_v(v: Any) -> str:
        return f"{v:.1f}" if isinstance(v, float) else str(v)

    # Handle string comparison normalization if target is str
    def _normalize(v: Any) -> Any:
        return v.strip().lower() if isinstance(v, str) else v

    normalized_target = _normalize(target_value)
    target_repr = _repr_v(target_value)

    if trace:
        order_desc = "มากไปน้อย (Descending)" if reverse else "น้อยไปมาก (Ascending)"
        traces.append(
            f"เริ่มต้น Binary Search: ค้นหา '{target_repr}', ขอบเขตเริ่มต้น [0 .. {len(items) - 1}] ({order_desc})"
        )

    step = 0
    while low <= high:
        step += 1
        mid = (low + high) // 2
        mid_raw = k(items[mid])
        mid_val = _normalize(mid_raw)
        mid_repr = _repr_v(mid_raw)
        comparisons += 1

        if mid_val == normalized_target:
            found_index = mid
            if trace:
                traces.append(
                    f"Step {step:02d}: ช่วง [{low}..{high}], Mid={mid} (ค่า '{mid_repr}') == '{target_repr}' [✓ พบข้อมูลที่ Index {mid}]"
                )
            break

        # Check search direction
        if not reverse:
            # Ascending order
            if mid_val < normalized_target:
                if trace:
                    traces.append(
                        f"Step {step:02d}: ช่วง [{low}..{high}], Mid={mid} (ค่า '{mid_repr}') < '{target_repr}' -> ขยับขอบเขตไปฝั่งขวา [{mid + 1}..{high}]"
                    )
                low = mid + 1
            else:
                if trace:
                    traces.append(
                        f"Step {step:02d}: ช่วง [{low}..{high}], Mid={mid} (ค่า '{mid_repr}') > '{target_repr}' -> ขยับขอบเขตไปฝั่งซ้าย [{low}..{mid - 1}]"
                    )
                high = mid - 1
        else:
            # Descending order
            if mid_val > normalized_target:
                if trace:
                    traces.append(
                        f"Step {step:02d}: ช่วง [{low}..{high}], Mid={mid} (ค่า '{mid_repr}') > '{target_repr}' -> ขยับขอบเขตไปฝั่งขวา [{mid + 1}..{high}]"
                    )
                low = mid + 1
            else:
                if trace:
                    traces.append(
                        f"Step {step:02d}: ช่วง [{low}..{high}], Mid={mid} (ค่า '{mid_repr}') < '{target_repr}' -> ขยับขอบเขตไปฝั่งซ้าย [{low}..{mid - 1}]"
                    )
                high = mid - 1

    if trace and found_index is None:
        traces.append(
            f"สิ้นสุดการค้นหา: ไม่พบค่า '{target_repr}' ในระบบ (ขอบเขต low={low} > high={high})"
        )

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    metrics = SearchMetrics(
        algorithm_name="Binary Search",
        comparisons=comparisons,
        execution_time_ms=elapsed_ms,
        found=found_index is not None,
        is_sorted_validated=sorted_valid,
        traces=traces,
    )
    return found_index, metrics
