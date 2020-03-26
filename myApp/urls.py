from django.urls import path
from . import views

from django.contrib import admin
from django.urls import include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import IndexView, Under_Construction_View, aboutNFA, UserChangeForm
from .views import SignUpForm, SignUp, UserEdit, IndexView02, Location_CreateView
from .views import Location_UpdateView, Location_DeleteView, Location_ListView
from .views import CropSelect, registCropAvail

from django.contrib import admin
from django.urls import include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('index01/',  IndexView.as_view(), name='index01'),
    path('index02/',  IndexView02.as_view(), name='index02'),
    path('construction/',  Under_Construction_View.as_view(), name='construction'),
    path('aboutNFA/', aboutNFA.as_view(), name='aboutnfa'),
    path('SignUp/',  SignUp.as_view(), name='signup'),
    path('UserEdit/<int:pk>/',  UserEdit.as_view(), name='useredit'),
    path('login/', auth_views.LoginView.as_view(template_name='myApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('Location/create/', Location_CreateView.as_view(), name='Location_create'),
    path('Location/update/<int:pk>/', Location_UpdateView.as_view(), name='Location_update'),
    path('Location/delete/<int:pk>/', Location_DeleteView.as_view(), name='Location_delete'),
    path('Location/list/', Location_ListView.as_view(), name='Location_list'),
    path('crop_select/<int:myLocation>/',  CropSelect.as_view(), name='crop_select'),
    path('registCropAvail/', views.registCropAvail, name='regist_crop_avail'),

]
