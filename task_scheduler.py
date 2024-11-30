from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def prioritize_tasks(tasks):
    for task in tasks:
        days_until_deadline = max((datetime.strptime(task['deadline'], '%Y-%m-%d') - datetime.now()).days, 1)
        task['score'] = task['priority'] * 0.7 + (1 / days_until_deadline) * 0.3
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
                start_time = slot['start']
                end_time = start_time + timedelta(minutes=task['duration'])
                scheduled_tasks.append({
                    'task': task['name'],
                    'start': start_time.strftime('%Y-%m-%d %H:%M'),
                    'end': end_time.strftime('%Y-%m-%d %H:%M')
                })
                free_slots.remove(slot)  # Use this slot
                break
    return scheduled_tasks


def fetch_calendar_events():
    """Fetches events from Google Calendar."""
    creds = None

    # Use token.json for credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        # If token.json doesn't exist, initiate authentication flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Save the credentials to token.json for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Connect to the Google Calendar API
    service = build('calendar', 'v3', credentials=creds)

    # Fetch upcoming events
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Format the events
    calendar_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        summary = event.get('summary', 'No Title')
        calendar_events.append({'summary': summary, 'start': start, 'end': end})

    return calendar_events
    