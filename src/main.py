import asyncio

from util.google_calendar.calendar_util import *

from util.isp.acad_calendar_util import get_acad_calendar
from util.isp.event_calendar_util import get_event_calendar

from util.db_util import fetch_data

print(fetch_data(_class="4A3", week="Even"))
print(get_acad_calendar(term=3, year=2024))
print(asyncio.run(get_event_calendar(month=1, year=2024)))