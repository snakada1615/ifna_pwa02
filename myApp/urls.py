from django.urls import path
from . import views
from .views import TestView, FCT_show, OfflineView

urlpatterns = [
    path('test/',  TestView.as_view(), name='test'),
    path('offline/',  OfflineView.as_view(), name='offline'),
    path('fct/<int:categ>/<int:order>/',  FCT_show.as_view(), name='FCT_show'),
]
