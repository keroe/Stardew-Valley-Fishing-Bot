from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from data.models import UserData
from data.forms import UserDataForm

def data(request):
	return render(request, 'data/data_index.html')

def download(request):
	return render(request, 'data/download_index.html')

def upload(request):
    submitted = ''
    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            submitted = 'True' #'File submitted succesfully. Thank you :)'
            
        else:
            submitted = 'False' #"Your file was not submitted, maybe you are not logged in or your training data is unvalid."

    else:
        form = UserDataForm()

    return render(request, 'data/upload_index.html', {
        'form': form,
        'user': request.user,
        'submitted': submitted
    })

def ranking(request):
	return render(request, 'data/ranking_index.html')