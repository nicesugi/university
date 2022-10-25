from django.urls import path
from university import views


urlpatterns = [
    path("task", views.TaskView.as_view()),
    path("", views.SearchView.as_view()),
    path("<university_id>/preference", views.RreferenceView.as_view()),
]
