from django.urls import path

from transactions.views import TransactionViewApi

urlpatterns = [
    path('<int:pk>/', TransactionViewApi.as_view())
]
