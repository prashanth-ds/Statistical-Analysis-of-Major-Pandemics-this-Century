import csv
from django.db import connection


def enter():
    with open(r'C:\Users\...\Pandemics\downloaded data\covid19\WHO-COVID-19-global-data.csv', 'r') as file:
        csv_data = csv.reader(file, delimiter=',')
        data = []
        next(csv_data)
        for i in csv_data:
            temp = i[0]
            i[0] = temp[8:] + "/" + temp[5:7] + "/" + temp[:4]  # converting date format from YYYY-MM-DD to DD/MM/YYYY
            row = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]]
            data.append(row)

    count = 0
    with connection.cursor() as cursor:

        cursor.execute("TRUNCATE TABLE pandemics.covid_world_who;")
        print("Started entering World Data")
        for i in data:
            count = count + 1
            #i[0] = datetime.strptime(i[0], '%m-%d-%Y').strftime('%d/%m/%Y')
            var = cursor.execute("INSERT INTO pandemics.covid_world_who VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                 [count, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]])

        cursor.execute("UPDATE pandemics.covid_world_who SET country='Russia' WHERE country='Russian Federation'")
        cursor.execute("UPDATE pandemics.covid_world_who SET country='UK' WHERE country='The United Kingdom'")
        cursor.execute("UPDATE pandemics.covid_world_who SET country='USA' WHERE country='United States of America'")
        cursor.execute(
            "UPDATE pandemics.covid_world_who SET country='UAE' WHERE country='United Arab Emirates'")
        cursor.execute("UPDATE pandemics.covid_world_who SET country='Syria' WHERE country='Syrian Arab Republic'")
        print('End')


