from django.urls import path
from . import views
from knox import views as knox_views

urlpatterns = [
    path('login/', views.login_api),
    path('user/', views.get_user_data),
    path('register/', views.register_api),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
    path('QR/', views.get_QR),
    # path(r'^QR/guest/$', views.get_QR_guest),
    path('validate/', views.validate),
]