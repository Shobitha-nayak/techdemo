from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/kpi/<str:ticker>/', views.api_kpi, name='api_kpi'),
    path('api/top-gainers-losers/', views.api_top_gainers_losers, name='api_top_gainers_losers'),
]
