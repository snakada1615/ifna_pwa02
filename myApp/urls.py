from django.urls import path
from . import views
from .views import TestView

urlpatterns = [
    path('test/',  TestView.as_view(), name='test'),
]
