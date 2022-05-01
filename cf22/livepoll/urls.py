from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_home, name='redirect_home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('devlog/', views.devlog, name='devlog'),
    path('polls/', views.polls, name='polls'),
    path('new_poll/', views.new_poll, name='new_poll'),
    path('new_answer/<int:poll_ID>/', views.new_answer, name='new_answer'),
    path('polls/<int:poll_ID>/', views.question, name='question'),
    path('polls/<int:poll_ID>/vote/', views.vote, name='vote'),
    path('polls/<int:poll_ID>/live/', views.live, name='live'),
    path('get_data/', views.get_data, name='get_data'),
    path('create-account/', views.register, name='create_account'),
    path('profile/', views.profile, name='profile'),
]
