from django.shortcuts import render

# Create your views here.


def index(request):
    """Home page of web app"""

    return render(request, 'logs/index.html')
