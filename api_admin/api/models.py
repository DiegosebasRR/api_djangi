from django.db import models

# Create your models here.
#python manage.py inspectdb ejecutar si quieres los modelos de la base de datos
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=25)
    role = models.CharField(max_length=15)
    avatar = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'users'  

