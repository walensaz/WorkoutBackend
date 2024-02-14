def convert_date(row):
    row['date'] = row['date'].strftime('%m-%d-%Y')
    return row