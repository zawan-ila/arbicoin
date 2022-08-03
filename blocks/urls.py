from django.urls import path

from .views import BlockViewApi

urlpatterns = [
    path('<int:pk>/', BlockViewApi.as_view()),

]