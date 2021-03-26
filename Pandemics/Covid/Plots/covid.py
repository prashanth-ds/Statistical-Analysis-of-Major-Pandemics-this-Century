import pandas as pd
from .. import tasks
from django.db import connection
from iso3166 import countries


def total_D_R(data):
    print(data)
    country = []
    total_deaths = []
    total_recovered = []
    total_cases = []
    for i in data:
        total_cases.append(i['total_cases'])
        country.append(i['country_name'])
        total_deaths.append(i['total_deaths'])
        total_recovered.append(i['total_recovered'])
    df = pd.DataFrame({'Country': country,
                       'Total Cases': total_cases,
                       'Total Deaths': total_deaths,
                       'Total Recovered': total_recovered})
    df.set_index('Country', inplace=True)
    df['Total Deaths'] = df['Total Deaths'].replace(['N/A'], '0')
    df['Total Deaths'] = df['Total Deaths'].str.replace(',', '')
    df['Total Recovered'] = df['Total Recovered'].str.replace(',', '')
    df['Total Recovered'] = df['Total Recovered'].replace(['N/A'], '0')
    df['Total Cases'] = df['Total Cases'].str.replace(',', '')
    df['Total Cases'] = pd.to_numeric(df['Total Cases'])
    df['Total Deaths'] = pd.to_numeric(df['Total Deaths'])
    df['Total Recovered'] = pd.to_numeric(df['Total Recovered'])
    df['Recovered Rate'] = (df['Total Recovered']/df['Total Cases'])*100
    df['Death Rate'] = (df['Total Deaths']/df['Total Cases'])*100
    df['Recovered Rate'] = df['Recovered Rate'].round(decimals=2)
    df['Death Rate'] = df['Death Rate'].round(decimals=2)
    df.drop(['Total Deaths', 'Total Recovered', 'Total Cases'], axis=1, inplace=True)
    print(df.head())
    line_graph = tasks.line_chart(df,  columns=2, legend=['Recovery Rate', 'Death Rate'],
                                  color1='green', color2='red', title='Recovery Rate vs Death Rate (%)')
    return line_graph


def new_cases_bar(data):
    country = []
    val = []
    for i in data:
        country.append(i['country_name'])
        val.append(i['new_cases'])
    df = pd.DataFrame({'Country': country, 'New Cases': val})
    df.set_index('Country', inplace=True)
    df['New Cases'] = df['New Cases'].replace(['N/A'], '0')
    df['New Cases'] = df['New Cases'].map(lambda x: x.lstrip('+'))
    df['New Cases'] = df['New Cases'].str.replace(',', '')
    df['New Cases'] = pd.to_numeric(df['New Cases'])
    bar_graph = tasks.bar_chart(df, legend=['New Cases'], title='New Cases')
    return bar_graph


def total_cases_map():
    countries_name_codes = ['USA', 'India', 'Brazil', 'Russian Federation', 'France', 'Spain', 'Argentina', 'Colombia',
                            'United Kingdom of Great Britain and Northern Ireland', 'Mexico', 'Peru',
                            'South Africa', 'Iran, Islamic Republic of', 'Italy', 'Chile', 'Germany', 'Iraq',
                            'Bangladesh', 'Indonesia', 'Philippines',
                            'Ukraine', 'Turkey', 'Belgium', 'Saudi Arabia', 'Pakistan', 'Netherlands', 'Poland',
                            'Israel',
                            'Czechia', 'Canada', 'Romania', 'Morocco', 'Ecuador', 'Nepal',
                            'Bolivia, Plurinational State of', 'Switzerland', 'Qatar',
                            'Panama', 'United Arab Emirates', 'Portugal', 'Dominican Republic', 'Kuwait', 'Sweden',
                            'Oman', 'Kazakhstan', 'Egypt',
                            'Costa Rica', 'Guatemala', 'Japan', 'Belarus', 'Honduras', 'Ethiopia',
                            'Venezuela, Bolivarian Republic of', 'Austria', 'China',
                            'Armenia', 'Bahrain', 'Lebanon', 'Moldova, Republic of', 'Hungary', 'Uzbekistan', 'Nigeria',
                            'Jordan', 'Paraguay',
                            'Ireland', 'Libya', 'Singapore', 'Kyrgyzstan', 'Algeria', 'Tunisia', 'Azerbaijan',
                            'Palestine', 'Kenya',
                            'Slovakia', 'Myanmar', 'Ghana', 'Bulgaria', 'Bosnia and Herzegovina', 'Croatia', 'Denmark',
                            'Serbia',
                            'Afghanistan', 'Georgia', 'Greece', 'El Salvador', 'Slovenia', 'Malaysia',
                            'North Macedonia',
                            'Korea, Republic of', 'Cameroon', 'Albania', 'Norway', 'Montenegro', 'Madagascar', 'Zambia',
                            'Luxembourg', 'Senegal', 'Finland', 'Sudan', 'Lithuania', 'Namibia', 'Mozambique', 'Guinea',
                            'Uganda',
                            'Maldives', 'Tajikistan', 'French Guiana', 'Angola', 'Sri Lanka', 'Haiti', 'Gabon',
                            'Jamaica',
                            'Cabo Verde', 'Zimbabwe', 'Mauritania', 'Guadeloupe', 'French Polynesia', 'Cuba', 'Bahamas',
                            'Botswana', 'Malawi', 'Eswatini', 'Malta', 'Trinidad and Tobago', 'Syrian Arab Republic',
                            'Djibouti', 'Nicaragua',
                            'Latvia', 'Hong Kong', 'Congo', 'Suriname', 'Rwanda', 'Equatorial Guinea',
                            'Estonia',
                            'Iceland', 'Andorra', 'Aruba', 'Mayotte', 'Guyana', 'Somalia', 'Cyprus', 'Thailand',
                            'Gambia',
                            'Martinique', 'Mali', 'Belize', 'Uruguay', 'South Sudan', 'Benin', 'Burkina Faso',
                            'Guinea-Bissau',
                            'Sierra Leone', 'Togo', 'Yemen', 'New Zealand', 'Lesotho', 'Chad', 'Liberia', 'Viet Nam',
                            'Sao Tome and Principe', 'San Marino', 'Australia',
                            'Taiwan']

    countries_name = ['USA', 'India', 'Brazil', 'Russia', 'France', 'Spain', 'Argentina', 'Colombia', 'UK', 'Mexico',
                      'Peru',
                      'South Africa', 'Iran', 'Italy', 'Chile', 'Germany', 'Iraq', 'Bangladesh', 'Indonesia',
                      'Philippines',
                      'Ukraine', 'Turkey', 'Belgium', 'Saudi Arabia', 'Pakistan', 'Netherlands', 'Poland', 'Israel',
                      'Czechia', 'Canada', 'Romania', 'Morocco', 'Ecuador', 'Nepal', 'Bolivia', 'Switzerland', 'Qatar',
                      'Panama', 'UAE', 'Portugal', 'Dominican Republic', 'Kuwait', 'Sweden', 'Oman', 'Kazakhstan',
                      'Egypt',
                      'Costa Rica', 'Guatemala', 'Japan', 'Belarus', 'Honduras', 'Ethiopia', 'Venezuela', 'Austria',
                      'China',
                      'Armenia', 'Bahrain', 'Lebanon', 'Moldova', 'Hungary', 'Uzbekistan', 'Nigeria', 'Jordan',
                      'Paraguay',
                      'Ireland', 'Libya', 'Singapore', 'Kyrgyzstan', 'Algeria', 'Tunisia', 'Azerbaijan', 'Palestine',
                      'Kenya',
                      'Slovakia', 'Myanmar', 'Ghana', 'Bulgaria', 'Bosnia and Herzegovina', 'Croatia', 'Denmark',
                      'Serbia',
                      'Afghanistan', 'Georgia', 'Greece', 'El Salvador', 'Slovenia', 'Malaysia', 'North Macedonia',
                      'S. Korea', 'Cameroon', 'Albania', 'Norway', 'Montenegro', 'Madagascar', 'Zambia',
                      'Luxembourg', 'Senegal', 'Finland', 'Sudan', 'Lithuania', 'Namibia', 'Mozambique', 'Guinea',
                      'Uganda',
                      'Maldives', 'Tajikistan', 'French Guiana', 'Angola', 'Sri Lanka', 'Haiti', 'Gabon', 'Jamaica',
                      'Cabo Verde', 'Zimbabwe', 'Mauritania', 'Guadeloupe', 'French Polynesia', 'Cuba', 'Bahamas',
                      'Botswana', 'Malawi', 'Eswatini', 'Malta', 'Trinidad and Tobago', 'Syria', 'Djibouti',
                      'Nicaragua',
                      'Latvia', 'Hong Kong', 'Congo', 'Suriname', 'Rwanda', 'Equatorial Guinea', 'Estonia',
                      'Iceland', 'Andorra', 'Aruba', 'Mayotte', 'Guyana', 'Somalia', 'Cyprus', 'Thailand', 'Gambia',
                      'Martinique', 'Mali', 'Belize', 'Uruguay', 'South Sudan', 'Benin', 'Burkina Faso',
                      'Guinea-Bissau',
                      'Sierra Leone', 'Togo', 'Yemen', 'New Zealand', 'Lesotho', 'Chad', 'Liberia', 'Vietnam',
                      'Sao Tome and Principe', 'San Marino', 'Australia',
                      'Taiwan']


    codes = []

    for i in countries_name_codes:
        codes.append(countries.get(i)[2])

    data = []
    with connection.cursor() as cursor:
        for i in countries_name:
            cursor.execute("SELECT country_name, total_cases FROM pandemics.covid_daily WHERE country_name=%s", [i])
            data.append(cursor.fetchone())

    cc = []
    val = []
    for i in data:
        cc.append(i[0])
        val.append(i[1])

    entry = {'Country': cc, 'Total Cases': val, 'Code': codes}

    df = pd.DataFrame(entry)
    df.set_index('Country', inplace=True)
    df['Total Cases'] = df['Total Cases'].str.replace(',', '')
    df['Total Cases'] = pd.to_numeric(df['Total Cases'])
    world_map = tasks.world_map(df, title='Total Cases', legend='Cases')
    return world_map


def total_cases_india_plotly(data):
    state = []
    confirmed_total = []
    for i in data:
        state.append(i['state_unionT'])
        confirmed_total.append(i['confirmed_total'])

    df = pd.DataFrame({'State': state, 'Total Cases': confirmed_total})
    df['Total Cases'] = pd.to_numeric(df['Total Cases'])
    df['State'].replace('Jammu and Kashmir', 'Jammu & Kashmir', inplace=True)
    df['State'].replace('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli and Daman and Diu', inplace=True)
    df['State'].replace('Andaman and Nicobar Islands', 'Andaman & Nicobar', inplace=True)

    india_map = tasks.india_map(df)

    return india_map


def country_daily_cases_line_graph(entry):
    date = []
    new_cases = []
    new_deaths = []
    for i in entry:
        date.append(i['date_reported'])
        new_cases.append(i['new_cases'])
        new_deaths.append(i['new_deaths'])

    df = pd.DataFrame({'Date': date, 'New Cases': new_cases, 'New Deaths': new_deaths})
    df.set_index('Date', inplace=True)
    df['New Cases'] = df['New Cases'].str.replace('+', '')
    df['New Cases'] = pd.to_numeric(df['New Cases'])
    df['New Deaths'] = df['New Deaths'].str.replace('+', '')
    df['New Deaths'] = pd.to_numeric(df['New Deaths'])

    line_graph = tasks.line_chart_non_p(df, legend=['New Cases', ' New Deaths'],
                                        color1='green', color2='red', title='New Cases vs New Deaths',
                                        x_title='Date Reported')
    return line_graph


def state_graph_dates_cases(entry):
    date = []
    total_cases = []
    cured = []
    death = []
    for i in entry:
        date.append(i['date'])
        total_cases.append(i['total_cases'])
        cured.append(i['cured'])
        death.append(i['death'])

    df = pd.DataFrame({'Date': date,
                       'Total Cases': total_cases,
                       'Cured': cured,
                       'Death': death})
    df.set_index('Date', inplace=True)
    df['Total Cases'] = pd.to_numeric(df['Total Cases'])
    df['Cured'] = pd.to_numeric(df['Cured'])
    df['Death'] = pd.to_numeric(df['Death'])
    df['Cured Rate'] = (df['Cured']/df['Total Cases'])*100
    df['Death Rate'] = (df['Death']/df['Total Cases'])*100
    df.drop(['Total Cases', 'Cured', 'Death'], axis=1, inplace=True)

    line_graph = tasks.line_chart_non_p(df, legend=['Cured Rate', 'Death Rate'], color1='green', color2='red',
                                        title='Cured Rate vs Death Rate (%)', x_title='Date Reported')

    return line_graph


def state_graph_dates_samples(entry):
    date = []
    total_samples = []
    positive_samples = []
    negative_samples = []
    for i in entry:
        date.append(i['date'])
        total_samples.append(i['total_samples'])
        positive_samples.append(i['positive'])
        negative_samples.append(i['negative'])

    df = pd.DataFrame({'Date': date,
                       'Total Samples': total_samples,
                       'Positive Samples': positive_samples,
                       'Negative Samples': negative_samples})
    df.set_index('Date', inplace=True)
    df['Total Samples'] = pd.to_numeric(df['Total Samples'])
    df = df[(df != 'NA').all(1)]
    df['Positive Rate'] = (df['Positive Samples'] / df['Total Samples']) * 100
    df['Negative Rate'] = (df['Negative Samples'] / df['Total Samples']) * 100
    df.drop(['Total Samples', 'Positive Samples', 'Negative Samples'], axis=1, inplace=True)

    line_graph = tasks.line_chart_non_p(df, legend=['Positive Rate', 'Negative Rate'], color1='green',
                                        color2='red', title='Positive Sample Rate vs Negative Sample Rate (%)',
                                        x_title='Date Reported')

    return line_graph


def stacked_bar_graph_all(entry):
    state = []
    total_cases = []
    total_recovered = []
    total_deaths = []
    active_cases = []
    for i in entry:
        state.append(i['state_unionT'])
        total_cases.append(i['confirmed_total'])
        total_recovered.append(i['cured'])
        total_deaths.append(i['death'])
        active_cases.append(i['active_cases'])
    df = pd.DataFrame({'State': state, 'Total Cases': total_cases,
                       'Total Recovered': total_recovered, 'Total Deaths': total_deaths,
                       'Active Cases': active_cases})
    df.set_index('State', inplace=True)
    df['Total Cases'] = pd.to_numeric(df['Total Cases'])
    df['Total Recovered'] = pd.to_numeric(df['Total Recovered'])
    df['Total Deaths'] = pd.to_numeric(df['Total Deaths'])
    bar_graph = tasks.stacked_bar_graph(df, legend=['Total Cases', 'Total Recovered', 'Total Deaths', 'Active Cases'],
                                title='Stacked Bar Graph')
    return bar_graph

