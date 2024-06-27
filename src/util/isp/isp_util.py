import os
import json

from datetime import datetime

from playwright.async_api import async_playwright

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