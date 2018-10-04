from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


'''
Client secret = kK5MrgIPk5GLluvDZS4E7HYM
Client ID = 130335195609-r8e5aguvg3sr2a1d0e2oap6bjrn3aoml.apps.googleusercontent.com
'''

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        # print(event)
        summary = event['summary']
        start = fix_event_time(event['start']['dateTime'])
        end = fix_event_time(event['end']['dateTime'])
        dict = {'summary':summary, 'start':start, 'end':end}
        print(dict)
        # self.events.append(dict)
        # print(event)

def fix_event_time(str):
    sub1 = str[0:10]
    sub2 = str[11:16]
    return sub1 + ' ' + sub2
        # start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start, event['summary'])

if __name__ == '__main__':
    main()
