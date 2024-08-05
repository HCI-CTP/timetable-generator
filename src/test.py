import json

from util.google_calendar.api_util import *
from util.google_calendar.acl_util import *
from util.google_calendar.calendar_util import *

from util.isp.acad_calendar_util import *
from util.isp.event_calendar_util import *

from util.db.db_util import *

# api tests

# acl tests

# calendar tests

# event tests

# db tests

odd_cal = list_calendar()["items"][0]
odd_events = list_calendar_events(cal_id=odd_cal["id"])

print(odd_events[0])