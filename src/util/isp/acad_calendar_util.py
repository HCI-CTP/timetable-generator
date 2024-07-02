import asyncio

from urllib.parse import urlencode
import requests

from bs4 import BeautifulSoup

from datetime import datetime

import json

cal_url = "https://isphs.hci.edu.sg/curriculum/acadcalendar.asp"

from util.isp.isp_util import get_cookies

def get_soup(url):
    cookie_data = asyncio.run(get_cookies())

    cookies = {d["name"]: d["value"] for d in cookie_data}

    r = requests.get(
        url=url,
        cookies=cookies,
    )

    content = r.text
    soup = BeautifulSoup(content, features="html.parser")

    return soup

def get_options():
    soup = get_soup(url=cal_url)

    year = soup.find("select", attrs={"name": "year"})
    year_options = [*year.find_all("option")]
    year_options = {e.get_text(): e.attrs["value"] for e in year_options}

    year_to_term_options = {}

    for year, value in year_options.items():
        params = {
            "year": value,
        }

        soup = get_soup(url=cal_url + "?" + urlencode(params))

        term = soup.find("select", attrs={"name": "Term"})
        term_options = [*term.find_all("option")]
        term_options = term_options[1:]
        term_options = {e.get_text(): e.attrs["value"] for e in term_options}

        year_to_term_options[value] = term_options

    return year_options, year_to_term_options

def get_acad_calendar(year: int, term: int) -> dict:
    year_options, year_to_term_options = get_options()

    if term not in range(1, 5):
        raise ValueError(f"Invalid Term provided : {term}")

    year = str(year)
    term = str(term)

    if year not in year_options.values():
        raise ValueError(f"Invalid Year provided : {year}")
    
    term_options = year_to_term_options[year]
    
    params = {
        "year": year,
        "term": term_options[f"Term {term}"],
    }

    soup = get_soup(url=cal_url + "?" + urlencode(params))

    table = soup.find("tr", attrs={"class": "t"}).parent
    rows = [*table.find_all("tr")]
    rows = rows[1:]
    
    week_to_date = {}

    for row in rows:
        data = row.find_all("td")
        week, start_d, end_d, hol = [d.get_text() for d in data]

        start_d = start_d.split()[0]
        end_d = end_d.split()[0]

        start_d = datetime.strptime(start_d, "%d/%m/%Y")
        end_d = datetime.strptime(end_d, "%d/%m/%Y")

        week_to_date[week] = (start_d, end_d)

    return week_to_date

if __name__ == "__main__":
    print(get_acad_calendar(2024, 3))