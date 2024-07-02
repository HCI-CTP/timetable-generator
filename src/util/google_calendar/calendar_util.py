from util.google_calendar.api_util import *

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
    service = get_service()

    cal = service.calendarList().get(calendarId=cal_id).execute()

    return cal

def list_calendar() -> None:
    service = get_service()

    cal_lst = service.calendarList().list().execute()

    return cal_lst

def update_calendar(cal_id: str, body: dict) -> dict:
    service = get_service()

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

if __name__ == "__main__":
    service = get_service()