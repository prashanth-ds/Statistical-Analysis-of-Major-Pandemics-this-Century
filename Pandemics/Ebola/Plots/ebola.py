from iso3166 import countries
import pandas as pd
from Ebola import tasks


def total_cases_map(entry):
    countries_name_code = ['Sierra Leone', 'Liberia', 'Guinea', 'Congo',  'Uganda', 'Sudan', 'Gabon', 'Nigeria', 'Mali',
                           'USA', 'Italy', 'United Kingdom of Great Britain and Northern Ireland', 'Spain', 'Senegal',
                           'South Africa', 'CIV']

    codes = []
    for i in countries_name_code:
        codes.append(countries.get(i)[2])

    country = []
    cases = []
    for i in entry:
        country.append(i['country'])
        cases.append(i['total_cases'])

    df = pd.DataFrame({'Country': country, 'Total Cases': cases, 'Code':codes})
    df.set_index('Country', inplace=True)
    world_map = tasks.world_map(df, title='Total Cases', legend='Cases')
    return world_map


def stack_bar_chart(entry):
    country = []
    total_cases = []
    total_deaths = []
    for i in entry:
        country.append(i['country'])
        total_cases.append(i['total_cases'])
        total_deaths.append(i['total_deaths'])

    df = pd.DataFrame({'Country': country, 'Total Cases': total_cases, 'Total Deaths': total_deaths})

    stacked_bar_chart = tasks.bar_chart(df, 'Total Cases & Total Deaths')

    return stacked_bar_chart
