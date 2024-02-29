from django.contrib.auth.models import User
from django.db import models

class Bolim(models.Model):
    nomi=models.CharField(max_length=200)
    haqida=models.TextField()

    def __str__(self):
        return self.nomi


class Muallif(models.Model):
    ism=models.CharField(max_length=50)
    tirik=models.BooleanField(default=True)
    mamlakat=models.CharField(max_length=50)

    def __str__(self):
        return self.ism

class Kitob(models.Model):
    nomi=models.CharField(max_length=50)
    muallif=models.ForeignKey(Muallif, on_delete=models.CASCADE)
    yili=models.PositiveIntegerField()
    bolim=models.ForeignKey(Bolim, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    file=models.FileField(null=True, blank=True)
    def __str__(self):
        return self.nomi


