from api_util import *

import datetime

def create_calendar(title: str, desc: str = None) -> dict:
    service = get_service()

    info = {
        "summary": title,
        "description": desc,
        "timeZone": "Asia/Singapore",
    }

    calendar = service.calendars().insert(body=info).execute()

    return calendar

def get_calendar(cal_id: str) -> dict:
    cal = service.calendarList().get(calendarId=cal_id).execute()

    return cal

def list_calendar() -> None:
    cal_lst = service.calendarList().list().execute()

    return cal_lst

def update_calendar(cal_id: str, body: dict) -> dict:
    cal = service.calendarList().update(
        calendarId=cal_id, 
        body=body
    ).execute()

    return cal

def delete_calendar(cal_id: str) -> None:
    service = get_service()
    service.calendarList().delete(calendarId=cal_id).execute()

def clear_calendar() -> None:
    cal_lst = list_calendar()

    for cal in cal_lst["items"]:
        cal_id = cal["id"]
        delete_calendar(cal_id=cal_id)

def config_recurrence() -> str:
    # found in https://datatracker.ietf.org/doc/html/rfc5545#section-3.8.5.3
    pass

def create_event(cal_id: str, title: str, start_dt: datetime, end_dt: datetime, location: str = None, desc: str = None, recurrence: list = None, emails: list = None,) -> dict:
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

    event = service.events().insert(calendarId=cal_id, body=info).execute()

    return event

if __name__ == "__main__":
    service = get_service()