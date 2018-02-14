from django.db import models


class UserData(models.Model):
	username = models.CharField(max_length=40)
	#score = models.IntegerField()  Acho desnecessario pq len(data) já é o score
	file = models.FileField(upload_to='userdata/')#upload_to='uploads/')
	uploaded_at = models.DateTimeField(auto_now_add=True)


# Create your models here.