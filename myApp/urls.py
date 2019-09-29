from django.urls import path
from . import views
from .views import TestView, FCT_show, OfflineView, FamilyMember_List

urlpatterns = [
    path('test/',  TestView.as_view(), name='test'),
    path('off/', OfflineView.as_view(), name='off'),
    path('fct/<int:categ>/<int:order>/',  FCT_show.as_view(), name='FCT_show'),
    path('familymember/list/<int:familyid>',  FamilyMember_List.as_view(), name='familymember_list'),
]
