from pathlib import Path
import re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import fitz

root=Path('/caso')
out=root/'output/pdf'
out.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DejaVu',font+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold',font+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body',fontName='DejaVu',fontSize=9.5,leading=14,spaceAfter=7,textColor=colors.black))
styles.add(ParagraphStyle(name='H1x',fontName='DejaVu-Bold',fontSize=16,leading=21,spaceBefore=10,spaceAfter=13,keepWithNext=True))
styles.add(ParagraphStyle(name='H2x',fontName='DejaVu-Bold',fontSize=11.5,leading=16,spaceBefore=12,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='Cover',fontName='DejaVu-Bold',fontSize=23,leading=31,alignment=TA_CENTER,spaceAfter=24))
styles.add(ParagraphStyle(name='Center',parent=styles['Body'],alignment=TA_CENTER,fontSize=11,leading=18,spaceAfter=16))
def fmt(s):
    s=html.escape(s.replace('`',''))
    s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'\1 (\2)',s)
    return s
story=[]
lines=(root/'PLAN.md').read_text(encoding='utf-8').splitlines()
split=next(i for i,l in enumerate(lines) if l.startswith('## 1.'))
story += [Spacer(1,45),Paragraph('UNIVERSIDAD PRIVADA DE TACNA',styles['Center']),Paragraph('Facultad de Ingeniería<br/>Escuela de Ingeniería de Sistemas',styles['Center']),Spacer(1,30),Paragraph('Plan de auditoría de seguridad del canal digital',styles['Cover']),Paragraph('Clínica Santa Lucía S.A.C.',styles['Center']),Paragraph('SI-084 · Auditoría de Sistemas<br/>Examen práctico de Unidad II',styles['Center']),Spacer(1,22)]
for line in lines[:split]:
    if line.startswith('|'):
        cells=[c.strip() for c in line.strip('|').split('|')]
        if cells[0] in ('Carátula','---'):continue
        story.append(Paragraph('<b>'+fmt(cells[0])+':</b> '+fmt(cells[1]),styles['Body']))
story += [Spacer(1,20),Paragraph('Tacna, Perú · 2026',styles['Center']),Paragraph('CONFIDENCIAL · USO ACADÉMICO',styles['Center']),PageBreak()]
i=split
while i<len(lines):
    line=lines[i].strip()
    if not line:i+=1;continue
    if line.startswith('## '):
        if line.startswith(('## 3.','## 4.','## 6.','## 7.')):
            story.append(PageBreak())
        story.append(Paragraph(fmt(line[3:]),styles['H1x']))
    elif line.startswith('### '):
        if line.startswith('### P-') and not line.startswith('### P-01'):story.append(PageBreak())
        story.append(Paragraph(fmt(line[4:]),styles['H2x']))
    elif line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.match(r'^:?-+:?$',c) for c in cells):rows.append(cells)
            i+=1
        header=rows[0]
        for row in rows[1:]:
            if len(header)==2:
                story.append(Paragraph('<b>'+fmt(row[0])+'.</b> '+fmt(row[1]),styles['Body']))
            else:
                content=' '.join('<b>'+fmt(header[n])+':</b> '+fmt(cell) for n,cell in enumerate(row))
                story.append(Paragraph(content,styles['Body']))
                story.append(Spacer(1,8))
        continue
    else:story.append(Paragraph(fmt(line.removeprefix('- ')),styles['Body']))
    i+=1
pdf=out/'SI084-EXPRAC-U2-ChireRamosMayraFernanda.pdf'
def footer(canvas,doc):
    canvas.setFont('DejaVu',8)
    canvas.setFillColor(colors.HexColor('#555555'))
    canvas.drawString(45,25,'SI-084 · Chire Ramos, Mayra Fernanda · 2021072620')
    canvas.drawRightString(550,25,str(doc.page))
doc=SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),rightMargin=45,leftMargin=45,topMargin=43,bottomMargin=45,title='Plan de auditoría del canal digital de Clínica Santa Lucía',author='Chire Ramos, Mayra Fernanda')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
qa=root/'tmp/pdfs';qa.mkdir(parents=True,exist_ok=True)
d=fitz.open(pdf)
for n,p in enumerate(d):
    p.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(qa/f'pagina-{n+1:02}.png')
    for block in p.get_text('blocks'):
        if block[1]<0 or block[3]>842 or block[0]<0 or block[2]>596:raise ValueError(f'Texto fuera de página {n+1}')
print(f'PDF generado: {pdf.name}; {len(d)} páginas; límites de texto correctos')
