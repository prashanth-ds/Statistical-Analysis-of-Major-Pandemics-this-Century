
import csv
from django.db import connection

def enter():
    with open(r'C:\Users\...\Pandemics\downloaded data\covid19\StatewiseTestingDetails.csv', 'r') as file:
        csv_data = csv.reader(file)
        data = []
        for i in csv_data:
            before_change = i[0]
            changed_date = before_change[8:] + "/" + before_change[5:7] + "/" + before_change[:4]
            i[0] = changed_date
            data.append(i)

        length = len(data)

    with open(r'C:\Users\...\Pandemics\downloaded data\covid19\test.csv', 'w', newline='') as file:

        writer = csv.writer(file)
        writer.writerows(data)

    def change(key):
        if key == '':
            return "NA"
        else:
            return key

    with open(r'C:\Users\...\Pandemics\downloaded data\covid19\test.csv', 'r') as file:
        csv_data = csv.reader(file)
        data = []
        next(csv_data)
        for i in csv_data:
            row = [change(i[0]), change(i[1]), change(i[2]), change(i[3]), change(i[4])]
            data.append(row)
            # print(i)

    count = 0
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE pandemics.covid_india_testing;")
        for i in data:
            count = count+1
            # i[0] = datetime.strptime(i[0], '%m-%d-%Y').strftime('%d/%m/%Y')
            var = cursor.execute("INSERT INTO pandemics.covid_india_testing VALUES (%s, %s, %s, %s, %s, %s)",
                                 [count, i[0], i[1], i[2], i[3], i[4]])

        cursor.execute("UPDATE pandemics.covid_india_testing SET state_unionT='Dadra and Nagar Haveli' WHERE"
                       " state_unionT='Dadra and Nagar Haveli and Daman and Diu'")
        print('End')
