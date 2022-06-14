from django.urls import path

from . import views
from.views import *

urlpatterns = [
    # path("", views.Import_csv),
    path("", FileFieldFormView.as_view()),
]