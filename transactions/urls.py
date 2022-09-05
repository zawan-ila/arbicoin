from django.urls import path
from transactions.views import TransactionHashView, TransactionIdView, UnconfirmedTransactionView, TransactionsCountView, AllTransactionsView


urlpatterns = [
    path('unconfirmed/', UnconfirmedTransactionView.as_view()),

    path('hash/<str:hash>/', TransactionHashView.as_view()),

    path('id/<int:pk>/', TransactionIdView.as_view()),

    path('length/', TransactionsCountView.as_view()),

    path('all/', AllTransactionsView.as_view()),
]
