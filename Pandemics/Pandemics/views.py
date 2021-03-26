from Covid import updater, tasks
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import RedirectView


class UpdateView(RedirectView):
    updater.start()
    tasks.automating()
    url = reverse_lazy('main_page')


def main_page(request):
    return render(request, 'main.html')
