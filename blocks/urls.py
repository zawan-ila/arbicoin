from django.urls import path
from blocks.views import BlockHashView, BlockLatestView, AllBlocksView, ChainLengthView, BlockIdView


urlpatterns = [
    path('all/', AllBlocksView.as_view()),
    path('latest/', BlockLatestView.as_view()),
    path('length/', ChainLengthView.as_view()),
    path('hash/<str:hash>/', BlockHashView.as_view()),
    path('id/<int:pk>/', BlockIdView.as_view()),

]
