from models import WorkTime, Milestone, Base, engine, session
from models import TIMELORD_INSTALL_DIRECTORY

from sqlalchemy.sql import func
from termcolor import colored

import time
import datetime
import os
import sys


def initialize():
    os.makedirs(TIMELORD_INSTALL_DIRECTORY)
    Base.metadata.create_all(engine) 


def terminal_visual():
    print_line_count = 0
    print colored('TIMELORD v.0.0.1', 'white', attrs=['bold'])
    print_line_count += 1

    # work
    todays_work = session.query(func.sum(WorkTime.work)).filter(WorkTime.datetime >= datetime.date.today()).one()
    if todays_work:
        todays_work = todays_work[0]
    if not todays_work:
        todays_work = 0

    print colored('work: ', 'cyan') + \
            colored(str(todays_work / 60.), 'green') + \
            colored(' hrs', 'cyan')
    print_line_count += 1

    # tasks
    print colored('task progress:', 'cyan')
    print_line_count += 1
    todays_progress = session.query(Milestone).filter(Milestone.datetime >= datetime.date.today()).all()
    if todays_progress:
        for tp in todays_progress:
            print colored('    ' + str(tp), 'yellow')
            print_line_count += 1
    else:
        print colored('    none', 'red')
        print_line_count += 1

    for i in range(print_line_count):
        print '\033[1A' + '\r',
        sys.stdout.flush()


def monitor(terminal_vis=True):
    if not os.path.exists(TIMELORD_INSTALL_DIRECTORY):
        initialize()
    mark = datetime.datetime.now()
    if terminal_vis:
        terminal_visual()
    while True:
        now = datetime.datetime.now()
        if (now - mark).total_seconds() >= 60:
            mark = now
            wt = WorkTime()
            session.add(wt)
            session.commit()
            if terminal_vis:
                terminal_visual()


if __name__ == '__main__':
    monitor()
