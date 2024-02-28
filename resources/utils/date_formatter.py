import datetime

def convert_date(row):
    for key, value in row.items():
        if isinstance(value, datetime.date):
            row[key] = value.strftime('%Y-%m-%d')
    return row