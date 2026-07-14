from django.urls import path
from . import views

urlpatterns = [
    path("review/", views.review_resume, name="review_resume"),
]
