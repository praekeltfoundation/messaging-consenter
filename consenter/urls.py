from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path(
        "success/",
        TemplateView.as_view(template_name="consenter/success.html"),
        name="success",
    ),
    path("<str:user_uuid>/", views.ConsentView.as_view(), name="consent"),
]
