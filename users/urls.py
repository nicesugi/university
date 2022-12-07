from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path
from users import views

urlpatterns = [
    path("", views.UserView.as_view()),
    path("login", TokenObtainPairView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
]
