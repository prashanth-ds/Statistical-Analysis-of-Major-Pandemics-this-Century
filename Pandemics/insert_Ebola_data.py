import os
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pandemics.settings')
import django

django.setup()

from django.db import connection


with open(r'downloaded data/Ebola/Ebola.csv', 'r') as file:
    csv_data = csv.reader(file)
    next(csv_data)
    data = []
    for i in csv_data:
        row = [i[0], int(i[1]), int(i[2])]
        data.append(row)

count = 0

with connection.cursor() as cursor:
    for i in data:
        count = count+1
        var = cursor.execute("INSERT INTO pandemics.ebola_world VALUES(%s, %s, %s, %s)",
                             [count, i[0], i[1], i[2]])

