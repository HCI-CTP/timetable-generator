import os
import sqlite3

import json

from datetime import datetime, time, timedelta

from typing import Literal

from tqdm import tqdm

data_files = os.listdir("./data")

file = data_files[0]
file = f"./data/{file}"

day_to_delta = {
    "Mon": timedelta(days=0),
    "Tue": timedelta(days=1),
    "Wed": timedelta(days=2),
    "Thu": timedelta(days=3),
    "Fri": timedelta(days=4),
}

def fetch_data(_class: str = None, week: Literal["Even", "Odd"] = None, subj: str = None, day: str = None, start_t: time = None, end_t: time = None,) -> list:
    connect = sqlite3.connect(file)
    try:
        with open("./src/command.txt", "r") as f:
            template = f.read()

        command = template
        params = []
        values = []

        if any(a for a in (_class, week, subj, day, start_t, end_t)):
            command += "WHERE "

        if _class:
            params.append(f"class LIKE ?")
            values.append(_class)

        if week:
            params.append(f"class LIKE ?")
            values.append(week)

        if subj:
            params.append(f"short_subj LIKE ?")
            values.append(subj)
        
        if day:
            params.append(f"week_day LIKE ?")
            values.append(day)

        if start_t:
            params.append(f"start_t_time LIKE ?")
            values.append(start_t.strftime('%-H:%M'))

        if end_t:
            params.append(f"end_time LIKE ?")
            values.append(end_t.strftime('%-H:%M'))

        if params:
            command += " AND ".join(params)
        
        cursor = connect.execute(command, tuple([f"%{v}%" for v in values]))
        rows = cursor.fetchall()

        return rows
    except Exception as e:
        connect.close()
        raise e
    
def format_data(data: list, start_dt: datetime) -> list:
    res = []

    for d in tqdm(data):
        _class, full_subj, subj, day, start_t, end_t = d
        start_t = datetime.strptime(start_t, "%H:%M")
        end_t = datetime.strptime(end_t, "%H:%M")
        
        start_dt = datetime(year=start_dt.year, month=start_dt.month, day=start_dt.day, hour=start_t.hour, minute=start_t.minute)
        end_dt = datetime(year=start_dt.year, month=start_dt.month, day=start_dt.day, hour=end_t.hour, minute=end_t.minute)

        # ocd hitting hard rn
        new_subj = ""
        for i in range(len(subj)):
            if subj[i] == '(' and (i == 0 or subj[i-1] != ' '):
                new_subj += ' '
            new_subj += subj[i]

        cur_event = {"title": new_subj, "alt": full_subj, "start": start_dt + day_to_delta[day], "end": end_dt + day_to_delta[day]}

        res.append(cur_event)

    return res

def clump_data(data: list) -> list:
    res = []
    data = sorted(data, key=lambda d: d["start"])

    cur = None

    for d in tqdm(data):
        if not cur:
            cur = d
        elif d["title"] == cur["title"]:
            cur = {"title": cur["title"], "alt": cur["alt"], "start": cur["start"], "end": d["end"]}
        else:
            res.append(cur)
            cur = d

    return res

def get_subjects(data: list) -> list:
    subj_lst = set()

    for d in data:
        subj_lst.add(d["title"])

    return list(subj_lst)

if __name__ == "__main__":
    json.dump(fetch_data(_class="4A3", week="Odd"), open("test.json", "w+"), indent=4)