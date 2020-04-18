from django.urls import path
from . import views

from django.contrib import admin
from django.urls import include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import IndexView, Under_Construction_View, aboutNFA, UserChangeForm
from .views import SignUpForm, SignUp, UserEdit, IndexView02, Location_CreateView
from .views import Location_UpdateView, Location_DeleteView, Location_ListView
from .views import Person_ListView, Person_UpdateView, Person_CreateView, Person_DeleteView
from .views import initTable, delete_TableRec, registDiet, Output1, Output2, Output3, Output4, Output_list, registPerson
from .views import CropSelect, registCropAvail, Trial_View, Diet_Plan1, update_profile

from django.contrib import admin
from django.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('trial/', Trial_View.as_view(), name='trial'),
  path('index01/', IndexView.as_view(), name='index01'),
  path('index02/', IndexView02.as_view(), name='index02'),
  path('construction/', Under_Construction_View.as_view(), name='construction'),
  path('aboutNFA/', aboutNFA.as_view(), name='aboutnfa'),
  path('SignUp/', SignUp.as_view(), name='signup'),
  path('UserEdit/<int:pk>/', UserEdit.as_view(), name='useredit'),
  path('login/', auth_views.LoginView.as_view(template_name='myApp/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('update_profile/', views.update_profile, name='update_profile'),
  path('Location/create/', Location_CreateView.as_view(), name='Location_create'),
  path('Location/update/<int:pk>/', Location_UpdateView.as_view(), name='Location_update'),
  path('Location/delete/<int:pk>/', Location_DeleteView.as_view(), name='Location_delete'),
  path('Location/list/', Location_ListView.as_view(), name='Location_list'),
  path('crop_select/<int:myLocation>/', CropSelect.as_view(), name='crop_select'),
  path('registCropAvail/', views.registCropAvail, name='regist_crop_avail'),
  path('person/list/<int:myLocation>/<int:page>/', Person_ListView.as_view(), name='person_list'),
  path('person/create/<int:myLocation>/<int:mytarget_scope>/', Person_CreateView.as_view(), name='person_create'),
  path('person/update/<int:myLocation>/<int:pk><int:mytarget_scope>/', Person_UpdateView.as_view(), name='person_update'),
  path('person/delete/<int:myLocation>/<int:pk>/<int:mytarget_scope>/', Person_DeleteView.as_view(), name='person_delete'),
  path('registPerson/', views.registPerson, name='regist_person'),
  path('Diet1/<int:myLocation>/', Diet_Plan1.as_view(), name='diet1'),
  path('registDiet/', views.registDiet, name='regist_diet'),
  path('delete_TableRec/<str:tblName>/', views.delete_TableRec, name='delete_TableRec'),
  path('initTable/', initTable.as_view(), name='initTable'),
  path('Output1/<int:myLocation>/', Output1.as_view(), name='output1'),
  path('Output2/<int:myLocation>/', Output2.as_view(), name='output2'),
  path('Output3/<int:myLocation>/', Output3.as_view(), name='output3'),
  path('Output4/<int:myLocation>/', Output4.as_view(), name='output4'),
  path('Output_list/<int:myLocation>/', Output_list.as_view(), name='output_list'),
]
