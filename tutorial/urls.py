from django.conf.urls import url
from django.urls import path
from tutorial import views

app_name = 'tutorial'
urlpatterns = [
    # The home view ('/tutorial/')
    path('', views.home, name='home'),
    # Explicit home ('/tutorial/home/')
    path('home/', views.home, name='home'),
    # Redirect to get token ('/tutorial/gettoken/')
    path('gettoken/', views.gettoken, name='gettoken'),
    
    path('mailing/', views.mailing, name='mailing'),
]
