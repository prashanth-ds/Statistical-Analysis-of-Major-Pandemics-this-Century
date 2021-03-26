from selenium import webdriver
import os
from django.db import connection
from Covid.models import WorldDaily


# Web Scraping

os.environ['MOZ_HEADLESS'] = '1'

countries_name = ['USA', 'India', 'Brazil', 'Russia', 'France', 'Spain', 'Argentina', 'Colombia', 'UK', 'Mexico', 'Peru',
                 'South Africa', 'Iran', 'Italy', 'Chile', 'Germany', 'Iraq', 'Bangladesh', 'Indonesia', 'Philippines',
                 'Ukraine', 'Turkey', 'Belgium', 'Saudi Arabia', 'Pakistan', 'Netherlands', 'Poland', 'Israel',
                 'Czechia', 'Canada', 'Romania', 'Morocco', 'Ecuador', 'Nepal', 'Bolivia', 'Switzerland', 'Qatar',
                 'Panama', 'UAE', 'Portugal', 'Dominican Republic', 'Kuwait', 'Sweden', 'Oman', 'Kazakhstan', 'Egypt',
                 'Costa Rica', 'Guatemala', 'Japan', 'Belarus', 'Honduras', 'Ethiopia', 'Venezuela', 'Austria', 'China',
                 'Armenia', 'Bahrain', 'Lebanon', 'Moldova', 'Hungary', 'Uzbekistan', 'Nigeria', 'Jordan', 'Paraguay',
                 'Ireland', 'Libya', 'Singapore', 'Kyrgyzstan', 'Algeria', 'Tunisia', 'Azerbaijan', 'Palestine', 'Kenya',
                 'Slovakia', 'Myanmar', 'Ghana', 'Bulgaria', 'Bosnia and Herzegovina', 'Croatia', 'Denmark', 'Serbia',
                 'Afghanistan', 'Georgia', 'Greece', 'El Salvador', 'Slovenia', 'Malaysia', 'North Macedonia',
                 'S. Korea', 'Cameroon', 'Ivory Coast', 'Albania', 'Norway', 'Montenegro', 'Madagascar', 'Zambia',
                 'Luxembourg', 'Senegal', 'Finland', 'Sudan', 'Lithuania', 'Namibia', 'Mozambique', 'Guinea', 'Uganda',
                 'Maldives', 'DRC', 'Tajikistan', 'French Guiana', 'Angola', 'Sri Lanka', 'Haiti', 'Gabon', 'Jamaica',
                 'Cabo Verde', 'Zimbabwe', 'Mauritania', 'Guadeloupe', 'French Polynesia', 'Cuba', 'Bahamas',
                 'Botswana', 'Malawi', 'Eswatini', 'Malta', 'Trinidad and Tobago', 'Syria', 'Djibouti', 'Nicaragua',
                 'Réunion', 'Latvia', 'Hong Kong', 'Congo', 'Suriname', 'Rwanda', 'Equatorial Guinea', 'CAR', 'Estonia',
                 'Iceland', 'Andorra', 'Aruba', 'Mayotte', 'Guyana', 'Somalia', 'Cyprus', 'Thailand', 'Gambia',
                 'Martinique', 'Mali', 'Belize', 'Uruguay', 'South Sudan', 'Benin', 'Burkina Faso', 'Guinea-Bissau',
                 'Sierra Leone', 'Togo', 'Yemen', 'New Zealand', 'Lesotho', 'Chad', 'Liberia', 'Nigeria', 'Vietnam',
                 'Sao Tome and Principe', 'Curaçao', 'San Marino', 'Channel Islands', 'Sint Maarten', 'Australia',
                 'Taiwan']

data_dict = {}
# data_dict[0] = ['Country Name', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered',
#                 'Active Cases', 'Population']
# indexes - 1,2,3,4,5,6,7,11,13


def connection_driver():
    print("trying driver connection")
    driver = webdriver.Firefox(executable_path=r"C:\Users\Prashanth\Downloads\geckodriver.exe")
    driver.get('https://www.worldometers.info/coronavirus/')
    print("driver connection succeeded")
    return driver


count = -1


def send():
    global count
    count = count + 1
    if count == 169:
        return "//a[contains(., 'Australia')]"
    return "//td[contains(.,'%s')]" % countries_name[count]


def make(country_path):
    global data_dict
    if count == 169:
        data = country_path.find_element_by_xpath("./../..")
    else:
        data = country_path.find_element_by_xpath("./..")
    test = data.text.split(" ")
    if " " in countries_name[count]:
        space = countries_name[count].count(" ")
        if space == 1:
            if '+' in test[4]:
                if '+' in test[6]:  # here 4 and 6 index will be changed as there is one space in name
                    data_dict[test[0]] = [countries_name[count], test[3], test[4], test[5], test[6], test[7], test[8],
                                          test[len(test) - 1]]
                else:
                    data_dict[test[0]] = [countries_name[count], test[3], test[4], test[5], "N/A", test[6], test[7],
                                          test[len(test) - 1]]
            elif '+' not in test[4]:
                if '+' not in test[4]:
                    data_dict[test[0]] = [countries_name[count], test[3], "N/A", test[4], "N/A", test[5], test[6],
                                          test[len(test) - 1]]
                else:
                    data_dict[test[0]] = [countries_name[count], test[3], "N/A", test[4], test[5], test[6], test[7],
                                          test[len(test) - 1]]
        else:
            if '+' in test[space + 3]:
                if '+' in test[space + 5]:
                    data_dict[test[0]] = [countries_name[count], test[space + 2], test[space + 3], test[space + 4],
                                          test[space + 5], test[space + 6], test[space + 7], test[len(test) - 1]]
                else:
                    data_dict[test[0]] = [countries_name[count], test[space + 2], test[space + 3], test[space + 4], "N/A",
                                          test[space + 5], test[space + 6], test[len(test) - 1]]
            elif '+' not in test[space + 3]:
                if '+' not in test[space + 4]:
                    data_dict[test[0]] = [countries_name[count], test[space + 2], "N/A", test[space + 3], "N/A",
                                          test[space + 4], test[space + 5], test[len(test) - 1]]
                else:
                    data_dict[test[0]] = [countries_name[count], test[space + 2], "N/A", test[space + 3], test[space + 4],
                                          test[space + 5], test[space + 6], test[len(test) - 1]]
    else:
        if '+' in test[3]:
            if '+' in test[5]:  # here 3 and 5 index will be changed as there is one space in name
                data_dict[test[0]] = [countries_name[count], test[2], test[3], test[4], test[5], test[6], test[7],
                                      test[len(test) - 1]]
            else:
                data_dict[test[0]] = [countries_name[count], test[2], test[3], test[4], "N/A", test[5], test[6],
                                      test[len(test) - 1]]
        elif '+' not in test[3]:
            if '+' not in test[4]:
                data_dict[test[0]] = [countries_name[count], test[2], "N/A", test[3], "N/A",  test[4], test[5],
                                      test[len(test) - 1]]
            else:
                data_dict[test[0]] = [countries_name[count], test[2], "N/A", test[3], test[4], test[5], test[6],
                                      test[len(test) - 1]]


flag = 0


def collect(driver):
    table = driver.find_element_by_xpath('//table[@id="main_table_countries_today"]/tbody[1]')
    country = table.find_element_by_xpath(send())
    make(country)


def call_collect():

    driver = connection_driver()

    global data_dict
    global flag
    for i in range(171):
        collect(driver)
        if i == 170:
            driver.quit()
    data_dict = {int(key): val for key, val in data_dict.items()}
    data = sorted(data_dict.items())
    data_dict = {i[0]: i[1] for i in data}
    flag = 0


def enter_data():
    global count
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE pandemics.covid_daily")

    for i in data_dict.values():
        val = WorldDaily.objects.create(country_name=i[0], total_cases=i[1], new_cases=i[2], total_deaths=i[3],
                                        new_deaths=i[4], total_recovered=i[5], active_cases=i[6], population=i[7])
        val.save()
    count = -1  # as the file will be running multiple times as scheduled and count is global

    return None



