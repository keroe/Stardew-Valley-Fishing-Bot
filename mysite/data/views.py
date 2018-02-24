from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Count
from django.db.models import DateField, Case, F
from datetime import date, timedelta

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

    score_sum_by_user = UserData.objects.values('username').annotate(Sum('score'))
    #best_5 = all_users_score[0:5]
    score_sum_by_user = score_sum_by_user.values('username', 'score__sum')

    last_week = date.today()-timedelta(days=7)

    score_by_day = list(UserData.objects
    .filter(uploaded_at__gt=last_week)
    .extra(select={'day': 'date(uploaded_at)'})
    .values('day')
    .annotate(sum=Sum('score')))


    #Does not work: make it get data from 1 day and sum it all up, call it s1. Then get the data from the day before with "-timedelta(days=1)", sum it all up and call it s2...
    try:
        #d1 = score_by_day[0]["day"]
        s1 = score_by_day[0]["sum"]
    except:
        #d1 = 0
        s1 = 0

    try:
        #d2 = score_by_day[1]["day"]
        s2 = score_by_day[1]["sum"]
    except:
        #d2 = 0
        s2 = 0

    try:
        #d3 = score_by_day[2]["day"]
        s3 = score_by_day[2]["sum"]
    except:
        #d3 = 0
        s3 = 0

    try:
        #d4 = score_by_day[3]["day"]
        s4 = score_by_day[3]["sum"]
    except:
        #d4 = 0
        s4 = 0

    try:
        #d5 = score_by_day[4]["day"]
        s5 = score_by_day[4]["sum"]
    except:
        #d5 = 0
        s5 = 0

    try:
        #d6 = score_by_day[5]["day"]
        s6 = score_by_day[5]["sum"]
    except:
        #d6 = 0
        s6 = 0

    try:
        #d7 = score_by_day[6]["day"]
        s7 = score_by_day[6]["sum"]
    except:
        #d7 = 0
        s7 = 0

    total_score = UserData.objects.aggregate(Sum('score'))["score__sum"]

    return render(request, 'data/ranking_index.html', {
        'user': request.user,
        'user_score': user_score,
        'total_score': total_score,
        'score_sum_by_user': score_sum_by_user,
        'score_by_day': score_by_day,
        
        's1': s1,
        's2': s2,
        's3': s3,
        's4': s4,
        's5': s5,
        's6': s6,
        's7': s7,

        #'d1': d1,
        #'d2': d2,
        #'d3': d3,
        #'d4': d4,
        #'d5': d5,
        #'d6': d6,
        #'d7': d7

    })