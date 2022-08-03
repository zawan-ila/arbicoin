from django.urls import path

from .views import TransactionHashView, TransactionViewApi, UnconfirmedTransactionView

urlpatterns = [
    path('unconfirmed/', UnconfirmedTransactionView.as_view()),

    path('<str:hash>/', TransactionHashView.as_view()),

]