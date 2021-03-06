import datetime
import os

import gantt
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from .models import Project, Task

from bot_trainer.settings import TMP_PATH


def generate_diagram(project):
    gantt.define_font_attributes(fill='black',
                                 stroke='black',
                                 stroke_width=0,
                                 font_family="Verdana", )

    gantt.define_not_worked_days([])

    main_project = gantt.Project(name=project.title)

    gantt_performers = []
    gantt_tasks = []

    # taskdb = TaskDB(project=project)
    # tasks = taskdb.get_all_tasks()
    # tasks = Task.objects.filter(project=project)
    for performer in project.performers.all():
        if performer.tasks.all():
            gantt_performer = gantt.Project(name=performer.name)
            gantt_performers.append(gantt_performer)
            for task in performer.tasks.all():
                gantt_task = gantt.Task(
                    name=task.title,
                    start=task.date_start,
                    duration=task.duration
                )
                gantt_performer.add_task(gantt_task)


    # for task in tasks:
    #     gantt_task = gantt.Task(
    #         name=task.title,
    #         start=task.date_start,
    #         duration=task.duration
    #     )
    #     if task.performers.all():
    #         for performer in task.performers.all():
    #             gantt_performer = gantt.Project(name=performer.name)
    #             gantt_performer.add_task(gantt_task)
    #             gantt_performers.append(gantt_performer)
    #     else:
    #         gantt_tasks.append(gantt_task)

    [main_project.add_task(task) for task in gantt_tasks]
    [main_project.add_task(task) for task in gantt_performers]

    today_time = datetime.datetime.now()
    today_date = datetime.date(today_time.year, today_time.month, today_time.day)

    main_project.make_svg_for_tasks(filename=os.path.join(TMP_PATH, str(project.user) + '.svg'),
                                    today=today_date,
                                    start=project.date_start,
                                    end=project.date_end)

    with open(os.path.join(TMP_PATH, str(project.user) + '.svg'), 'r') as f:
        svg_string = f.read()

    svg_string = svg_string.replace('lightgray', '#D3D3D3').replace('gray', '#808080').replace('#0000FF ', '#C2C5CC')

    with open(os.path.join(TMP_PATH, str(project.user) + '.svg'), 'w') as f:
        f.write(svg_string)

    drawing = svg2rlg(os.path.join(TMP_PATH, str(project.user) + '.svg'))
    renderPM.drawToFile(drawing, os.path.join(TMP_PATH, str(project.user) + '.jpg'), fmt="jpg")

    os.remove(os.path.join(TMP_PATH, str(project.user) + '.svg'))

    return os.path.join(TMP_PATH, str(project.user) + '.jpg')


"""
from bot.models import Project
pr = Project.objects.all()[0]
from bot.build_diagram import generate_diagram
generate_diagram(pr)
"""
