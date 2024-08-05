import os
import json

import asyncio

from urllib.parse import urlencode
from playwright.async_api import async_playwright

from datetime import datetime

from util.isp.isp_util import get_cookies

cal_url = "https://isphs.hci.edu.sg/eventcalendar.asp"

async def get_playwright(url):
    cookies = await get_cookies()

    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context()

    await context.add_cookies(cookies=cookies)

    page = await context.new_page()
    await page.goto(url=url)

    await page.wait_for_load_state("domcontentloaded")

    return p, browser, context, page

async def get_event_calendar(year: int, month: int) -> list:
    if month not in range(1, 13):
        raise ValueError(f"Invalid Month provided : {month}")

    year = str(year)
    month = str(month)
    
    params = {
        "year": year,
        "month": month,
    }

    p, browser, context, page = await get_playwright(url=cal_url + "?" + urlencode(params))

    await page.wait_for_selector("#calendar > div")

    table = page.locator("#calendar > div > div > div")
    events = await table.locator("div").all()

    events_lst = []

    for e in events:
        await e.hover()

        table = page.locator("#calendar > div > div > div")

        info = table.locator("div").last
        values = (await info.inner_text()).splitlines()

        values.pop(1)
        
        keys = ["title", "start_dt", "end_dt", "in_charge", "venue", "details"]
        values = [i.split(": ")[-1] if i[-1:] != ":" else None for i in values]

        dt = values[1]
        
        if "From" in dt:
            dt = dt.split("From ")[-1]
            start_dt, end_dt = [datetime.strptime(d, "%d %b %Y %H:%M") for d in dt.split(" To ")]
        else:
            date = dt.split()[:3]
            date = " ".join(date)
            
            start_dt = end_dt = datetime.strptime(date, "%d %b %Y")
            end_dt = datetime(year=end_dt.year, month=end_dt.month, day=end_dt.day, hour=23, minute=59, second=59)

        values.pop(1)
        values.insert(1, end_dt)
        values.insert(1, start_dt)

        event_details = dict(zip(keys, values))

        events_lst.append(event_details)

    await context.close()
    await browser.close()
    await p.stop()

    return events_lst

async def main():
    print(await get_event_calendar(2024, 6))

if __name__ == "__main__":
    asyncio.run(main())