from datetime import datetime

from util.google_calendar.api_util import *

def config_recurrence() -> str:
    # found in https://datatracker.ietf.org/doc/html/rfc5545#section-3.8.5.3
    pass

def create_event(cal_id: str, title: str, start_dt: datetime, end_dt: datetime, location: str = None, desc: str = None, recurrence: list = None, emails: list = None, colour: str = None,) -> dict:
    service = get_service()

    info = {
        "summary": title,
        "start" : {
            "dateTime": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "Asia/Singapore",
        },

        "end" : {
            "dateTime": end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "Asia/Singapore",
        },
    }
    
    if location:
        info["location"] = location
    
    if desc:
        info["description"] = desc
    
    if recurrence:
        info["recurrence"] = recurrence
    
    if emails:
        info["attendees"] = [{"email": e} for e in emails]

    if colour:
        info["colorId"] = colour

    event = service.events().insert(calendarId=cal_id, body=info).execute()

    return event