from django.urls import path
from . import views as main_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', main_views.home, name='home'),
    path('near-you', main_views.near_you, name='near-you'),
    path('404', main_views.error_404, name='404'),
    
    # path('donate', main_views.donate, name='donate'),
    # path('news', main_views.news, name='news'),
    # path('news-detail', main_views.news_detail, name='news-detail'),
    
]