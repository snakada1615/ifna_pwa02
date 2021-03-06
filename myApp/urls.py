from django.urls import path
from . import views
from .views import TestView, FCT_show, OfflineView
from .views import Family_UpdateView, Family_DeleteView, Family_ListView, Family_CreateView
from .views import Person_UpdateView, Person_DeleteView, Person_ListView, Person_CreateView
from .views import Crop_UpdateView, Crop_DeleteView, Crop_ListView, Crop_CreateView
from .views import WhoamI_View, Usage_View, TestOfflineView, off_FCT_view, off_Family_ListView
from .views import Trial_View, off_Family_CreateView, FCTdatable_View, Under_Construction_View
from .views import Crop_Feas_View, Crop_Calendar_View, FamilyFiltered_ListView

from django.contrib import admin
from django.urls import include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('result/<int:familyid>/',  Crop_Feas_View.as_view(), name='result'),
    path('trial/',  Trial_View.as_view(), name='trial'),
    path('test/',  TestView.as_view(), name='test'),
    path('offline/', TestOfflineView.as_view(), name='offline'),
    path('offline/fct/<int:categ>/<int:order>/',  off_FCT_view.as_view(), name='off_FCT_view'),
    path('offline/Family/list/', off_Family_ListView.as_view(), name='off_family_list'),
    path('offline/Family/create/', off_Family_CreateView.as_view(), name='off_family_create'),
    path('who/',  WhoamI_View.as_view(), name='who'),
    path('usage/',  Usage_View.as_view(), name='usage'),
    path('construction/',  Under_Construction_View.as_view(), name='construction'),
    path('fct/<int:categ>/<int:order>/',  FCT_show.as_view(), name='FCT_show'),
    path('FCTdata/<int:familyid>/<str:items>/',  FCTdatable_View.as_view(), name='fctdata'),
    path('Family/list/', Family_ListView.as_view(), name='Family_index'),
    path('Family/list/filter/', FamilyFiltered_ListView.as_view(), name='Family_filter'),
    path('Family/create/<int:pk>/', Family_CreateView.as_view(), name='Family_create'),
    path('Family/update/<int:pk>/', Family_UpdateView.as_view(), name='Family_update'),
    path('Family/delete/<int:pk>/', Family_DeleteView.as_view(), name='Family_delete'),
    path('person/list/<int:familyid>/',  Person_ListView.as_view(), name='person_list'),
    path('person/create/<int:familyid>/', Person_CreateView.as_view(), name='person_create'),
    path('person/update/<int:familyid>/<int:pk>/', Person_UpdateView.as_view(), name='person_update'),
    path('person/delete/<int:familyid>/<int:pk>/', Person_DeleteView.as_view(), name='person_delete'),
    path('crop/list/<int:familyid>/',  Crop_ListView.as_view(), name='crop_list'),
    path('crop/create/<int:familyid>/', Crop_CreateView.as_view(), name='crop_create'),
    path('crop/update/<int:familyid>/<int:pk>/', Crop_UpdateView.as_view(), name='crop_update'),
    path('crop/delete/<int:familyid>/<int:pk>/', Crop_DeleteView.as_view(), name='crop_delete'),
    path('crop/calendar/<int:familyid>/<int:pk>/<str:items>/',  Crop_Calendar_View.as_view(), name='calendar'),
    path('getNFA/<int:store_id>/<int:familyid>/',  views.getNFA, name='getnfa'),
    path('registCalendar/<int:familyid>/<int:pk>/<str:itemstr>/',  views.registCalendar, name='registcalendar'),
    path('registCrops/<int:familyid>/<str:items>/',  views.registCrops, name='registcrops'),
    path('funcTest/',  views.funcTest, name='funcTest'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='myApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('SetCal/',  views.SetCal, name='setcal'),

]
