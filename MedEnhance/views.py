from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"index.html")

def login(request):
    return render(request,"login.html")
def results(request):
    return render(request,"results.html")

def upload(request):
    return render(request,"upload.html")
