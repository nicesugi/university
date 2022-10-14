from django.urls import path
from university import views


urlpatterns = [
    path('', views.SearchView.as_view()),
    path('<university_id>/preference', views.RreferenceView.as_view()),
]