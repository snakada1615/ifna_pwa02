from django.urls import path
from . import views
from .views import TestView, FCT_show

urlpatterns = [
    path('test/',  TestView.as_view(), name='test'),
    path('fct/<int:categ>/<int:order>/',  FCT_show.as_view(), name='FCT_show'),
]
