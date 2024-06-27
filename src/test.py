from util.google_calendar.api_util import *
from util.google_calendar.calendar_util import *
from util.isp.acad_calendar_util import *
from util.isp.event_calendar_util import *
from util.db_util import *

# api tests
print("Retrieving OAuth2.0 Credentials", end="...")
creds = get_oauth2_creds()
print(creds)
print("Done\n")

print("Starting API Service", end="...")
service = get_service()
print(service)
print("Done\n")

# calendar tests

# event tests

# db tests