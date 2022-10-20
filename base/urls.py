from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.homePage, name='home'),
    path('add/', views.addNote, name='add'),
    path('delete/', views.deleteNote, name='delete'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view(next_page='/')),
    path('register/', views.registerUser, name='register'),
]