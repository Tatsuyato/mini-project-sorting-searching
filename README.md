# ระบบจัดการคะแนนนักเรียน (Student Score Management System)
### สาธิตการทำงานและเปรียบเทียบประสิทธิภาพ Sorting & Searching Algorithms ด้วย Python

โปรเจกต์ขนาดเล็ก (Mini Project) ภาษา Python สำหรับการศึกษาการทำงานของขั้นตอนวิธี (Algorithms) ในหมวดการจัดเรียงข้อมูล (**Sorting**) และการค้นหาข้อมูล (**Searching**) ผ่านระบบจัดการข้อมูลคะแนนและเกรดของนักเรียน พร้อมเครื่องมือตรวจวัดประสิทธิภาพเชิงปริมาณ (Time & Operation Metrics)

---

## 📌 จุดเด่นของระบบ (Features)

1. **สถาปัตยกรรมแบบแยกส่วน (Layered Architecture)**:
   - **Domain Layer (`models/`)**: จัดการข้อมูลนักเรียน มีการตรวจสอบความถูกต้อง (Validation) ของรหัส, ชื่อ และช่วงคะแนน (0.0 – 100.0) พร้อมตัดเกรด A, B+, B, C+, C, D+, D, F อัตโนมัติ
   - **Algorithm Core (`algorithms/`)**: อัลกอริทึมถูกเขียนเป็น Pure Functions และ Generic Type ไม่ขึ้นต่อโมเดลใดโมเดลหนึ่งโดยตรง รองรับ Custom Key Selector และการจัดเรียงทั้งแบบน้อยไปมาก (Ascending) และมากไปน้อย (Descending)
   - **Service Layer (`services/`)**: จัดการ CRUD ใน Memory, รันการเปรียบเทียบประสิทธิภาพพร้อมกัน (Benchmark), และควบคุมความถูกต้องของเงื่อนไข (Preconditions)
   - **CLI Presentation (`main.py`)**: หน้าต่างคำสั่งแบบเมนูโต้ตอบภาษาไทย แสดงตารางข้อมูลแบบ ASCII Table อย่างสวยงามและเป็นระเบียบ

2. **ระบบวัดประสิทธิภาพเพื่อการศึกษา (Educational Metrics)**:
   - บันทึกจำนวนรอบที่เปรียบเทียบข้อมูล (**Comparisons**)
   - บันทึกจำนวนครั้งที่มีการสลับค่า/เลื่อนข้อมูล/ผสานข้อมูล (**Swaps / Shifts / Merges**)
   - จับเวลาการประมวลผลจริงในระดับมิลลิวินาที (**Elapsed Time in ms**) ผ่าน `time.perf_counter()`

3. **การตรวจสอบเงื่อนไขก่อนค้นหา (Pre-condition Enforcement)**:
   - Binary Search จะตรวจสอบล่วงหน้าเสมอว่าลิสต์ได้รับการเรียงลำดับแล้วหรือไม่ หากยังไม่เรียง จะแจ้งเตือนและมีตัวเลือกช่วยเรียงลำดับให้อัตโนมัติ

---

## 📊 ตารางวิเคราะห์ขั้นตอนวิธี (Algorithm Complexity)

### 1. อัลกอริทึมการจัดเรียง (Sorting Algorithms)

| อัลกอริทึม | Best Case | Average Case | Worst Case | Space Complexity | Stability | คุณลักษณะเด่น |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Bubble Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Stable | มี Early-exit flag หยุดทันทีเมื่อไม่มีการสลับค่าในรอบนั้น |
| **Insertion Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Stable | มีประสิทธิภาพสูงมากเมื่อข้อมูลเกือบเรียงลำดับอยู่แล้ว (Nearly Sorted) |
| **Selection Sort** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Unstable | ทำการสลับข้อมูล (Swap) น้อยที่สุด ไม่เกิน $n-1$ ครั้ง |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Stable | ใช้หลัก Divide and Conquer รับประกันประสิทธิภาพ $O(n \log n)$ ทุกกรณี |

### 2. อัลกอริทึมการค้นหา (Searching Algorithms)

| อัลกอริทึม | Best Case | Average Case | Worst Case | Space Complexity | เงื่อนไขข้อมูลนำเข้า (Precondition) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Sequential Search** | $O(1)$ | $O(n)$ | $O(n)$ | $O(k)^*$ | ข้อมูลไม่จำเป็นต้องเรียงลำดับ ค้นหาได้ทุกรายการที่ตรงกัน |
| **Binary Search** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | **ต้องเรียงลำดับข้อมูลก่อนเสมอ** (Sorted array) |

*\* $k$ คือจำนวนรายการที่ค้นหาพบ*

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
mini-project-sorting-searching/
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py          # การทำงานของ Bubble, Insertion, Selection, Merge Sort
│   └── searching.py        # การทำงานของ Sequential และ Binary Search
├── models/
│   ├── __init__.py
│   └── student.py          # Student dataclass และการคำนวณเกรด
├── services/
│   ├── __init__.py
│   ├── mock_data.py        # ตัวสร้างข้อมูลสังเคราะห์จำลองสำหรับการสาธิต (Synthetic Mock Data)
│   └── score_manager.py    # Business logic, state management และ benchmark
├── tests/
│   ├── __init__.py
│   ├── test_sorting.py      # Unit tests สำหรับ Sorting Algorithms
│   ├── test_searching.py    # Unit tests สำหรับ Searching Algorithms
│   ├── test_score_manager.py# Unit tests สำหรับ Model และ Service
│   └── test_mock_data.py    # Unit tests สำหรับ Mock Data และ CLI arguments
├── main.py                 # โปรแกรมหลัก (Interactive CLI Interface)
├── .gitignore
└── README.md
```

---

## 🚀 วิธีการติดตั้งและเริ่มใช้งาน

โปรเจกต์นี้เขียนด้วย **Python 3 Standard Library** ล้วน จึงไม่จำเป็นต้องติดตั้งไลบรารีภายนอกเพิ่มเติม

### ความต้องการของระบบ:
- Python 3.9 ขึ้นไป (ทดสอบบน Python 3.11)

### 1. เรียกใช้งานโปรแกรมแบบ Interactive (CLI)

#### โหมดปกติ (ข้อมูลตัวอย่าง 12 รายการ)
```bash
python3 main.py
```

#### โหมดข้อมูลสังเคราะห์จำลองสำหรับการสาธิต (ค่าเริ่มต้น 12 รายการ)
สำหรับการสาธิตการทำงานของขั้นตอนวิธี Sorting และ Searching สามารถเปิดโหมดข้อมูลจำลองได้โดยระบุ Flag `--mock-data` หรือใช้ alias `-data-test`, `--data-test`, หรือ `--mock`:
```bash
# ใช้ข้อมูลจำลองค่าเริ่มต้น 12 รายการ
python3 main.py -data-test

# ระบุจำนวนข้อมูลเองได้ ตั้งแต่ 1 ถึง 1,000,000 รายการ
python3 main.py -data-test --mock-count 50
python3 main.py --data-test --mock-count 1000
```
ระบบตรวจสอบจำนวนข้อมูลและจะปฏิเสธค่าที่น้อยกว่า 1 หรือมากกว่า 1,000,000 เพื่อป้องกันการใช้หน่วยความจำเกินโดยไม่ตั้งใจ

### เมนูการใช้งานในโปรแกรม:
1. `แสดงรายชื่อนักเรียนทั้งหมด (View All Students)`
2. `เพิ่มข้อมูลนักเรียน (Add Student)`
3. `ลบข้อมูลนักเรียน (Delete Student)`
4. `โหลดชุดข้อมูลตัวอย่าง (Load Demo Data)` - โหลดข้อมูลนักเรียน 12 คน (หรือโหลดข้อมูลจำลองซ้ำในโหมด Mock Data)
5. `สาธิตการเรียงลำดับ (Demonstrate Sorting Algorithms)` - เลือกอัลกอริทึม, เกณฑ์เรียง (คะแนน/รหัส/ชื่อ), ทิศทาง (น้อยไปมาก/มากไปน้อย)
6. `สาธิตการค้นหา (Demonstrate Searching Algorithms)` - ค้นหาแบบเชิงเส้นหรือทวิภาค
7. `ตารางเปรียบเทียบประสิทธิภาพ Sorting (Benchmark All)` - ประมวลผลเปรียบเทียบ 4 อัลกอริทึมพร้อมกัน
8. `ล้างข้อมูลทั้งหมด (Clear All Records)`
0. `ออกจากโปรแกรม (Exit)`

---

## 🔒 ข้อชี้แจงเกี่ยวกับข้อมูลสังเคราะห์และจริยธรรมข้อมูล (Synthetic Data & Privacy Notice)

- **ข้อมูลสังเคราะห์ 100% (Synthetic / Mock Data Only):** ข้อมูลนักเรียนทั้งหมดในระบบ ทั้งในโหมดเริ่มต้น (12 รายการ) และโหมดข้อมูลจำลองสำหรับการสาธิต (`--mock-data` / `--mock-count` สูงสุด 1,000,000 รายการ) เป็น **ข้อมูลสังเคราะห์ที่สร้างขึ้นเพื่อการศึกษาเท่านั้น** โดยใช้รูปแบบรหัสปลอม เช่น `TEST0001` และชื่อปลอม เช่น `นักเรียนทดสอบ 001`
- **ไม่มีการใช้ข้อมูลส่วนบุคคลจริง:** ทางผู้จัดทำ **ไม่มีการคัดลอก เผยแพร่ หรือจัดเก็บชื่อจริง นามสกุลจริง หรือรหัสนักศึกษาจริง** จากระบบสารสนเทศของสถาบันการศึกษาใด ๆ
- **หมายเหตุแหล่งอ้างอิง:** ลิงก์ระบบบริการการศึกษา [https://reg.skru.ac.th/registrar/studentset.asp?cmd=1&campusid=1&groupyear=681&studentgroup=10874&avs236771226=5](https://reg.skru.ac.th/registrar/studentset.asp?cmd=1&campusid=1&groupyear=681&studentgroup=10874&avs236771226=5) ถูกนำมาใช้เพื่อเป็นแนวทางอ้างอิง **โครงสร้างและบริบทของข้อมูลกลุ่มเรียน (Student Group Data Structure & Context)** เท่านั้น มิใช่การนำข้อมูลส่วนบุคคลจริงมาใช้ในระบบ

---

## 🧪 การทดสอบชุดคำสั่ง (Testing & Verification)

### รัน Unit Tests ด้วย pytest
```bash
pytest -v
```

### รัน Unit Tests ด้วย unittest (Standard Library)
```bash
python3 -m unittest discover -s tests -v
```

### ตรวจสอบ Syntax และ Compilation
```bash
python3 -m py_compile main.py models/*.py algorithms/*.py services/*.py tests/*.py
```

