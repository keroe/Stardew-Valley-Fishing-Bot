from django.shortcuts import render

def index(request):
	return render(request, 'sign_in/index.html')

# Create your views here.
