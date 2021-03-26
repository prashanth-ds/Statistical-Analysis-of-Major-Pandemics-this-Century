from django.shortcuts import render
from django.views.generic import View
from django.db import connection
from Ebola.Plots import ebola
from Ebola import emaliing


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
            cursor.execute("SELECT country, confirmed_cases, confirmed_deaths FROM pandemics.ebola_world"
                           " ORDER BY confirmed_cases DESC")
            var = cursor.fetchall()
            modified_data = latest_data(var)

        # stacked bar chart for deaths and confirmed cases
        stacked_bar_chart = ebola.stack_bar_chart(modified_data)

        # world map for total cases
        world_map_total_cases = ebola.total_cases_map(modified_data)

        context = {'EbolaData': modified_data, 'world_map_total_cases': world_map_total_cases,
                   'stacked_bar_chart': stacked_bar_chart}

        if request.method == 'GET':
            name = request.GET.get('name-user', False)  
            email = request.GET.get('email-id', False)

            if name is not False and email is not False:
                filename = 'Ebola/static/Ebola/Mailing/{}.csv'.format("WorldInfo")
                emaliing.email(name=name,
                               mailid=email,
                               subject="Ebola Stats of {}".format("World"),
                               file_path=filename)

        return render(request, 'Ebola/each_country.html', context)
