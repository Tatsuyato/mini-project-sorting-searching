"""Main application entry point providing an interactive CLI for Student Score Management.

Demonstrates:
- Sorting Algorithms: Bubble Sort, Insertion Sort, Selection Sort, Merge Sort
- Searching Algorithms: Sequential Search, Binary Search
"""
import sys
from typing import List, Optional
from models.student import Student
from services.score_manager import ScoreManager
from algorithms.sorting import SortMetrics
from algorithms.searching import SearchMetrics


def print_header(title: str) -> None:
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def print_table(students: List[Student], caption: Optional[str] = None) -> None:
    """Print student records formatted in an ASCII table."""
    if caption:
        print(f"\n>> {caption} (จำนวน: {len(students)} คน)")
    if not students:
        print("+-------------+---------------------------+---------+-------+")
        print("| ไม่พบข้อมูลนักเรียนในระบบ                           |")
        print("+-------------+---------------------------+---------+-------+")
        return

    print("+-------------+---------------------------+---------+-------+")
    print("| รหัสนักเรียน  | ชื่อ-นามสกุล               | คะแนน   | เกรด  |")
    print("+-------------+---------------------------+---------+-------+")
    for s in students:
        # Format columns with padding
        print(f"| {s.student_id:<11} | {s.name:<25} | {s.score:>7.1f} | {s.grade:>5} |")
    print("+-------------+---------------------------+---------+-------+")


def display_sorting_metrics(metrics: SortMetrics) -> None:
    print("\n" + "-" * 50)
    print(f" ผลการวิเคราะห์ประสิทธิภาพ: {metrics.algorithm_name}")
    print("-" * 50)
    print(f" • จำนวนครั้งที่เปรียบเทียบ (Comparisons) : {metrics.comparisons:,} ครั้ง")
    print(f" • จำนวนการสลับ/จัดวางข้อมูล (Swaps/Ops)  : {metrics.swaps:,} ครั้ง")
    print(f" • เวลาที่ใช้ในการประมวลผล (Elapsed Time): {metrics.execution_time_ms:.4f} ms")
    print("-" * 50)


def display_searching_metrics(metrics: SearchMetrics) -> None:
    print("\n" + "-" * 50)
    print(f" ผลการค้นหาด้วย: {metrics.algorithm_name}")
    print("-" * 50)
    print(f" • สถานะผลลัพธ์                          : {'พบข้อมูล' if metrics.found else 'ไม่พบข้อมูล'}")
    print(f" • จำนวนรอบที่เปรียบเทียบ (Comparisons)  : {metrics.comparisons:,} ครั้ง")
    print(f" • เวลาที่ใช้ในการประมวลผล (Elapsed Time): {metrics.execution_time_ms:.4f} ms")
    print("-" * 50)


def display_trace(traces: List[str], title: str = "ขั้นตอนการทำงาน (Algorithm Trace)") -> None:
    """Print step-by-step execution trace clearly."""
    if not traces:
        return
    print("\n" + "." * 65)
    print(f"  {title}")
    print("." * 65)
    for step in traces:
        print(f"  {step}")
    print("." * 65)


def handle_add_student(manager: ScoreManager) -> None:
    print_header("เพิ่มข้อมูลนักเรียนใหม่")
    student_id = input("กรอกรหัสนักเรียน (เช่น 6601015): ").strip()
    if not student_id:
        print("[!] รหัสนักเรียนต้องไม่เป็นค่าว่าง")
        return

    name = input("กรอกชื่อ-นามสกุล: ").strip()
    if not name:
        print("[!] ชื่อ-นามสกุลต้องไม่เป็นค่าว่าง")
        return

    score_str = input("กรอกคะแนน (0.0 - 100.0): ").strip()
    try:
        score = float(score_str)
        student = Student(student_id=student_id, name=name, score=score)
        manager.add_student(student)
        print(f"[✓] บันทึกข้อมูลนักเรียน {name} (เกรด {student.grade}) สำเร็จเรียบร้อย!")
    except ValueError as e:
        print(f"[!] เกิดข้อผิดพลาด: {e}")


def handle_remove_student(manager: ScoreManager) -> None:
    print_header("ลบข้อมูลนักเรียน")
    if manager.count == 0:
        print("[!] ไม่มีข้อมูลนักเรียนในระบบ")
        return

    student_id = input("กรอกรหัสนักเรียนที่ต้องการลบ: ").strip()
    if manager.remove_student(student_id):
        print(f"[✓] ลบข้อมูลนักเรียนรหัส {student_id} สำเร็จ!")
    else:
        print(f"[!] ไม่พบรหัสนักเรียน '{student_id}' ในระบบ")


def handle_sorting(manager: ScoreManager) -> None:
    print_header("สาธิตการทำงานของ Sorting Algorithms")
    if manager.count == 0:
        print("[!] กรุณาเพิ่มข้อมูลหรือโหลดข้อมูลตัวอย่างก่อนทำการเรียงลำดับ")
        return

    print("เลือกอัลกอริทึมการจัดเรียง:")
    print(" 1) Bubble Sort    (O(n²) - สลับสมาชิกคู่ติดกัน)")
    print(" 2) Insertion Sort (O(n²) - แทรกสมาชิกในตำแหน่งที่ถูกต้อง)")
    print(" 3) Selection Sort (O(n²) - เลือกค่าน้อย/มากที่สุดมาวางด้านหน้า)")
    print(" 4) Merge Sort     (O(n log n) - แบ่งย่อยและผสานตามหลัก Divide & Conquer)")
    algo_choice = input("เลือกหมายเลข (1-4) [ค่าเริ่มต้น: 4]: ").strip() or "4"

    algo_map = {
        "1": "bubble",
        "2": "insertion",
        "3": "selection",
        "4": "merge",
    }
    algo_name = algo_map.get(algo_choice)
    if not algo_name:
        print("[!] ตัวเลือกอัลกอริทึมไม่ถูกต้อง")
        return

    print("\nเลือกเกณฑ์ในการเรียงลำดับ:")
    print(" 1) คะแนน (Score)")
    print(" 2) รหัสนักเรียน (Student ID)")
    print(" 3) ชื่อนักเรียน (Name)")
    key_choice = input("เลือกหมายเลข (1-3) [ค่าเริ่มต้น: 1]: ").strip() or "1"

    key_map = {
        "1": "score",
        "2": "student_id",
        "3": "name",
    }
    key_field = key_map.get(key_choice)
    if not key_field:
        print("[!] ตัวเลือกเกณฑ์ไม่ถูกต้อง")
        return

    print("\nเลือกทิศทางการเรียง:")
    print(" 1) จากน้อยไปมาก (Ascending)")
    print(" 2) จากมากไปน้อย (Descending)")
    order_choice = input("เลือกหมายเลข (1-2) [ค่าเริ่มต้น: 2 สำหรับคะแนน, 1 สำหรับรหัส]: ").strip()
    if not order_choice:
        reverse = True if key_field == "score" else False
    else:
        reverse = (order_choice == "2")

    trace_choice = input("ต้องการแสดงขั้นตอนการทำงานจริง (Trace) หรือไม่? (Y/n) [ค่าเริ่มต้น: Y]: ").strip().lower()
    show_trace = (trace_choice != "n")

    update_choice = input("ต้องการบันทึกผลการจัดเรียงนี้เป็นลำดับหลักของระบบหรือไม่? (y/N): ").strip().lower()
    update_state = (update_choice == "y")

    sorted_list, metrics = manager.sort_students(
        algorithm=algo_name,
        key_field=key_field,
        reverse=reverse,
        update_state=update_state,
        trace=show_trace,
    )

    if show_trace and metrics.traces:
        display_trace(metrics.traces, f"ขั้นตอนการทำงานจริง (Trace): {metrics.algorithm_name}")

    direction_str = "มากไปน้อย" if reverse else "น้อยไปมาก"
    print_table(sorted_list, caption=f"ผลลัพธ์จัดเรียงด้วย {metrics.algorithm_name} (เรียงตาม {key_field} แบบ{direction_str})")
    display_sorting_metrics(metrics)
    if update_state:
        print("[✓] อัปเดตลำดับข้อมูลในระบบเรียบร้อยแล้ว")


def handle_searching(manager: ScoreManager) -> None:
    print_header("สาธิตการทำงานของ Searching Algorithms")
    if manager.count == 0:
        print("[!] กรุณาเพิ่มข้อมูลหรือโหลดข้อมูลตัวอย่างก่อนทำการค้นหา")
        return

    print("เลือกอัลกอริทึมการค้นหา:")
    print(" 1) Sequential Search (ค้นหาเชิงเส้น - ตรวจสอบทีละตัว ไม่จำเป็นต้องเรียงลำดับ)")
    print(" 2) Binary Search     (ค้นหาแบบทวิภาค - ต้องเรียงลำดับข้อมูลก่อน O(log n))")
    search_algo_choice = input("เลือกหมายเลข (1-2) [ค่าเริ่มต้น: 1]: ").strip() or "1"

    print("\nเลือกฟิลด์ที่ต้องการค้นหา:")
    print(" 1) รหัสนักเรียน (Student ID)")
    print(" 2) คะแนน (Score)")
    print(" 3) ชื่อนักเรียน (Name - เฉพาะ Sequential Search)")
    field_choice = input("เลือกหมายเลข (1-3) [ค่าเริ่มต้น: 1]: ").strip() or "1"

    field_map = {"1": "student_id", "2": "score", "3": "name"}
    key_field = field_map.get(field_choice)
    if not key_field:
        print("[!] ฟิลด์ที่เลือกไม่ถูกต้อง")
        return

    if search_algo_choice == "2" and key_field == "name":
        print("[!] การค้นหาด้วย Binary Search ในเมนูนี้รองรับรหัสนักเรียนและคะแนน (เลือกใช้ Sequential Search สำหรับชื่อ)")
        return

    query_val = input(f"กรอกค่า '{key_field}' ที่ต้องการค้นหา: ").strip()
    if not query_val:
        print("[!] คำค้นหาต้องไม่เป็นค่าว่าง")
        return

    trace_choice = input("ต้องการแสดงลำดับขั้นตอนการตรวจสอบ (Trace) หรือไม่? (Y/n) [ค่าเริ่มต้น: Y]: ").strip().lower()
    show_trace = (trace_choice != "n")

    if search_algo_choice == "1":
        matched, metrics = manager.search_students(
            "sequential", query_val, key_field=key_field, trace=show_trace
        )
        if show_trace and metrics.traces:
            display_trace(metrics.traces, f"ลำดับขั้นตอนการตรวจสอบ (Sequential Search Trace): '{query_val}'")
        print_table(matched, caption=f"ผลการค้นหา Sequential Search: '{query_val}'")
        display_searching_metrics(metrics)

    elif search_algo_choice == "2":
        # Check if current list is sorted
        # Binary search default direction check
        is_asc_sorted = manager.is_current_list_sorted(key_field=key_field, reverse=False)
        is_desc_sorted = manager.is_current_list_sorted(key_field=key_field, reverse=True)

        if not is_asc_sorted and not is_desc_sorted:
            print(f"\n[!] คำเตือน: รายการนักเรียนยังไม่ได้เรียงลำดับตาม '{key_field}'")
            auto_sort = input("ต้องการให้ระบบเรียงลำดับข้อมูลอัตโนมัติก่อนค้นหาหรือไม่? (Y/n): ").strip().lower()
            if auto_sort != "n":
                manager.sort_students("merge", key_field=key_field, reverse=False, update_state=True)
                print(f"[✓] เรียงลำดับข้อมูลตาม '{key_field}' แบบน้อยไปมากเรียบร้อยแล้ว")
                is_asc_sorted = True
                is_desc_sorted = False
            else:
                print("[!] ยกเลิกการค้นหา Binary Search เนื่องจากข้อมูลยังไม่ได้รับการจัดเรียง")
                return

        reverse_flag = is_desc_sorted and not is_asc_sorted
        try:
            matched, metrics = manager.search_students(
                "binary", query_val, key_field=key_field, reverse=reverse_flag, trace=show_trace
            )
            if show_trace and metrics.traces:
                display_trace(metrics.traces, f"ลำดับขั้นตอนการตรวจสอบ (Binary Search Trace): '{query_val}'")
            print_table(matched, caption=f"ผลการค้นหา Binary Search: '{query_val}'")
            display_searching_metrics(metrics)
        except ValueError as err:
            print(f"[!] เกิดข้อผิดพลาด: {err}")
    else:
        print("[!] ตัวเลือกการค้นหาไม่ถูกต้อง")


def handle_benchmark(manager: ScoreManager) -> None:
    print_header("เปรียบเทียบประสิทธิภาพ Sorting ทั้ง 4 อัลกอริทึม (Benchmark)")
    if manager.count == 0:
        print("[!] โหลดข้อมูลตัวอย่างให้อัตโนมัติสำหรับการเปรียบเทียบ...")
        manager.load_sample_data()

    print(f"\nชุดข้อมูลทดสอบ: จำนวนนักเรียน {manager.count} รายการ")
    print("กำลังประมวลผลการจัดเรียงบนชุดข้อมูลเดียวกัน...")

    results = manager.benchmark_sorting(key_field="score", reverse=True)

    print("\n+-----------------+-----------------------+---------------------+-------------------+")
    print("| Algorithm       | Comparisons (ครั้ง)   | Swaps/Ops (ครั้ง)   | Execution Time    |")
    print("+-----------------+-----------------------+---------------------+-------------------+")
    for name, metrics in results.items():
        print(f"| {name:<15} | {metrics.comparisons:>21,} | {metrics.swaps:>19,} | {metrics.execution_time_ms:>14.4f} ms |")
    print("+-----------------+-----------------------+---------------------+-------------------+")
    print("หมายเหตุ: ข้อมูลตัวอย่างขนาดเล็ก ค่าเวลาอาจแปรผันตาม CPU ticks แต่สถิติ Comparisons & Swaps สะท้อนความซับซ้อนตามจริง")


def print_main_menu() -> None:
    print("\n" + "=" * 65)
    print("   ระบบจัดการคะแนนนักเรียน - Sorting & Searching Demo (Python)")
    print("=" * 65)
    print(" 1) แสดงรายชื่อนักเรียนทั้งหมด (View All Students)")
    print(" 2) เพิ่มข้อมูลนักเรียน (Add Student)")
    print(" 3) ลบข้อมูลนักเรียน (Delete Student)")
    print(" 4) โหลดชุดข้อมูลตัวอย่าง (Load Demo Data)")
    print(" 5) สาธิตการเรียงลำดับ (Demonstrate Sorting Algorithms)")
    print(" 6) สาธิตการค้นหา (Demonstrate Searching Algorithms)")
    print(" 7) ตารางเปรียบเทียบประสิทธิภาพ Sorting (Benchmark All)")
    print(" 8) ล้างข้อมูลทั้งหมด (Clear All Records)")
    print(" 0) ออกจากโปรแกรม (Exit)")
    print("=" * 65)


def main() -> None:
    manager = ScoreManager()
    # Pre-load sample data for immediate demo readiness
    manager.load_sample_data()
    print("\n[i] เริ่มต้นระบบและโหลดชุดข้อมูลตัวอย่างเรียบร้อยแล้ว (12 รายการ)")

    while True:
        try:
            print_main_menu()
            choice = input("เลือกเมนูที่ต้องการ (0-8): ").strip()

            if choice == "1":
                print_table(manager.get_all_students(), caption="รายชื่อนักเรียนปัจจุบันในระบบ")
            elif choice == "2":
                handle_add_student(manager)
            elif choice == "3":
                handle_remove_student(manager)
            elif choice == "4":
                loaded_count = manager.load_sample_data()
                print(f"[✓] โหลดข้อมูลตัวอย่างสำเร็จ ({loaded_count} รายการ)")
            elif choice == "5":
                handle_sorting(manager)
            elif choice == "6":
                handle_searching(manager)
            elif choice == "7":
                handle_benchmark(manager)
            elif choice == "8":
                confirm = input("ยืนยันการล้างข้อมูลทั้งหมดหรือไม่? (y/N): ").strip().lower()
                if confirm == "y":
                    manager.clear()
                    print("[✓] ล้างข้อมูลทั้งหมดเรียบร้อยแล้ว")
            elif choice == "0":
                print("\nขอบคุณที่ใช้งานโปรแกรม สวัสดีครับ / Goodbye!")
                sys.exit(0)
            else:
                print("[!] เมนูไม่ถูกต้อง กรุณาเลือกตัวเลข 0 ถึง 8")
        except (KeyboardInterrupt, EOFError):
            print("\n\nออกจากโปรแกรมเรียบร้อยแล้ว")
            sys.exit(0)


if __name__ == "__main__":
    main()
