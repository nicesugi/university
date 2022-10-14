from django.urls import path
from university import views


urlpatterns = [
    path('', views.SearchView.as_view()),
]