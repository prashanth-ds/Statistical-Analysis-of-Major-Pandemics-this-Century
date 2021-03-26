import os
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pandemics.settings')

import django

django.setup()

from django.db import connection


f_name = [r'downloaded data/H1N1/summary_africa.csv', r'downloaded data/H1N1/summary_asia.csv',
          r'downloaded data/H1N1/summary_europe.csv', r'downloaded data/H1N1/summary_south_america.csv']

data = []
flag = r'downloaded data/H1N1/summary_south_america.csv'

for k in f_name:
    if k == flag: reps = 1
    else: reps =0
    with open(k, 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)
        for i in csv_data:
            if not reps :
                row = [i[0], int(i[1]), int(i[2])]
                data.append(row)
            else:
                row = [i[0], int(i[1]), int(i[3])]
                data.append(row)

count = 0

with connection.cursor() as cursor:
    cursor.execute("TRUNCATE TABLE pandemics.h1n1_world")
    for i in data:
        print(i)
        count = count+1
        var = cursor.execute("INSERT INTO pandemics.h1n1_world VALUES(%s, %s, %s, %s)",
                             [count, i[0], i[1], i[2]])

    count = count+1
    # 'https://www.cdc.gov/flu/pandemic-resources/2009-h1n1-pandemic.html#:~:text=From%20April%2012%2C%202009%20to,the%20(H1N1)pdm09%20virus.'
    var = cursor.execute("INSERT INTO pandemics.h1n1_world VALUES(%s, %s, %s, %s)",
                         [count, 'USA', 60800000, 12469])

    count = count + 1
    # 'https://ipac-canada.org/pandemic-h1n1-resources.php'
    var = cursor.execute("INSERT INTO pandemics.h1n1_world VALUES(%s, %s, %s, %s)",
                         [count, 'Canada', 12262+33509+1024+1063+1274+10436, 77+428+0+0+1+0])

    count = count + 1
    # 'https://en.wikipedia.org/wiki/2009_swine_flu_pandemic_in_Australia#:~:text=Australia%20had%2037%2C537%20confirmed%20cases,the%20Australian%20Bureau%20of%20Statistics.&text=Sources%20say%20that%20as%20many,a%20result%20of%20this%20virus.'
    var = cursor.execute("INSERT INTO pandemics.h1n1_world VALUES(%s, %s, %s, %s)",
                         [count, 'Australia', 37537, 191])

    count = count + 1
    # 'https://en.wikipedia.org/wiki/2009_swine_flu_pandemic_in_New_Zealand#:~:text=On%2017%20June%2C%20there%20was,experienced%20a%20community%20level%20outbreak.'
    var = cursor.execute("INSERT INTO pandemics.h1n1_world VALUES(%s, %s, %s, %s)",
                         [count, 'New Zealand', 3175, 19])

    count = count + 1
    # 'https://en.wikipedia.org/wiki/2009_swine_flu_pandemic_in_Mexico'
    var = cursor.execute("INSERT INTO pandemics.h1n1_world VALUES(%s, %s, %s, %s)",
                         [count, 'Mexico', 50234, 398])

