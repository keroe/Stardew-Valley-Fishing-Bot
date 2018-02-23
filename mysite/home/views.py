from django.shortcuts import render
from django.db.models import Sum

from data.models import UserData

def index(request):
	user_score = UserData.objects.filter(username=request.user.username).aggregate(Sum('score'))['score__sum']
	return render(request, 'home/index.html', {
        'user': request.user,
        'user_score': user_score,
    })

# Create your views here.
