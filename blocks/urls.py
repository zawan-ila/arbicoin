from django.urls import path

from .views import BlockHashView, BlockLatestView, AllBlocksView, ChainLengthView

urlpatterns = [
    path('all/', AllBlocksView.as_view()),
    path('latest/', BlockLatestView.as_view()),
    path('length/', ChainLengthView.as_view()),
    path('<str:hash>/', BlockHashView.as_view()),

]