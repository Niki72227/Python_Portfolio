from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history', views.history, name='history'),
    path('queries', views.queries, name='queries'),
    path('get-crypto-list/', views.get_crypto_list, name="get_crypto_list"),
    path('get-stock-list/', views.get_stock_list, name="get_stock_list"),
    path('get-ccy-list/', views.get_ccy_list, name="get_ccy_list"),
    path('get-crypto-price/', views.get_crypto_price, name="get_crypto_price"),
    path('get-stock-price/', views.get_stock_price, name="get_stock_price"),
    path('get-ccy-price/', views.get_ccy_price, name="get_ccy_price"),
    path('get-asset-list/', views.get_asset_list, name="get_asset_list"),
    path('get-asset-stats/', views.asset_stats, name="get_asset_stats"),

]