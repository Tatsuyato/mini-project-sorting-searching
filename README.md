# Mini Project: ระบบจัดการคะแนนนักเรียน (Student Score Management System)
> โครงงานสาธิตอัลกอริทึมการจัดเรียง (Sorting) และการค้นหา (Searching) ด้วยภาษา Python (Clean Architecture & Zero External Dependencies)

---

## 📌 บทนำและภาพรวมโครงการ

โครงงานนี้พัฒนาขึ้นเพื่อเป็นสื่อการเรียนรู้และระบบต้นแบบการจัดการคะแนนนักเรียน โดยมุ่งเน้นการนำเสนอหลักการทำงานและการเปรียบเทียบประสิทธิภาพของอัลกอริทึมพื้นฐานที่สำคัญในวิทยาการคอมพิวเตอร์:

- **Sorting Algorithms (การจัดเรียงลำดับ)**:
  1. **Bubble Sort** (พร้อม Early-exit optimization เมื่อข้อมูลเรียงแล้ว)
  2. **Insertion Sort**
  3. **Selection Sort**
  4. **Merge Sort** (Divide and Conquer)
- **Searching Algorithms (การค้นหาข้อมูล)**:
  1. **Sequential Search** (Linear Search)
  2. **Binary Search** (พร้อม Precondition validation ตรวจสอบความถูกต้องของ Sorted array)

ระบบถูกออกแบบเชิงโมดูลาร์ (Modular Architecture) แยกส่วน Model, Algorithm, Service และ Presentation (CLI) ไว้อย่างชัดเจน พร้อมระบบบันทึก Metrics (Comparisons, Swaps/Ops, Execution Time) ในทุกอัลกอริทึม

---

## 📊 ตารางสรุป Time & Space Complexity

| อัลกอริทึม | Best Case | Average Case | Worst Case | Space Complexity | เสถียรภาพ (Stability) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Bubble Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Stable |
| **Insertion Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Stable |
| **Selection Sort** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Unstable |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Stable |
| **Sequential Search** | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | - |
| **Binary Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | - |

---

## 🏗 โครงสร้างโฟลเดอร์ของโปรเจกต์

```text
mini-project-sorting-searching/
├── .gitignore               # การตั้งค่าละเว้นไฟล์ชั่วคราว
├── README.md                # เอกสารประกอบโครงการ
├── main.py                  # จุดเข้าใช้งานหลัก (Interactive CLI Menu ภาษาไทย)
├── models/
│   ├── __init__.py
│   └── student.py           # Student Data Model พร้อมระบบคำนวณเกรดและ Validation
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py           # Bubble, Insertion, Selection, Merge Sort พร้อม SortMetrics
│   └── searching.py         # Sequential Search, Binary Search พร้อม SearchMetrics
├── services/
│   ├── __init__.py
│   └── score_manager.py     # Service จัดการ State รายการนักเรียนและประสานงานอัลกอริทึม
└── tests/
    ├── __init__.py
    ├── test_sorting.py       # Unit tests ทดสอบ Sorting algorithms (Edge cases & Objects)
    ├── test_searching.py     # Unit tests ทดสอบ Searching algorithms (Preconditions & Results)
    └── test_score_manager.py # Unit tests ทดสอบ Data model และ Service layer
```

---

## 🚀 ความต้องการระบบและการติดตั้ง

- **Python Runtime**: Python 3.10 ขึ้นไป (ทดสอบกับ Python 3.11.15)
- **Dependencies**: ใช้เฉพาะ Standard Library ของ Python (Zero External Dependencies ไม่ต้องลง `pip install` เพิ่มเติม)

---

## 💻 การเรียกใช้งานโปรแกรม (Usage)

รันโปรแกรมผ่าน Terminal หรือ Command Prompt:

```bash
python3 main.py
```

### ฟังก์ชันหลักในเมนูของโปรแกรม:
1. **แสดงรายชื่อนักเรียนทั้งหมด**: แสดงผลตาราง ASCII ระบุรหัสนักเรียน ชื่อ คะแนน และเกรด
2. **เพิ่มข้อมูลนักเรียน**: รองรับการตรวจสอบข้อมูลซ้ำ และ validation คะแนน 0.0 - 100.0
3. **ลบข้อมูลนักเรียน**: ลบข้อมูลด้วยรหัสนักเรียน
4. **โหลดชุดข้อมูลตัวอย่าง**: โหลดข้อมูลนักเรียนจำลอง 12 รายการเพื่อการทดสอบทันที
5. **สาธิตการเรียงลำดับ**:
   - เลือกอัลกอริทึมได้ทั้ง 4 ตัว
   - เลือกคีย์การเรียง: คะแนน (Score), รหัส (ID) หรือ ชื่อ (Name)
   - เลือกลำดับ: น้อยไปมาก หรือ มากไปน้อย
   - แสดงสถิติ: Comparisons, Swaps และ Elapsed Time (ms)
6. **สาธิตการค้นหาข้อมูล**:
   - Sequential Search: ค้นหาได้ทันที ไม่ต้องเรียงลำดับ
   - Binary Search: ตรวจสอบความถูกต้องของ Sorted array อัตโนมัติ (หากยังไม่เรียงจะมีตัวเลือกให้เรียงทันที)
7. **ตารางเปรียบเทียบประสิทธิภาพ (Benchmark All)**: รันการจัดเรียงทั้ง 4 อัลกอริทึมบนชุดข้อมูลเดียวกัน พร้อมตารางสรุปเปรียบเทียบ
8. **ล้างข้อมูลทั้งหมด**: เคลียร์ข้อมูลในระบบ

---

## 🧪 การทดสอบแบบอัตโนมัติ (Automated Testing)

โปรเจกต์มีชุดการทดสอบ Unit Tests ครอบคลุม 30 กรณีทดสอบ (Edge Cases, Negative Cases, Object Sorting, Precondition Checks):

```bash
python3 -m unittest discover -s tests -v
```

ตัวอย่างผลการทดสอบ:
```text
Ran 30 tests in 0.015s
OK
```
