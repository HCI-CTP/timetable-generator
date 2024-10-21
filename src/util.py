import asyncio

from datetime import timedelta

import re

from util.google_calendar.acl_util import *
from util.google_calendar.calendar_util import *
from util.google_calendar.event_util import *
from util.google_calendar.colour_util import *

from util.isp.acad_calendar_util import get_acad_calendar
from util.isp.event_calendar_util import get_event_calendar

from util.db.db_util import *

from tqdm import tqdm

def save_timetable(_class: str, email: str):
    db_data = fetch_data(_class=_class)

    even_data = [d for d in db_data if "Even" in d[0]]
    odd_data = [d for d in db_data if d not in even_data] # includes HBL (which does not have "odd")

    acad_data = get_acad_calendar(year=2024, term=2)
    acad_data = acad_data.items()

    odd_dates, even_dates = list(acad_data)[:2]
    odd_week, (odd_start, odd_end) = odd_dates
    even_week, (even_start, even_end) = even_dates

    odd_data = format_data(data=odd_data, start_dt=odd_start)
    even_data = format_data(data=even_data, start_dt=even_start)

    odd_data = clump_data(data=odd_data)
    even_data = clump_data(data=even_data)

    all_subj_lst = get_subjects(data=odd_data+even_data)
    all_subj_lst = sorted(all_subj_lst, key=len)

    non_subj_lst = ["ACAD CONS", "PACE"]
    subj_lst = [s for s in all_subj_lst if ("".join(re.findall("[A-Za-z]", s)).isupper() or "HBL" in s) and s not in non_subj_lst]
    break_lst = ["Recess", "Lunch"]
    non_subj_lst = [s for s in all_subj_lst if s not in subj_lst]

    odd_cal = create_calendar(title="2024 4A3 T2 (Odd)")
    even_cal = create_calendar(title="2024 4A3 T2 (Even)")

    odd_acl = insert_acl(cal_id=odd_cal["id"], scope="user", email=email, role="owner")
    even_acl = insert_acl(cal_id=even_cal["id"], scope="user", email=email, role="owner")

    for d in tqdm(odd_data):
        if d["title"] in subj_lst:
            colour = "9"
        elif d["title"] in break_lst:
            colour = "10"
        else:
            colour = "3"

        event = create_event(cal_id=odd_cal["id"], title=d["title"], start_dt=d["start"], end_dt=d["end"], colour=colour, recurrence=["RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=5"])

    for d in tqdm(even_data):
        if d["title"] in subj_lst:
            colour = "9"
        elif d["title"] in break_lst:
            colour = "1"
        else:
            colour = "8"

        event = create_event(cal_id=even_cal["id"], title=d["title"], start_dt=d["start"], end_dt=d["end"], colour=colour, recurrence=["RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=5"])

    return odd_cal, even_cal

def save_weeks(email: str):
    acad_data = get_acad_calendar(year=2024, term=2)
    acad_data = acad_data.items()

    week_cal = create_calendar(title="2024 T2 Week Calendar")
    week_acl = insert_acl(cal_id=week_cal["id"], scope="user", email=email, role="owner")

    for d in tqdm(acad_data):
        week, (start, end) = d
        
        end += timedelta(hours=23, minutes=59)

        event = create_event(cal_id=week_cal["id"], title=week, start_dt=start, end_dt=end)

def save_events(email: str):
    events_lst = []

    for m in tqdm(range(1, 13)):
        events_lst += asyncio.run(get_event_calendar(year=2024, month=m)) 

    events_cal = create_calendar(title="2024 HCI Events Calendar")
    events_acl = insert_acl(cal_id=events_cal["id"], scope="user", email=email, role="owner")

    for e in tqdm(events_lst):
        desc = f"""In Charge : {e["in_charge"]}
Venue : {e["venue"]}
Details : {e["details"]}
"""
        create_event(cal_id=events_cal["id"], title=e["title"], start_dt=e["start_dt"], end_dt=e["end_dt"], desc=desc)

if __name__ == "__main__":
    clear_calendar_list()
    # save_timetable(_class="4A3", email="chongchoonhourafael@gmail.com")
    # save_weeks(email="chongchoonhourafael@gmail.com")
    save_events(email="chongchoonhourafael@gmail.com")
    