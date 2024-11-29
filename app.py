from flask import Flask, render_template, request, redirect, url_for
from task_scheduler import prioritize_tasks, schedule_tasks, fetch_calendar_events

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = {
        'name': request.form['task'],
        'deadline': request.form['deadline'],
        'priority': int(request.form['priority']),
        'duration': int(request.form['duration']),
    }
    tasks.append(task)
    return redirect(url_for('index'))

@app.route('/schedule')
def schedule():
    calendar_events = fetch_calendar_events()
    prioritized_tasks = prioritize_tasks(tasks)
    scheduled_tasks = schedule_tasks(prioritized_tasks, calendar_events)
    return render_template('schedule.html', scheduled_tasks=scheduled_tasks)

if __name__ == '__main__':
    app.run(debug=True)
