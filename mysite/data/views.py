from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from data.models import UserData
from data.forms import UserDataForm

import numpy as np

def data(request):
	return render(request, 'data/data_index.html')

def upload(request):
    submitted = ''
    file = ""
    score = None
    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)
        file = request.FILES['file']
        if form.is_valid() and (file.name == 'training_data.npy') and (file.size > 10 ):

            file = list(np.load(file))
            form.save()

            last_row = UserData.objects.latest('id')
            
            last_row.score = len(file)
            last_row.save()

            submitted = 'True'
             #'File submitted succesfully. Thank you :)'
            
        else:
            submitted = 'False' #"Your file was not submitted, maybe you are not logged in or your training data is unvalid."

    else:
        form = UserDataForm()

    return render(request, 'data/upload_index.html', {
        'form': form,
        'user': request.user,
        'submitted': submitted,
        'file': file,
        'score': score
    })

def ranking(request):
	return render(request, 'data/ranking_index.html')