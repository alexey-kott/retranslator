from django.db import models


# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=40, null=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, null=True)
    phone = models.CharField(max_length=20)


class FilterWord(models.Model):
    word = models.TextField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Addressee(models.Model):
    username = models.CharField(max_length=40)
    source = models.ForeignKey(Account, on_delete=models.CASCADE)
