from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = '/home/ryu/mini-project-sorting-searching/เอกสารประกอบมินิโปรเจกต์_Sorting_Searching.pdf'
FONT = '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'
pdfmetrics.registerFont(TTFont('Loma', FONT))
pdfmetrics.registerFont(TTFont('Loma-Bold', FONT_BOLD))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='THTitle', fontName='Loma-Bold', fontSize=23, leading=31, alignment=TA_CENTER, textColor=colors.HexColor('#17365D'), spaceAfter=12))
styles.add(ParagraphStyle(name='THSubtitle', fontName='Loma', fontSize=15, leading=23, alignment=TA_CENTER, textColor=colors.HexColor('#444444'), spaceAfter=8))
styles.add(ParagraphStyle(name='THH1', fontName='Loma-Bold', fontSize=17, leading=24, textColor=colors.HexColor('#17365D'), spaceBefore=8, spaceAfter=8))
styles.add(ParagraphStyle(name='THH2', fontName='Loma-Bold', fontSize=14, leading=21, textColor=colors.HexColor('#24527A'), spaceBefore=6, spaceAfter=5))
styles.add(ParagraphStyle(name='THBody', fontName='Loma', fontSize=11.2, leading=17, spaceAfter=5))
styles.add(ParagraphStyle(name='THSmall', fontName='Loma', fontSize=9.5, leading=14, spaceAfter=3))
styles.add(ParagraphStyle(name='THBullet', fontName='Loma', fontSize=11, leading=17, leftIndent=16, firstLineIndent=-10, bulletIndent=3, spaceAfter=3))
styles.add(ParagraphStyle(name='THCode', fontName='Loma', fontSize=9.5, leading=14, backColor=colors.HexColor('#F2F4F7'), borderColor=colors.HexColor('#D5DCE5'), borderWidth=.5, borderPadding=6, spaceAfter=8))

P = lambda text, style='THBody': Paragraph(text, styles[style])
B = lambda text: Paragraph('• ' + text, styles['THBullet'])

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Loma', 8.5)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(18*mm, 10*mm, 'Mini Project: Sorting & Searching | Python')
    canvas.drawRightString(192*mm, 10*mm, f'หน้า {doc.page}')
    canvas.restoreState()

def table(data, widths, header=True, small=False):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign='LEFT')
    ts = [
        ('FONTNAME', (0,0), (-1,-1), 'Loma'),
        ('FONTSIZE', (0,0), (-1,-1), 8.8 if small else 9.5),
        ('LEADING', (0,0), (-1,-1), 12 if small else 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), .35, colors.HexColor('#AAB7C4')),
        ('LEFTPADDING', (0,0), (-1,-1), 5), ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]
    if header:
        ts += [('BACKGROUND', (0,0), (-1,0), colors.HexColor('#DCE6F1')), ('FONTNAME', (0,0), (-1,0), 'Loma-Bold')]
    for r in range(1 if header else 0, len(data)):
        if r % 2 == 0: ts.append(('BACKGROUND', (0,r), (-1,r), colors.HexColor('#F7F9FB')))
    t.setStyle(TableStyle(ts))
    return t

story=[]
story += [Spacer(1, 28*mm), P('เอกสารประกอบมินิโปรเจกต์', 'THTitle'), P('ระบบจัดการคะแนนนักเรียน<br/>สาธิตอัลกอริทึมการเรียงลำดับและการค้นหาข้อมูล', 'THSubtitle'), Spacer(1, 10*mm)]
story += [P('<b>รายวิชา:</b> โครงสร้างข้อมูลและขั้นตอนวิธี', 'THBody'), P('<b>ภาษาในการพัฒนา:</b> Python 3 (Standard Library)', 'THBody'), P('<b>กำหนดส่งและนำเสนอ:</b> วันที่ 5 ตุลาคม 2569 เวลา 13.00–16.00 น.', 'THBody'), Spacer(1, 8*mm)]
story += [P('<b>สมาชิกกลุ่ม</b>', 'THH2')]
for x in ['รัตนพล ไชยคีรี — 684234034','ธาดา ผ่องสุวรรณ — 684234018','ทัฬห์ พูลศิริสุข — 684234029','จิรัชญา บุญเกิด — 684234001','ชยางกูร สุวิชญางกูร — 684234016','ธนิษฐา สระทอง — 684234017']:
    story.append(B(x))
story += [Spacer(1, 8*mm), P('เอกสารฉบับนี้จัดทำขึ้นเพื่ออธิบายแนวคิด อัลกอริทึม โครงสร้างโปรแกรม วิธีใช้งาน และแนวทางการสาธิตโปรแกรมตามโจทย์มินิโปรเจกต์', 'THBody'), PageBreak()]

story += [P('1. บทนำและวัตถุประสงค์', 'THH1'), P('มินิโปรเจกต์นี้พัฒนาโปรแกรมจัดการคะแนนนักเรียน โดยใช้ข้อมูลรหัสนักเรียน ชื่อ และคะแนนเป็นตัวอย่างในการสาธิตการทำงานของอัลกอริทึมการเรียงลำดับ (Sorting) และการค้นหาข้อมูล (Searching) ผู้ใช้สามารถเลือกอัลกอริทึม ดูผลลัพธ์ ดูสถิติการทำงาน และเปิดโหมด Trace เพื่อดูขั้นตอนระหว่างการประมวลผลได้', 'THBody'), P('<b>วัตถุประสงค์</b>', 'THH2')]
for x in ['ศึกษาและอธิบายหลักการของ Bubble Sort, Insertion Sort, Selection Sort และ Merge Sort','ศึกษาและอธิบาย Sequential Search และ Binary Search','พัฒนาโปรแกรม Python ที่แสดงผลการทำงานของอัลกอริทึมอย่างเป็นรูปธรรม','เปรียบเทียบจำนวนการเปรียบเทียบ การสลับ/จัดวางข้อมูล และเวลาในการทำงาน','สร้างสื่อประกอบการนำเสนอและทำให้สมาชิกทุกคนสามารถอธิบายโปรแกรมได้']:
    story.append(B(x))
story += [P('2. ขอบเขตและความสามารถของระบบ', 'THH1')]
for x in ['เพิ่มข้อมูลนักเรียน ตรวจสอบรหัสซ้ำ และตรวจสอบคะแนนให้อยู่ในช่วง 0–100','แสดงรายชื่อนักเรียนพร้อมคะแนนและเกรด','ลบข้อมูลนักเรียนและโหลดข้อมูลตัวอย่าง 12 รายการ','เรียงข้อมูลตามคะแนน รหัสนักเรียน หรือชื่อ ทั้งแบบน้อยไปมากและมากไปน้อย','ค้นหาด้วยรหัสหรือคะแนนด้วย Sequential Search และ Binary Search','แสดงขั้นตอน Trace แบบจำกัดจำนวนบรรทัดเพื่อให้เหมาะกับการสาธิต','แสดง Benchmark ของ Sorting ทั้ง 4 วิธี โดยไม่ทำให้โหมด Trace กระทบผล Benchmark']:
    story.append(B(x))
story += [P('3. โครงสร้างโปรเจกต์', 'THH1')]
story.append(P('<font name="Loma">mini-project-sorting-searching/<br/>├── algorithms/ — sorting.py, searching.py<br/>├── models/ — student.py<br/>├── services/ — score_manager.py<br/>├── tests/ — ชุดทดสอบอัตโนมัติ<br/>├── main.py — เมนูโปรแกรมหลัก<br/>└── README.md — คู่มือและตารางความซับซ้อน</font>', 'THCode'))
story += [P('การออกแบบแบ่งเป็นชั้น ได้แก่ โมเดลข้อมูล (Student) แกนอัลกอริทึม ฟังก์ชันบริการจัดการข้อมูล และส่วนติดต่อผู้ใช้แบบ Command Line ทำให้สามารถทดสอบและอธิบายแต่ละส่วนแยกกันได้', 'THBody'), PageBreak()]

story += [P('4. ความรู้พื้นฐาน: Sorting', 'THH1'), P('Sorting คือการจัดเรียงข้อมูลตามเกณฑ์ที่กำหนด เช่น คะแนนจากน้อยไปมาก หรือจากมากไปน้อย ประสิทธิภาพมักอธิบายด้วย Big-O ซึ่งใช้บอกแนวโน้มเวลาหรือหน่วยความจำเมื่อจำนวนข้อมูลเพิ่มขึ้น', 'THBody')]
sort_rows=[['อัลกอริทึม','หลักการทำงาน','Best / Average / Worst','จุดเด่น'],['Bubble Sort','เปรียบเทียบสมาชิกที่อยู่ติดกันและสลับเมื่ออยู่ผิดลำดับ','O(n) / O(n²) / O(n²)','เข้าใจง่าย และหยุดเร็วได้เมื่อข้อมูลเรียงแล้ว'],['Insertion Sort','หยิบสมาชิกทีละตัวแล้วแทรกในตำแหน่งที่ถูกต้อง','O(n) / O(n²) / O(n²)','เหมาะกับข้อมูลเกือบเรียงลำดับ'],['Selection Sort','เลือกค่าน้อยสุดหรือมากสุดจากส่วนที่เหลือมาวางตำแหน่งถัดไป','O(n²) / O(n²) / O(n²)','จำนวนการสลับไม่มาก'],['Merge Sort','แบ่งข้อมูลเป็นส่วนย่อย เรียงแต่ละส่วน แล้วผสานกลับ','O(n log n) / O(n log n) / O(n log n)','ประสิทธิภาพสม่ำเสมอและเหมาะกับข้อมูลมาก']]
story.append(table(sort_rows,[28*mm,57*mm,38*mm,57*mm],small=True))
story += [P('4.1 Bubble Sort', 'THH2'), P('เริ่มจากสมาชิกคู่ติดกันทางซ้าย เปรียบเทียบกัน หากตัวซ้ายมากกว่าตัวขวาในกรณีเรียงน้อยไปมากให้สลับกัน เมื่อจบรอบ ค่าที่มากที่สุดจะถูกดันไปอยู่ด้านขวาสุด จากนั้นลดขอบเขตและทำซ้ำจนเรียงครบ หากไม่มีการสลับในรอบใด สามารถหยุดก่อนครบทุกประธานได้', 'THBody'), P('4.2 Insertion Sort', 'THH2'), P('มองส่วนซ้ายว่าเรียงแล้ว แล้วหยิบสมาชิกถัดไปมาเปรียบเทียบกับสมาชิกด้านซ้าย หากมากกว่าหรือผิดตำแหน่ง ให้เลื่อนสมาชิกเดิมไปทางขวาและแทรกสมาชิกที่หยิบมาในช่องว่าง วิธีนี้ทำงานดีเมื่อข้อมูลเกือบเรียงอยู่แล้ว', 'THBody'), P('4.3 Selection Sort', 'THH2'), P('ค้นหาสมาชิกที่มีค่าน้อยที่สุดในส่วนที่ยังไม่เรียง แล้วสลับมาไว้ตำแหน่งปัจจุบัน ทำซ้ำโดยเลื่อนตำแหน่งไปทางขวา จุดสังเกตคือแม้ข้อมูลจะเรียงอยู่แล้วก็ยังต้องตรวจสอบหลายคู่ จึงมีเวลา O(n²) ทุกกรณี', 'THBody'), P('4.4 Merge Sort', 'THH2'), P('ใช้แนวคิด Divide and Conquer แบ่งรายการครึ่งหนึ่งซ้ำจนเหลือรายการขนาดหนึ่ง จากนั้นผสานรายการย่อยสองฝั่งโดยเลือกค่าที่เหมาะสมทีละตัว จึงมีความซับซ้อน O(n log n) แต่ใช้หน่วยความจำเสริม O(n)', 'THBody'), PageBreak()]

story += [P('5. ความรู้พื้นฐาน: Searching', 'THH1')]
search_rows=[['อัลกอริทึม','หลักการทำงาน','ความซับซ้อน','เงื่อนไข'],['Sequential Search','ตรวจสมาชิกตั้งแต่ต้นรายการทีละตัวจนพบหรือหมดรายการ','Best O(1), Average/Worst O(n)','ไม่ต้องเรียงข้อมูล'],['Binary Search','ตรวจค่ากลาง แล้วตัดครึ่งช่วงค้นหาที่เป็นไปไม่ได้ออก','Best O(1), Average/Worst O(log n)','ต้องเรียงข้อมูลก่อน']]
story.append(table(search_rows,[35*mm,70*mm,39*mm,36*mm],small=True))
story += [P('5.1 Sequential Search', 'THH2'), P('เริ่มจากตำแหน่งแรก เปรียบเทียบค่าที่ค้นหากับสมาชิกปัจจุบัน หากตรงกันให้บันทึกผล หากไม่ตรงให้ขยับไปตัวถัดไป วิธีนี้ใช้ได้กับข้อมูลที่ยังไม่เรียง แต่ถ้าข้อมูลอยู่ท้ายรายการหรือไม่พบ จะต้องตรวจหลายรายการ', 'THBody'), P('5.2 Binary Search', 'THH2'), P('กำหนดขอบเขตซ้ายและขวา แล้วคำนวณตำแหน่งกลาง เปรียบเทียบค่ากลางกับค่าที่ต้องการ หากค่าค้นหามากกว่าให้เลื่อนไปครึ่งขวา หากน้อยกว่าให้เลื่อนไปครึ่งซ้าย ทำซ้ำจนพบหรือขอบเขตหมด โปรแกรมจะตรวจสอบก่อนว่าข้อมูลเรียงแล้ว หากยังไม่เรียงจะเสนอให้เรียงด้วย Merge Sort ก่อน', 'THBody'), P('<b>ข้อควรระวัง:</b> ห้ามใช้ Binary Search กับข้อมูลที่ยังไม่เรียง เพราะผลลัพธ์อาจผิด แม้โค้ดจะทำงานโดยไม่มีข้อผิดพลาดก็ตาม', 'THBody'), P('6. โหมด Trace สำหรับการสาธิต', 'THH1'), P('ในเมนูสาธิตการเรียงลำดับ โปรแกรมจะถามว่า “ต้องการแสดงขั้นตอนการทำงานจริง (Trace) หรือไม่?” หากตอบ Y โปรแกรมจะบันทึกและแสดงขั้นตอนสำคัญ เช่น คู่ข้อมูลที่กำลังเปรียบเทียบ การสลับค่า การแทรก การเลือกค่าต่ำสุด และการแบ่ง/ผสานของ Merge Sort ส่วน Search จะแสดงตำแหน่งหรือขอบเขตที่กำลังตรวจสอบ โหมด Trace ถูกแยกจาก Benchmark เพื่อให้สถิติการเปรียบเทียบยังสะท้อนการทำงานของอัลกอริทึมตามปกติ', 'THBody'), PageBreak()]

story += [P('7. วิธีติดตั้งและใช้งาน', 'THH1'), P('โปรเจกต์ใช้ Python Standard Library จึงไม่ต้องติดตั้งไลบรารีภายนอก แนะนำ Python 3.9 ขึ้นไป', 'THBody'), P('คำสั่งเปิดโปรแกรม', 'THH2'), P('cd /home/ryu/mini-project-sorting-searching<br/>python3 main.py', 'THCode'), P('เมนูหลัก', 'THH2')]
menu=[['เมนู','การทำงาน'],['1','แสดงรายชื่อนักเรียนทั้งหมด'],['2','เพิ่มข้อมูลนักเรียนและคำนวณเกรด'],['3','ลบข้อมูลด้วยรหัสนักเรียน'],['4','โหลดชุดข้อมูลตัวอย่าง'],['5','สาธิต Sorting เลือกอัลกอริทึม เกณฑ์ ทิศทาง และ Trace'],['6','สาธิต Searching เลือก Sequential หรือ Binary และฟิลด์ค้นหา'],['7','Benchmark Sorting ทั้ง 4 วิธี'],['8','ล้างข้อมูลทั้งหมด'],['0','ออกจากโปรแกรม']]
story.append(table(menu,[20*mm,160*mm]))
story += [P('ตัวอย่างลำดับการสาธิต Sorting', 'THH2')]
for x in ['เลือกเมนู 5','เลือกอัลกอริทึม เช่น 1 สำหรับ Bubble Sort','เลือกเกณฑ์ เช่น 1 สำหรับคะแนน','เลือกทิศทาง เช่น 1 สำหรับน้อยไปมาก','ตอบ Y เพื่อเปิด Trace','ตอบ N หากไม่ต้องการบันทึกผลการเรียงเป็นลำดับหลัก','อธิบายรายการ Trace แล้วชี้ให้เห็นผลลัพธ์และ Metrics']:
    story.append(B(x))
story += [P('ตัวอย่างลำดับการสาธิต Searching', 'THH2')]
for x in ['เลือกเมนู 6','เลือก Sequential Search หรือ Binary Search','เลือกฟิลด์ เช่น รหัสนักเรียน','กรอกค่าที่ต้องการค้นหา','สำหรับ Binary Search หากข้อมูลยังไม่เรียง ให้ตอบ Y เพื่อให้ระบบเรียงข้อมูลก่อน','อธิบายตำแหน่งที่ตรวจสอบจาก Trace และผลลัพธ์ที่พบ']:
    story.append(B(x))

story += [PageBreak(), P('8. การทดสอบและผลการตรวจสอบ', 'THH1'), P('โปรเจกต์มี Unit Tests ครอบคลุมโมเดลนักเรียน Sorting Searching และ ScoreManager รวมถึงพฤติกรรม Trace ที่เพิ่มเข้ามา ผลการตรวจสอบล่าสุดมีรายละเอียดดังนี้', 'THBody'), P('คำสั่งทดสอบ', 'THH2'), P('python3 -m unittest discover -s tests -v', 'THCode'), P('<b>ผลที่ตรวจสอบจริง:</b> ผ่านทั้งหมด 39 รายการ (OK)', 'THBody'), P('คำสั่งตรวจ Syntax', 'THH2'), P('python3 -m py_compile main.py models/*.py algorithms/*.py services/*.py tests/*.py', 'THCode'), P('<b>ผลที่ตรวจสอบจริง:</b> Exit Code 0 ไม่พบ Syntax Error หรือ Import Error', 'THBody'), P('เกณฑ์ตรวจรับงาน', 'THH2')]
for x in ['อัลกอริทึมทั้ง 6 แบบให้ผลลัพธ์ถูกต้องตามข้อมูล','Trace ถูกปิดเป็นค่าเริ่มต้นของฟังก์ชัน จึงไม่ทำลายการเรียกใช้เดิม','เปิด Trace แล้วมีขั้นตอนที่อธิบายได้และจำกัดความยาว','Binary Search ปฏิเสธหรือจัดการข้อมูลที่ยังไม่เรียงอย่างชัดเจน','Benchmark ไม่ได้รับผลกระทบจาก Trace','ชุดทดสอบอัตโนมัติและการ Compile ผ่าน']:
    story.append(B(x))
story += [P('9. แนวทางแบ่งการนำเสนอ 15 นาที', 'THH1')]
pres=[['เวลา','เนื้อหา','ผู้รับผิดชอบแนะนำ'],['0:00–1:00','แนะนำหัวข้อและสมาชิก','สมาชิก 1'],['1:00–4:00','อธิบาย Sorting 4 แบบและ Big-O','สมาชิก 2–3'],['4:00–6:00','อธิบาย Sequential และ Binary Search','สมาชิก 4'],['6:00–11:00','สาธิตโปรแกรมและ Trace','สมาชิก 5'],['11:00–13:00','อธิบายโครงสร้างโค้ดและ Unit Tests','สมาชิก 6'],['13:00–15:00','สรุป เปรียบเทียบ และตอบคำถาม','ทุกคน']]
story.append(table(pres,[27*mm,95*mm,58*mm],small=True))
story += [PageBreak(), P('10. รายละเอียดเชิงเทคนิค', 'THH1'), P('ส่วนนี้อธิบายการออกแบบภายในเพื่อให้ผู้พัฒนาหรือผู้ตรวจงานสามารถติดตามเส้นทางของข้อมูลตั้งแต่รับเข้าระบบจนถึงแสดงผลได้อย่างเป็นระบบ', 'THBody'), P('10.1 โมเดลข้อมูลและการตรวจสอบ (Data Model & Validation)', 'THH2'), P('ข้อมูลนักเรียนถูกแทนด้วย Student ซึ่งประกอบด้วยรหัสนักเรียน ชื่อ และคะแนน โดยกำหนดเงื่อนไขว่ารหัสและชื่อต้องไม่เป็นค่าว่าง คะแนนต้องอยู่ระหว่าง 0 ถึง 100 และรหัสนักเรียนต้องไม่ซ้ำกันใน ScoreManager เมื่อสร้างหรือเพิ่มข้อมูล ระบบคำนวณเกรดจากคะแนนโดยอัตโนมัติ จึงลดโอกาสที่ข้อมูลคะแนนและเกรดจะไม่สอดคล้องกัน', 'THBody'), P('10.2 การไหลของข้อมูล (Data Flow)', 'THH2'), P('ผู้ใช้เลือกคำสั่งจาก main.py → main.py แปลงคำสั่งเป็นพารามิเตอร์ → ScoreManager ตรวจสอบสถานะและเลือกอัลกอริทึม → algorithms/sorting.py หรือ algorithms/searching.py ประมวลผล → ส่งผลลัพธ์ Metrics และ Trace กลับมา → main.py แสดงตาราง ผลการค้นหา และสถิติบนหน้าจอ', 'THBody'), P('10.3 Pseudocode ของขั้นตอนสำคัญ', 'THH2'), P('Bubble Sort:<br/>1) ทำซ้ำจากรอบแรกถึงรอบสุดท้าย<br/>2) เปรียบเทียบสมาชิกคู่ติดกันในช่วงที่ยังไม่เรียง<br/>3) สลับเมื่ออยู่ผิดลำดับ<br/>4) หากไม่มีการสลับ ให้หยุดก่อนกำหนด<br/><br/>Binary Search:<br/>1) กำหนด left = 0 และ right = n - 1<br/>2) คำนวณ mid จากช่วงปัจจุบัน<br/>3) ถ้าค่ากลางตรงกับคำค้น ให้คืนผลลัพธ์<br/>4) ถ้าคำค้นมากกว่า ให้เลื่อน left ไปทางขวา มิฉะนั้นเลื่อน right ไปทางซ้าย<br/>5) ทำซ้ำจน left มากกว่า right', 'THCode'), P('10.4 ความถูกต้องและ Invariant', 'THH2'), P('Bubble/Insertion/Selection Sort ต้องรักษาเงื่อนไขว่าส่วนหน้าที่ผ่านการประมวลผลแล้วอยู่ในลำดับที่ถูกต้อง ส่วน Merge Sort ต้องคืนผลจากการผสานสองลิสต์ย่อยที่เรียงแล้วให้เป็นลิสต์ที่เรียงแล้ว สำหรับ Binary Search เงื่อนไขสำคัญคือช่วง [left, right] ต้องครอบคลุมคำตอบที่ยังเป็นไปได้ และข้อมูลต้องเรียงตาม key ก่อนเริ่มค้นหา', 'THBody'), P('10.5 การเก็บ Metrics และ Trace', 'THH2'), P('SortMetrics และ SearchMetrics แยกจำนวน Comparisons จำนวน Swaps/Shifts/Merges ตำแหน่งที่พบ และเวลาประมวลผล โดยใช้ time.perf_counter() สำหรับจับเวลา Trace ถูกเปิดด้วยพารามิเตอร์ trace=True และมี max_trace_lines เพื่อควบคุมขนาดผลลัพธ์ เมื่อ trace=False ค่า Trace จะว่างและการทำ Benchmark ไม่ถูกปนด้วยข้อความสาธิต', 'THBody'), P('10.6 การจัดการข้อผิดพลาดและกรณีขอบ (Error & Edge Cases)', 'THH2'), P('ระบบรองรับลิสต์ว่าง ข้อมูลหนึ่งรายการ ข้อมูลซ้ำ ข้อมูลเรียงแล้ว ข้อมูลเรียงย้อนกลับ ค้นหาไม่พบ รหัสซ้ำ คะแนนนอกช่วง และ Binary Search กับข้อมูลไม่เรียง โดยแจ้งข้อผิดพลาดหรือให้ผู้ใช้ยืนยันการเรียงข้อมูลก่อนดำเนินการต่อ', 'THBody'), P('10.7 ความปลอดภัยและการดูแลโค้ด', 'THH2'), P('โปรเจกต์ไม่มีการฝังรหัสผ่านหรือ API key ใช้ข้อมูลในหน่วยความจำและไม่เชื่อมต่อฐานข้อมูลภายนอก อินพุตสำคัญถูกตรวจสอบก่อนสร้าง Student คำสั่งทดสอบใช้ Standard Library และไฟล์ที่สร้างจากการรัน เช่น __pycache__ ไม่ควรถูก commit ตาม .gitignore', 'THBody'), P('10.8 แนวทางต่อยอดทางเทคนิค', 'THH2'), P('สามารถต่อยอดเป็น GUI หรือเว็บแอป เพิ่มการนำเข้า/ส่งออก CSV เพิ่มการวัดผลกับข้อมูลหลายขนาด ทำกราฟเปรียบเทียบเวลา เพิ่ม property-based testing และเพิ่มการบันทึกผลการทดลองเป็นไฟล์ เพื่อวิเคราะห์ผลกระทบของจำนวนข้อมูลต่อ Big-O ได้ชัดเจนขึ้น', 'THBody'), P('11. สรุป', 'THH1'), P('โปรแกรมนี้เชื่อมโยงทฤษฎีกับการทำงานจริง โดยใช้ระบบคะแนนนักเรียนเป็นบริบทที่เข้าใจง่าย ผู้ชมสามารถเห็นทั้งผลลัพธ์สุดท้าย สถิติการทำงาน และลำดับขั้นตอนผ่าน Trace จุดสำคัญในการนำเสนอคืออธิบายว่าแต่ละอัลกอริทึมเลือกตรวจหรือจัดข้อมูลอย่างไร เหตุใด Binary Search จึงต้องใช้ข้อมูลที่เรียงแล้ว และ Merge Sort จึงมีความซับซ้อนดีกว่าอัลกอริทึมแบบ O(n²) เมื่อข้อมูลมีจำนวนมาก', 'THBody'), Spacer(1, 8*mm), P('<b>ไฟล์โปรแกรม:</b> mini-project-sorting-searching.zip<br/><b>โฟลเดอร์โปรเจกต์:</b> /home/ryu/mini-project-sorting-searching', 'THBody')]

doc = SimpleDocTemplate(OUT, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=17*mm, title='เอกสารประกอบมินิโปรเจกต์ Sorting และ Searching', author='กลุ่ม Mini Project')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
