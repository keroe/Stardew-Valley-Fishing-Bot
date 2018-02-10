from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	
	return render(request, 'SDFBDownloads/home.html')

# Create your views here.
