from django.urls import path

from .views import TransactionViewApi

urlpatterns = [
    path('<int:pk>/', TransactionViewApi.as_view())
]
