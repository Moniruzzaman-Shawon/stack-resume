from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path("api/", include("resume_review.urls")),
    re_path(r"^(?!api/).*$", TemplateView.as_view(template_name="index.html"), name="frontend"),
]
