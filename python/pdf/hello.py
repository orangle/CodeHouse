# coding:utf-8
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

pdfmetrics.registerFont(TTFont('song', 'STSONG.TTF'))
ParagraphStyle.defaults['wordWrap']="CJK"

c = canvas.Canvas("hello.pdf", pagesize=letter)
c.setFont('song', 16)
c.drawString(0, 0, "hello world! 你好"*20)


styleSheet = getSampleStyleSheet()
style = styleSheet['BodyText']
style.fontName = 'song'
style.fontSize = 16
#设置行距
style.leading = 20
#首行缩进
style.firstLineIndent = 32
pa = Paragraph(u'<b>这里是粗体</b>，<i>这里是斜体</i>, <strike>这是删除线</strike>, <u>这是下划线</u>, <sup>这是上标</sup>, <em>这里是强调</em>, <font color=#ff0000>这是红色</font>', style)
pa.wrapOn(c, 6*inch, 8*inch)
pa.drawOn(c, 0, 5*inch)
c.showPage()
c.save()