# portfolio/urls.py
from django.urls import path
from . import views
from .views import register
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import analysis_view
urlpatterns = [
    path('wallet-balance/', views.wallet_balance_page, name='wallet_balance_page'),
    path('wallet/<str:wallet_address>/', views.wallet_balance, name='wallet_balance'),
    path('send-crypto/', views.send_crypto, name='send_crypto'),
    path('wallet/<str:wallet_address>/', views.wallet_balance, name='wallet_balance'),
    path('holdings/', views.holdings_list, name='holdings_list'),
    path('add-to-portfolio/', views.add_to_portfolio, name='add_to_portfolio'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('register/', register, name='register'),
    #path('logout/', views.user_logout, name='logout'),
    #path('logout/', LogoutView.as_view(next_page='loin'), name='logout'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('analysis/', analysis_view, name='analysis'),
    

]
