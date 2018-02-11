from django.shortcuts import render

def index(request):
	return render(request, 'personal/jumbotron-narrow/index.html')

def contact(request):
	return render(request, 'personal/basic.html',{'content':['If you would like to contact me, please email me.','ansetti7@gmail.com']})

# Create your views here.
