from django.shortcuts import render

# Create your views here.

def about(request):
    return render(request, 'pages/about.html')


def index(request):
    return render(request, 'pages/index.html')