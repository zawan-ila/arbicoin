from django.urls import path
from wallet.views import TransactionCreateApiView, WalletInfoView, WalletOwnView, UnspentOutputsView


urlpatterns = [
    path('post/', TransactionCreateApiView),
    path('own/', WalletOwnView.as_view()),
    path('unspent/<str:own_addr>/', UnspentOutputsView.as_view()),
    path('<str:own_addr>', WalletInfoView.as_view()),

]
