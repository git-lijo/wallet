from rest_framework import serializers
from account.models import *


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAccount
        fields = '__all__'


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = '__all__'
