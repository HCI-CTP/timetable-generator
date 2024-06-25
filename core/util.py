import os
import sqlite3

from datetime import time

data_files = os.listdir("./data")

file = data_files[0]
file = f"./data/{file}"

def fetch(_class: str = None, week: str = None, subj: str = None, day: str = None, start: time = None, end: time = None,) -> list:
    connect = sqlite3.connect(file)
    try:
        with open("./src/command.txt", "r") as f:
            template = f.read()

        command = template

        if any(a for a in (_class, week, subj, day, start, end)):
            command += "WHERE "
            params = []
            values = []

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

        if start:
            params.append(f"start_time LIKE ?")
            values.append(start.strftime('%-H:%M'))

        if end:
            params.append(f"end_time LIKE ?")
            values.append(end.strftime('%-H:%M'))

        command += " AND ".join(params)
        
        cursor = connect.execute(command, tuple([f"%{v}%" for v in values]))
        rows = cursor.fetchall()

        return rows
    except Exception as e:
        connect.close()

        raise e