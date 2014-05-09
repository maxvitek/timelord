from models import Milestone, session, TIMELORD_INSTALL_DIRECTORY

from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.colors import red, black, navy, white, green

import getpass
import datetime
import os

(PAGE_WIDTH, PAGE_HEIGHT) = defaultPageSize


def get_monday():
    today = datetime.date.today().toordinal()
    last_week = today - 7
    sunday = last_week - (last_week % 7)
    monday = sunday + 1
    monday_date = datetime.date.fromordinal(monday)
    return monday_date


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(navy)
    canvas.setLineWidth(5)
    canvas.line(66,72,66,PAGE_HEIGHT-72)
    canvas.setFont('Times-Bold',24)
    canvas.drawString(66, PAGE_HEIGHT-54, getpass.getuser() + '/' + \
            str(get_monday()))
    canvas.setFont('Times-Roman',12)
    canvas.drawString(4 * inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(red)
    canvas.setLineWidth(5)
    canvas.line(66,72,66,PAGE_HEIGHT-72)
    canvas.setFont('Times-Roman',12)
    canvas.drawString(4 * inch, 0.75 * inch, "Page %d" % doc.page)
    canvas.restoreState()


def report():
    story = []

    styNormal = ParagraphStyle('normal')

    milestones = session.query(Milestone).filter(Milestone.datetime >= get_monday()).all()
    for ms in milestones:
        story.append(Paragraph("<para><bullet bulletIndent='-1cm'>&rarr" + \
                "</bullet><b>%s</b> <br/>%s</para>" % (str(ms), ms.milestone), styNormal))

    template = SimpleDocTemplate(os.path.join(TIMELORD_INSTALL_DIRECTORY, 'status.pdf'),
            showBoundary=1)

    template.build(story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
