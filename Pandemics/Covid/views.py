from django.shortcuts import render
from django.views.generic import View
from django.db import connection
from datetime import datetime, timedelta
from Covid import TS
from Covid.Plots import covid
import copy
from Covid import emaliing
import csv
# Create your views here


class TempView(View):

    def get(self, request, *args, **kwargs):

        def tuple_to_dict(entry):
            complete_list = []
            for i in entry:
                inside_dict = {}
                inside_dict['id'] = i[0]
                inside_dict['country_name'] = i[1]
                inside_dict['total_cases'] = i[2]
                inside_dict['new_cases'] = i[3]
                inside_dict['total_deaths'] = i[4]
                inside_dict['new_deaths'] = i[5]
                inside_dict['total_recovered'] = i[6]
                inside_dict['active_cases'] = i[7]
                inside_dict['population'] = i[8]
                inside_dict['latest_update'] = i[9]
                complete_list.append(inside_dict)
            return complete_list

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pandemics.covid_daily;")
            var = cursor.fetchall()

        data = tuple_to_dict(var)

        bar_graph_new_cases = covid.new_cases_bar(data)

        # prepare data for total deaths and recovered graph
        line_graph_total_D_R = covid.total_D_R(data)

        # world map for total cases
        world_map_total_cases = covid.total_cases_map()

        context = {'world_daily': data,
                   'bar_graph_new_cases': bar_graph_new_cases,
                   'line_graph_total_D_R': line_graph_total_D_R,
                   'world_map_total_cases': world_map_total_cases
                   }

        if request.method == 'GET':
            name = request.GET.get('name-user', False)  # .get() has to be used to avoid multiDictKeyValues Error instead of using GET['ex']
            email = request.GET.get('email-id', False)
            if name is not False and email is not False:
                cols = ['Date', 'Country', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered',
                        'Active Cases', 'Population', 'DateTime']
                filename = 'Covid/static/Covid/Mailing/LiveData.csv'
                var = data

                with open(filename, 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(cols)
                    for i in var:
                        writer.writerow((i['id'], i['country_name'], i['total_cases'], i['new_cases'], i['total_deaths'],
                                         i['new_deaths'], i['total_recovered'], i['active_cases'], i['population'],
                                         i['latest_update']))

                emaliing.email(name=name,
                               mailid=email,
                               subject="Live Covid Stats as of {}".format(datetime.now()),
                               file_path=filename)

        return render(request, 'Covid/daily.html', context=context)


class EachCountryDetails(View):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, country_name FROM pandemics.covid_daily")
        ids = cursor.fetchall()

    def get(self, request, *args, **kwargs):

        def tuple_to_dict(entry):
            complete_list = []
            for i in entry:
                inside_dict = {}
                inside_dict['date_reported'] = i[1]
                inside_dict['country'] = i[3]
                inside_dict['new_cases'] = i[5]
                inside_dict['cumulative_cases'] = i[6]
                inside_dict['new_deaths'] = i[7]
                inside_dict['cumulative_deaths'] = i[8]
                complete_list.append(inside_dict)
            one_less_list = complete_list[:-1]
            return one_less_list, complete_list  # first one is for representing on table, second one is for getting dates for prediction modal

        pk = kwargs['pk']
        for k, v in self.ids:
            if k == pk:
                country = v
        test_query = "SELECT * FROM pandemics.covid_world_who  WHERE country = '{}';".format(country)

        with connection.cursor() as cursor:
            cursor.execute(test_query)
            var = cursor.fetchall()
        data, for_dates = tuple_to_dict(var)

        line_graph_new_D_C = covid.country_daily_cases_line_graph(data)

        new_query = "SELECT date_reported, new_cases FROM pandemics.covid_world_who WHERE country='{}';".format(country)

        today_prediction, future = TS.prediction_model_counries(new_query)

        print(round(today_prediction, 2), future)

        new_data = copy.copy(for_dates)
        new_data.reverse()
        actual_date = datetime.strptime(new_data[0]['date_reported'], "%d/%m/%Y")
        actual_val = new_data[0]['new_cases']
        now = actual_date

        def convert_date_to_string(now):
            list_of_dates = []
            list_of_dates.append(now.strftime("%d/%m/%Y"))
            for i in range(1, 6):
                flag = now + timedelta(days=i)
                list_of_dates.append(flag.strftime("%d/%m/%Y"))
            return list_of_dates

        dates = convert_date_to_string(now)

        today = [{'now': dates[0], 'present': actual_val, 'future': int(float(future.iloc[0]))}]
        future_five = [{'now': dates[1], 'future': int(float(future.iloc[1]))},
                       {'now': dates[2] , 'future': int(float(future.iloc[2]))},
                       {'now': dates[3], 'future': int(float(future.iloc[3]))},
                       {'now': dates[4], 'future': int(float(future.iloc[4]))},
                       {'now': dates[5], 'future': int(float(future.iloc[5]))}]

        context = {'country_details': data,
                   'country': country,
                   'lin_graph_new_D_C': line_graph_new_D_C,
                   'prediction': round(today_prediction, 2),
                   'future_five': future_five,
                   'today': today
                   }

        if request.method == 'GET':
            name = request.GET.get('name-user', False)
            email = request.GET.get('email-id', False)

            if name is not False and email is not False:
                cols = ['Date', 'Country', 'New Cases', 'Total Cases', 'New Deaths', 'Total Deaths']
                filename = 'Covid/static/Covid/Mailing/{}.csv'.format(country)
                var = new_data

                with open(filename, 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(cols)
                    for i in var:
                        writer.writerow((i['date_reported'], i['country'], i['new_cases'], i['cumulative_cases'], i['new_deaths'],
                                         i['cumulative_deaths']))

                emaliing.email(name=name,
                               mailid=email,
                               subject="Latest Covid Stats of {} as of {}".format(country, now),
                               file_path=filename)

        return render(request, 'Covid/each_country.html', context)


class IndianStates(View):
    indian_states = ["Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
                     "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli", "Delhi", "Goa",
                     "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala",
                     "Ladakh", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
                     "Odisha", "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
                     "Uttar Pradesh", "Uttarakhand", "West Bengal"]

    def get(self, request):
        def latest_data(entry):
            list_of_dict = []
            for i in entry:
                tuple_to_dict = {}
                tuple_to_dict['date'] = i[0]
                tuple_to_dict['state_unionT'] = i[1]
                tuple_to_dict['cured'] = i[2]
                tuple_to_dict['death'] = i[3]
                tuple_to_dict['confirmed_total'] = i[4]
                tuple_to_dict['active_cases'] = int(i[4]) - (int(i[2]) + int(i[3]))
                list_of_dict.append(tuple_to_dict)

            latest_date = sorted(list_of_dict, key=lambda i: datetime.strptime(i['date'], '%d/%m/%Y'), reverse=True)
            return latest_date[0]  # this is latest date which will have total cases till date

        all_qs = []
        for i in range(len(self.indian_states)):
            with connection.cursor() as cursor:
                cursor.execute("SELECT ci.date, ci.state_unionT, ci.cured, ci.death, ci.confirmed_total from "
                               "pandemics.covid_india ci where ci.state_unionT = %s", [self.indian_states[i]])
                var = cursor.fetchall()
                all_qs.append(latest_data(var))

        for i in range(len(self.indian_states)):
            all_qs[i]['no'] = i+1  # this is to assign sl.no for states

        stacked_bar_graph = covid.stacked_bar_graph_all(all_qs)

        india_map_total_cases = covid.total_cases_india_plotly(all_qs)

        context = {'states': all_qs,
                   'stacked_bar_graph': stacked_bar_graph,
                   'india_map_total_cases': india_map_total_cases,
                   'till_date': all_qs[20]['date']}

        if request.method == 'GET':
            name = request.GET.get('name-user', False)
            email = request.GET.get('email-id', False)
            if name is not False and email is not False:
                cols = ['Date', 'State/Union Territory', 'Cured', 'Death', 'Total Cases', 'Active Cases']
                filename = 'Covid/static/Covid/Mailing/IndiaLatest.csv'
                var = all_qs

                with open(filename, 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(cols)
                    for i in var:
                        writer.writerow((i['date'], i['state_unionT'], i['cured'], i['death'], i['confirmed_total'],
                                         i['active_cases']))

                emaliing.email(name=name,
                               mailid=email,
                               subject="Latest Covid Stats of {} as of {}".format("India", all_qs[20]['date']),
                               file_path=filename)

        return render(request, 'Covid/indian_states.html', context)


class IndiaDetails(View):
    indian_states = ["Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
                     "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli", "Delhi", "Goa",
                     "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala",
                     "Ladakh", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
                     "Odisha", "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
                     "Uttar Pradesh", "Uttarakhand", "West Bengal"]

    def get(self, request, *args, **kwargs):

        pk = kwargs['pk']
        state = self.indian_states[pk-1]
        with connection.cursor() as cursor:
            cursor.execute("CALL join_stats_testing(%s);", [state])
            joined_data = cursor.fetchall()

        def sort_context(entry):

            return sorted(entry, key=lambda i: datetime.strptime(i['date'], '%d/%m/%Y'))

        def tuple_to_dict(entry):
            changed_joined = []
            for i in entry:
                inner_dict = {}
                inner_dict['date'] = i[0]
                inner_dict['state_unionT'] = state
                inner_dict['cured'] = i[2]
                inner_dict['death'] = i[3]
                inner_dict['total_cases'] = i[4]
                inner_dict['total_samples'] = i[5]
                inner_dict['positive'] = i[6]
                inner_dict['negative'] = i[7]
                changed_joined.append(inner_dict)
            return changed_joined

        changed_joined = tuple_to_dict(joined_data)

        joined_data = sort_context(changed_joined)
        for_dates = copy.copy(joined_data)
        print(for_dates)
        joined_data = joined_data[:-1]



        today_prediction, future = TS.prediction_model_states(joined_data, for_dates[-1]['total_cases'], for_dates[-1]['date'])


        print(round(today_prediction, 2), future)  # here future will be a pandas series so we hv to process it before rendering it to html page

        new_data = copy.copy(for_dates)
        new_data.reverse()
        actual_date = datetime.strptime(new_data[0]['date'], "%d/%m/%Y")
        actual_val = new_data[0]['total_cases']
        now = actual_date

        def convert_date_to_string(now):
            list_of_dates = []
            list_of_dates.append(now.strftime("%d/%m/%Y"))
            for i in range(1, 6):
                flag = now + timedelta(days=i)
                list_of_dates.append(flag.strftime("%d/%m/%Y"))
            return list_of_dates

        dates = convert_date_to_string(now)

        today = [{'now': dates[0], 'present': actual_val,
                  'future': int(float(future.iloc[0]))}]  # for present day's prediction
        future_five = [{'now': dates[1], 'future': int(float(future.iloc[1]))},
                       {'now': dates[2], 'future': int(float(future.iloc[2]))},
                       {'now': dates[3], 'future': int(float(future.iloc[3]))},
                       {'now': dates[4], 'future': int(float(future.iloc[4]))},
                       {'now': dates[5], 'future': int(float(future.iloc[5]))}]

        cases_line_graph = covid.state_graph_dates_cases(joined_data)

        context = {'india_joined': joined_data,
                   'state': state,
                   'cases_line_graph': cases_line_graph,
                   'prediction': round(today_prediction, 2),
                   'future_five': future_five,
                   'today': today
                   }

        if request.method == 'GET':
            name = request.GET.get('name-user', False)
            email = request.GET.get('email-id', False)
            if name is not False and email is not False:
                cols = ['Date', 'State/Union Territory', 'Cured', 'Death', 'Total Cases', 'Total Samples', 'Positive', 'Negative']
                filename = 'Covid/static/Covid/Mailing/{}.csv'.format(state)
                var = for_dates
                with open(filename, 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(cols)
                    for i in var:
                        writer.writerow((i['date'], i['state_unionT'], i['cured'], i['death'], i['total_cases'],
                                         i['total_samples'], i['positive'], i['negative']))

                emaliing.email(name=name,
                               mailid=email,
                               subject="Daily Covid Stats of {}".format(state),
                               file_path=filename)

        return render(request, 'Covid/covid_india_details.html', context)

