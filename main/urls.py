from django.urls import path
from . import views as main_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('get-viacep/<str:cep>/', main_views.get_cep, name='get_cep'),
    path('', main_views.home, name='home'),
    path('donate', main_views.donate, name='donate'),
    path('news', main_views.news, name='news'),
    path('news-detail', main_views.news_detail, name='news-detail'),
    
]