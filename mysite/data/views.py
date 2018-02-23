from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum

from data.models import UserData
from data.forms import UserDataForm

import numpy as np

def data(request):
    user_score = UserData.objects.filter(username=request.user.username).aggregate(Sum('score'))['score__sum']
    return render(request, 'data/data_index.html', {
        'user': request.user,
        'user_score': user_score
    })

def upload(request):
    submitted = ''
    debug = ''
    user_score = UserData.objects.filter(username=request.user.username).aggregate(Sum('score'))['score__sum']
    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)
        file = request.FILES['file']
        if form.is_valid() and (file.name == 'training_data.npy') and (file.size > 10 ):

            file = list(np.load(file))
            form.save()

            last_row = UserData.objects.latest('id')
            last_row.score = len(file)
            last_row.save()

            #total_frames = UserData.objects.aggregate(Sum('score'))["score__sum"]

            #user_score = UserData.objects.filter(username=request.user.username).aggregate(Sum('score'))['score__sum']
            #UsuarioModel = UserProfile.objects.get(user__username=UsuarioElegido)
            #total_score = UserData.objects.values('username').annotate(Sum('score'))

            #debug = total_frames

            submitted = 'True' #"File submitted succesfully. Thank you :)"

            return redirect('/data/ranking/upload')
            
        else:
            submitted = 'False' #"Your file was not submitted, maybe you are not logged in or your training data is unvalid."

    else:
        form = UserDataForm()

    return render(request, 'data/upload_index.html', {
        'form': form,
        'user': request.user,
        'user_score': user_score,
        'submitted': submitted,
        'debug': debug
    })

def ranking(request):
    user_score = UserData.objects.filter(username=request.user.username).aggregate(Sum('score'))['score__sum']
    total_score = UserData.objects.aggregate(Sum('score'))["score__sum"]
    return render(request, 'data/ranking_index.html', {
        'user': request.user,
        'user_score': user_score,
        'total_score': total_score
    })