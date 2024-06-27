import asyncio

from urllib.parse import urlencode
from playwright.async_api import async_playwright

from datetime import datetime

import os
import json

cal_url = "https://isphs.hci.edu.sg/eventcalendar.asp"

async def get_cookies():
    cookies = None
    cookie_data = None
    
    cond = True

    if os.path.exists("./secrets/isphs-cookies.json"):
        with open("./secrets/isphs-cookies.json", "r") as f:
            cookie_data = f.read()

    if cookie_data:
        cookie_data = json.loads(cookie_data)

        dt = datetime.strptime(cookie_data["dt"], "%d/%m/%Y %H:%M:%S")
        td = datetime.now() - dt
        td = td.total_seconds()

        # i.e. less than 10 min
        if td < 600:
            cond = False
            cookies = cookie_data["cookies"]

    if cond:
        with open("./secrets/isphs-auth.json", "r") as f:
            auth = f.read()

        auth = json.loads(auth)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()

            page = await context.new_page()
            await page.goto(url="https://isphs.hci.edu.sg/")
            await page.wait_for_load_state("domcontentloaded")

            user_input, pw_input, submit = await page.locator(".form").locator("input").all()
            
            await user_input.fill(auth["username"])
            await pw_input.fill(auth["password"])
            await submit.click()

            await page.wait_for_load_state("domcontentloaded")

            cookies = await context.cookies()

            with open("./secrets/isphs-cookies.json", "w+") as f:
                cookie_data = json.dumps({
                    "cookies": cookies,
                    "dt": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })

                f.write(cookie_data)

            await context.close()
            await browser.close()
    
    return cookies   

async def get_playwright(url):
    cookies = await get_cookies()

    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()

    await context.add_cookies(cookies=cookies)

    page = await context.new_page()
    await page.goto(url=url)

    await page.wait_for_load_state("domcontentloaded")

    return p, browser, context, page

async def get_event_calendar(year: int, month: int) -> dict:
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