from datetime import datetime, timedelta

def prioritize_tasks(tasks):
    for task in tasks:
        task['score'] = (task['priority'] * 0.6) + (1 / (datetime.strptime(task['deadline'], '%Y-%m-%d') - datetime.now()).days * 0.4)
    return sorted(tasks, key=lambda x: x['score'], reverse=True)

def find_free_slots(calendar_events):
    free_slots = []
    now = datetime.now()
    for event in calendar_events:
        end_time = datetime.fromisoformat(event['end']['dateTime'])
        free_slots.append({'start': end_time, 'duration': 60})  # Dummy free slot example
    return free_slots

def schedule_tasks(tasks, calendar_events):
    free_slots = find_free_slots(calendar_events)
    scheduled_tasks = []
    for task in tasks:
        for slot in free_slots:
            if slot['duration'] >= task['duration']:
                scheduled_tasks.append({
                    'task': task['name'],
                    'start': slot['start'],
                    'end': slot['start'] + timedelta(minutes=task['duration']),
                })
                break
    return scheduled_tasks

def fetch_calendar_events():
    # Placeholder for Google Calendar API integration
    # Return mock data for testing
    return [
        {'start': {'dateTime': '2024-11-30T09:00:00'}, 'end': {'dateTime': '2024-11-30T10:00:00'}}
    ]
