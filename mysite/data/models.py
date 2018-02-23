from django.db import models


class UserData(models.Model):
	username = models.CharField(max_length=40)
	file = models.FileField(upload_to='userdata/')#upload_to='uploads/')
	#score = models.IntegerField()  Acho desnecessario pq len(data) já é o score
	uploaded_at = models.DateTimeField(auto_now_add=True)


# Create your models here.