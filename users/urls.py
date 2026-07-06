from django.urls import path
from . import views
urlpatterns = [
    # REGISTER
    path('register/', views.RegistrationView.as_view()),
    # LOGIN
    path('login/', views.LoginView.as_view()),
    # LOGOUT
    path('logout/', views.LogoutView.as_view()),
    # DASHBOARD
]