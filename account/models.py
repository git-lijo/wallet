from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class WalletAccount(models.Model):
    id = models.AutoField(primary_key=True)
    owned_by = models.CharField(max_length=36, unique=True)
    status = models.BooleanField(default=False)
    enabled_at = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField(default=0)
    user_id = models.ForeignKey(User,
                                on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Deposit(models.Model):
    id = models.AutoField(primary_key=True)
    deposited_by = models.CharField(max_length=36)
    status = models.BooleanField(default=False)
    deposited_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    reference_id = models.CharField(max_length=36, unique=True)

    def __str__(self):
        return str(self.id)


class Withdraw(models.Model):
    id = models.AutoField(primary_key=True)
    withdrawn_by = models.CharField(max_length=36)
    status = models.BooleanField(default=False)
    withdrawn_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    reference_id = models.CharField(max_length=36, unique=True)

    def __str__(self):
        return str(self.id)
