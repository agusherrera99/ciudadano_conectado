from django.shortcuts import render

# Create your views here.
def data_center(request):
    return render(request, 'data_center.html')