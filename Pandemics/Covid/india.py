import csv
from django.db import connection


def enter():

    with open(r'C:\Users\...\Pandemics\downloaded data\covid19\covid_19_india.csv', 'r') as file:
        csv_data = csv.reader(file)
        data = []
        for i in csv_data:
            before_change = i[1]
            changed_date = before_change[:6] + "20" + before_change[6:]
            i[1] = changed_date
            data.append(i)

        length = len(data)

    with open(r'C:\Users\...\Pandemics\downloaded data\covid19\test.csv', 'w', newline='') as file:

        writer = csv.writer(file)
        writer.writerows(data)

    with open(r'C:\Users\...\Pandemics\downloaded data\covid19\test.csv', 'r') as file:
        csv_data = csv.reader(file)
        data = []
        next(csv_data)
        for i in csv_data:
            row = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]]
            data.append(row)

    count = 0

    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE pandemics.covid_india;")
        print("Started entering India's details")
        for i in data:
            count = count+1
            # i[0] = datetime.strptime(i[0], '%m-%d-%Y').strftime('%d/%m/%Y')
            var = cursor.execute("INSERT INTO pandemics.covid_india VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                 [count, i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]])

        cursor.execute("UPDATE pandemics.covid_india SET state_unionT='Dadra and Nagar Haveli' WHERE"
                       " state_unionT='Dadra and Nagar Haveli and Daman and Diu'")
        print("End")

