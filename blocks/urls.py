from django.urls import path
from blocks.views import BlockViewApi


urlpatterns = [
    path('<int:pk>/', BlockViewApi.as_view()),
]
