from django.shortcuts import render

def data(request):
	return render(request, 'data/data_index.html')

def download(request):
	return render(request, 'data/download_index.html')

def ranking(request):
	return render(request, 'data/ranking_index.html')
