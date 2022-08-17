from django.urls import path
from .views import TransactionCreateApiView, WalletInfoView, UnspentOutputsView


urlpatterns = [
    path('post/', TransactionCreateApiView.as_view()),
    path('unspent/<str:own_addr>/', UnspentOutputsView.as_view()),
    path('<str:own_addr>', WalletInfoView.as_view()),

]
