import asyncio

from datetime import datetime

import re
import random

from util.google_calendar.acl_util import *
from util.google_calendar.calendar_util import *
from util.google_calendar.event_util import *
from util.google_calendar.colour_util import *

from util.isp.acad_calendar_util import get_acad_calendar
from util.isp.event_calendar_util import get_event_calendar

from util.db_util import *

from tqdm import tqdm

db_data = fetch_data(_class="4A3")

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

colour_lst = list_event_colour()

all_subj_lst = get_subjects(data=odd_data+even_data)
all_subj_lst = sorted(all_subj_lst, key=len)

non_subj_lst = ["ACAD CONS", "PACE"]
subj_lst = [s for s in all_subj_lst if ("".join(re.findall("[A-Za-z]", s)).isupper() or "HBL" in s) and s not in non_subj_lst]
break_lst = ["Recess", "Lunch"]
non_subj_lst = [s for s in all_subj_lst if s not in subj_lst]

clear_calendar_list()
odd_cal = create_calendar(title="4A3 T2 (Odd)", desc="test")
# even_cal = create_calendar(title="4A3 T2 (Even)", desc="test")

odd_acl = insert_acl(cal_id=odd_cal["id"], scope="user", email="chongchoonhourafael@gmail.com", role="owner")
# even_acl = insert_acl(cal_id=even_cal["id"], scope="user", email="chongchoonhourafael@gmail.com", role="owner")

subj_colour = "10"

for idx, d in enumerate(tqdm(odd_data)):
    if d["title"] in subj_lst:
        colour = "9" if subj_colour == "10" else "10"
        subj_colour = "10" if colour == "10" else "9"
    elif d["title"] in break_lst:
        colour = "2"
    else:
        colour = "1"    

    event = create_event(cal_id=odd_cal["id"], title=d["title"], start_dt=d["start"], end_dt=d["end"], colour=colour)

# for d in tqdm(even_data):
#     event = create_event(cal_id=even_cal["id"], title=d["title"], start_dt=d["start"], end_dt=d["end"], colour=subj_to_colour[d["title"]])