def convert_date(row):
    row['date'] = row['date'].strftime('%Y-%m-%d')
    return row