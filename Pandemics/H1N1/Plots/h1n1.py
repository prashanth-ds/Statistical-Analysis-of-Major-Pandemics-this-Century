from iso3166 import countries
import pandas as pd
from H1N1 import tasks


def total_cases_world_map(entry):
    country = []
    cases = []
    deaths = []
    for i in entry:
        country.append(i['country'])
        cases.append(i['total_cases'])
        deaths.append(i['total_deaths'])

    countries_name_code = country
    for n, i in enumerate(countries_name_code):
        if i == 'South Korea':
            countries_name_code[n] = 'Korea, Republic of'
        elif i == 'United Kingdom':
            countries_name_code[n] = 'United Kingdom of Great Britain and Northern Ireland'
        elif i == 'Vietnam':
            countries_name_code[n] = 'Viet Nam'
        elif i == 'Russia':
            countries_name_code[n] = 'Russian Federation'
        elif i == 'Czech Republic':
            countries_name_code[n] = 'Czechia'
        elif i == 'Democratic Republic of Congo':
            countries_name_code[n] = 'Congo'
        elif i == 'SÃ£o TomÃ© and PrÃ­ncipe':
            countries_name_code[n] = 'Sao Tome and Principe'
        elif i == 'Iran':
            countries_name_code[n] = 'Iran, Islamic Republic of'
        elif i == 'Macedonia':
            countries_name_code[n] = 'North Macedonia'
        elif i == 'Bolivia':
            countries_name_code[n] = 'Bolivia, Plurinational State of'
        elif i == 'Venezuela':
            countries_name_code[n] = 'Venezuela, Bolivarian Republic of'
        elif i == 'Moldova':
            countries_name_code[n] = 'Moldova, Republic of'
        elif i == 'Brunei':
            countries_name_code[n] = 'Brunei Darussalam'
        elif i == 'Tanzania':
            countries_name_code[n] = 'Tanzania, United Republic of'
        elif i == 'Laos':
            countries_name_code[n] = 'LAO'
        elif i == 'Syria':
            countries_name_code[n] = 'SYRIAN ARAB REPUBLIC'
        elif i == 'Cape Verde':
            countries_name_code[n] = 'CPV'
        elif i == 'Akrotiri and Dhekelia':
            countries_name_code[n] = 'CY'
        elif i == 'North Korea':
            countries_name_code[n] = 'PRK'
        elif i == 'Republic of the Congo':
            countries_name_code[n] = 'COG'
        elif i == 'Falkland Islands':
            countries_name_code[n] = 'FLK'
        elif i == 'CÃ´te d\'Ivoire':
            countries_name_code[n] = 'CIV'
        elif i == 'Swaziland':
            countries_name_code[n] = 'SWZ'

    codes = []
    for i in countries_name_code:
        codes.append(countries.get(i)[2])

    df = pd.DataFrame({'Country': country, 'Total Deaths': deaths, 'Code': codes})
    df.set_index('Country', inplace=True)

    world_map = tasks.world_map(df, title='Total Deaths', legend='Cases')
    return world_map


def total_cases_bar(entry):
    country = []
    cases = []
    for i in entry:
        country.append(i['country'])
        cases.append(i['total_cases'])

    df = pd.DataFrame({'Country': country, 'Total Cases': cases})
    df.set_index('Country', inplace=True)
    df.drop(index='USA', inplace=True)

    bar_chart = tasks.total_cases_bar_chart(df, 'Total Cases', 'Total Cases')

    return bar_chart


def total_deaths_bar(entry):
    country = []
    deaths = []
    for i in entry:
        country.append(i['country'])
        deaths.append(i['total_deaths'])

    df = pd.DataFrame({'Country': country, 'Total Deaths': deaths})
    df.set_index('Country', inplace=True)
    df.drop(index='USA', inplace=True)

    bar_chart = tasks.total_cases_bar_chart(df, 'Total Deaths', 'Total Deaths')

    return bar_chart


