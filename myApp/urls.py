from django.urls import path
from . import views
from .views import TestView, FCT_show, OfflineView
from .views import Family_UpdateView, Family_DeleteView, Family_ListView, Family_CreateView
from .views import Person_UpdateView, Person_DeleteView, Person_ListView, Person_CreateView

urlpatterns = [
    path('test/',  TestView.as_view(), name='test'),
    path('off/', OfflineView.as_view(), name='off'),
    path('fct/<int:categ>/<int:order>/',  FCT_show.as_view(), name='FCT_show'),
    path('Family/list/',  Family_ListView.as_view(), name='Family_index'),
    path('Family/create/', Family_CreateView.as_view(), name='Family_create'),
    path('Family/update/<int:pk>/', Family_UpdateView.as_view(), name='Family_update'),
    path('Family/delete/<int:pk>/', Family_DeleteView.as_view(), name='Family_delete'),
    path('person/list/<int:familyid>',  Person_ListView.as_view(), name='person_list'),
    path('person/create/<int:familyid>/', Person_CreateView.as_view(), name='person_create'),
    path('person/update/<int:familyid>/<int:pk>/', Person_UpdateView.as_view(), name='person_update'),
    path('person/delete/<int:familyid>/<int:pk>/', Person_DeleteView.as_view(), name='person_delete'),
]
