from django.shortcuts import render
from account.models import *
from account.serializers import *
from rest_framework.response import Response
from rest_framework import (filters, generics, pagination, permissions, status,
                            views)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class WalletView(generics.ListCreateAPIView):
    serializer_class = WalletSerializer
    queryset = WalletAccount.objects.all()
    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response({"Status": status.HTTP_201_CREATED,
                             "Message": "Wallet Initialized Successfully"})
        return Response({"Status": status.HTTP_400_BAD_REQUEST,
                         "Message": serializer.errors})


class WalletEnableView(generics.ListCreateAPIView):
    serializer_class = WalletSerializer
    queryset = WalletAccount.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        data_queryset = WalletAccount.objects.filter(user_id=self.request.user.id)
        print(data_queryset[0].status)
        if not data_queryset:
            return WalletAccount.objects.none()
        elif not data_queryset[0].status:
            return WalletAccount.objects.none()
        else:
            return data_queryset

    def post(self, request, format=None):
        try:
            user_account = WalletAccount.objects.get(user_id=request.user.id)
            if not user_account.status:
                user_account.status = True
                user_account.save()
                return Response({"Status": status.HTTP_201_CREATED,
                                 "Message": "Status is Enabled"})
            else:
                return Response({"Status": status.HTTP_400_BAD_REQUEST,
                                 "Message": "Wallet is Already Enabled"})
        except:
            return Response({"Status": status.HTTP_400_BAD_REQUEST,
                             "Message": "Please Initialize Wallet"})

    def patch(self, request, format=None):
        if request.data['is_disabled']:
            WalletAccount.objects.filter(user_id=request.user.id).update(status=False)
            return Response({'Status': status.HTTP_400_BAD_REQUEST,
                             'Message': "Successfully Disabled"})
        else:
            return Response({'Status': status.HTTP_400_BAD_REQUEST,
                             'Message': "Already Disabled"})


class DepositView(generics.ListCreateAPIView):
    serializer_class = DepositSerializer
    queryset = Deposit.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        wallet_account = WalletAccount.objects.get(user_id=request.user.id)
        request.data['deposited_by'] = wallet_account.owned_by
        request.data['status'] = True
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            wallet_account.balance = wallet_account.balance + request.data['amount']
            wallet_account.save()
            return Response({"Status": status.HTTP_201_CREATED,
                             "Message": "Amount Deposited"})
        return Response({"Status": status.HTTP_400_BAD_REQUEST,
                         "Message": serializer.errors})


class WithdrawView(generics.ListCreateAPIView):
    serializer_class = WithdrawSerializer
    queryset = Withdraw.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        wallet_account = WalletAccount.objects.get(user_id=request.user.id)
        request.data['withdrawn_by'] = wallet_account.owned_by
        request.data['status'] = True
        if wallet_account.balance < request.data['amount']:
            return Response({"Status": status.HTTP_400_BAD_REQUEST,
                             "Message": "Insufficient Balance"})
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            wallet_account.balance = wallet_account.balance - request.data['amount']
            wallet_account.save()
            return Response({"Status": status.HTTP_201_CREATED,
                             "Message": "Amount Withdrawn Successfully"})
        return Response({"Status": status.HTTP_400_BAD_REQUEST,
                         "Message": serializer.errors})

