from django.urls import path
from . import views
from .views import TestView, FCT_show, OfflineView, Family_ListView, Family_CreateView
from .views import Family_UpdateView, Family_DeleteView

urlpatterns = [
    path('test/',  TestView.as_view(), name='test'),
    path('off/', OfflineView.as_view(), name='off'),
    path('fct/<int:categ>/<int:order>/',  FCT_show.as_view(), name='FCT_show'),
    path('Family/list/',  Family_ListView.as_view(), name='Family_index'),
    path('Family/create/', Family_CreateView.as_view(), name='Family_create'),
    path('Family/update/<int:pk>/', Family_UpdateView.as_view(), name='Family_update'),
    path('Family/delete/<int:pk>/', Family_DeleteView.as_view(), name='Family_delete'),
]
