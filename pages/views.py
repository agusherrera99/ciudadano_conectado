from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'

@login_required
def panel(request):
    return render(request, 'panel.html')