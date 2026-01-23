from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class ParentGuardian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=100)  
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.relationship} of {self.user.username}'