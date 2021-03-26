from django.shortcuts import render
from django.views.generic import View
from django.db import connection
from H1N1.Plots import h1n1
from H1N1 import emaliing
# Create your views here.


class EachCountry(View):
    def get(self, request):

        def latest_data(entry):
            qs = []
            count = 0
            for i in entry:
                list_if_dict = {}
                count = count + 1
                list_if_dict['id'] = count
                list_if_dict['country'] = i[0]
                list_if_dict['total_cases'] = i[1]
                list_if_dict['total_deaths'] = i[2]
                qs.append(list_if_dict)
            return qs

        with connection.cursor() as cursor:
            cursor.execute("SELECT country, confirmed_cases, confirmed_deaths FROM pandemics.h1n1_world"
                           " ORDER BY confirmed_cases DESC")
            var = cursor.fetchall()
            modified_data = latest_data(var)

        # bar chart for total cases and total deaths
        total_cases_bar_graph = h1n1.total_cases_bar(modified_data)
        total_deaths_bar_graph = h1n1.total_deaths_bar(modified_data)

        # world map for total cases
        total_cases_world_map = h1n1.total_cases_world_map(modified_data)

        context = {'H1N1Data': modified_data,
                   'total_cases_world_map': total_cases_world_map,
                   'total_cases_bar_graph': total_cases_bar_graph,
                   'total_deaths_bar_graph': total_deaths_bar_graph}

        if request.method == 'GET':
            name = request.GET.get('name-user', False)
            email = request.GET.get('email-id', False)
            if name is not False and email is not False:
                filename = 'H1N1/static/H1N1/Mailing/{}.csv'.format("WorldInfo")
                emaliing.email(name=name,
                               mailid=email,
                               subject="Ebola Stats of {}".format("World"),
                               file_path=filename)

        return render(request, 'H1N1/each_country.html', context)


