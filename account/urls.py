from django.contrib import admin
from django.urls import path

from account import views

urlpatterns = [
    path('init', views.WalletView.as_view()),
    path('wallet', views.WalletEnableView.as_view()),
    path('wallet/deposits', views.DepositView.as_view()),
    path('wallet/withdraw', views.WithdrawView.as_view()),
]