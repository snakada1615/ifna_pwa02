# to get all the models in myApp
from django.apps import apps
# from django.contrib import admin

# import messaging framework
# from django.contrib import messages

# import receiver
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.db.models import Max  # 集計関数の追加
# from django.db.models import Count, Case, When, IntegerField  # 集計関数の追加

# import re
from django.shortcuts import render, redirect
# from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
from django.http.response import JsonResponse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from .forms import LocationForm, Person_Form, UserForm, ProfileForm, Crop_Feas_Form, PersonListForm
from .forms import UserCreateForm, FCTForm, Crop_Name_Form, Crop_Feas2_Form

from .models import Location, Countries, Crop_National, Crop_SubNational, Crop_Feasibility_instant
from .models import FCT, DRI, Crop_Feasibility, Crop_Individual, Person, Pop, Crop_Name, Season, Crop_Individual_instant

# for user registration
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction

# logging用の設定
from logging import getLogger

logger = getLogger(__name__)

# python component
import json


class Trial_View(TemplateView):
  template_name = "myApp/_test.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation']).select_related('myDRI')
    context['nutrient_target'] = tmp_nut_group[0].nut_group

    tmp_nut_group1 = tmp_nut_group.filter(target_scope=1)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    if len(tmp_nut_group1) > 0:
      for tmp in tmp_nut_group1:
        tmp_e += tmp.myDRI.energy
        tmp_p += tmp.myDRI.protein
        tmp_v += tmp.myDRI.vita
        tmp_f += tmp.myDRI.fe
    context['dri_e1'] = tmp_e
    context['dri_p1'] = tmp_p
    context['dri_v1'] = tmp_v
    context['dri_f1'] = tmp_f

    tmp_nut_group2 = tmp_nut_group.filter(target_scope=2)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    if len(tmp_nut_group2) > 0:
      for tmp in tmp_nut_group2:
        tmp_e += tmp.myDRI.energy * tmp.target_pop
        tmp_p += tmp.myDRI.protein * tmp.target_pop
        tmp_v += tmp.myDRI.vita * tmp.target_pop
        tmp_f += tmp.myDRI.fe * tmp.target_pop
    context['dri_e2'] = tmp_e
    context['dri_p2'] = tmp_p
    context['dri_v2'] = tmp_v
    context['dri_f2'] = tmp_f

    tmp_nut_group3 = tmp_nut_group.filter(target_scope=3)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    if len(tmp_nut_group3) > 0:
      for tmp in tmp_nut_group3:
        tmp_e += tmp.myDRI.energy * tmp.target_pop
        tmp_p += tmp.myDRI.protein * tmp.target_pop
        tmp_v += tmp.myDRI.vita * tmp.target_pop
        tmp_f += tmp.myDRI.fe * tmp.target_pop
    context['dri_e3'] = tmp_e
    context['dri_p3'] = tmp_p
    context['dri_v3'] = tmp_v
    context['dri_f3'] = tmp_f

    ########### send number of season   ###########
    tmp = Season.objects.filter(myLocation=self.kwargs['myLocation'])[0]
    season_field = ['m1_season', 'm2_season', 'm3_season', 'm4_season', 'm5_season', 'm6_season',
                    'm7_season', 'm8_season', 'm9_season', 'm10_season', 'm11_season', 'm12_season']
    mydat = {}
    for myfield in season_field:
      tmpdat = str(getattr(tmp, myfield))
      mydat[myfield] = tmpdat
    logger.info(mydat)

    context["season"] = mydat

    #######################################################

    # send selected crop by community ######
    tmp01 = Crop_SubNational.objects.filter(myLocation_id=self.kwargs['myLocation']).select_related('myFCT')
    d = []
    for tmp02 in tmp01:
      dd = {}
      dd["selected_status"] = tmp02.selected_status
      dd["Food_grp"] = tmp02.myFCT.Food_grp
      dd["Food_name"] = tmp02.myFCT.Food_name
      dd["Energy"] = tmp02.myFCT.Energy
      dd["Protein"] = tmp02.myFCT.Protein
      dd["VITA_RAE"] = tmp02.myFCT.VITA_RAE
      dd["FE"] = tmp02.myFCT.FE
      dd["Weight"] = 0
      dd["food_item_id"] = tmp02.myFCT.food_item_id
      dd["portion_size"] = tmp02.myFCT.portion_size_init
      dd["count_buy"] = 0
      dd["count_prod"] = 0
      dd["portion_size"] = tmp02.myFCT.portion_size_init
      dd["m1"] = tmp02.m1_avail
      dd["m2"] = tmp02.m2_avail
      dd["m3"] = tmp02.m3_avail
      dd["m4"] = tmp02.m4_avail
      dd["m5"] = tmp02.m5_avail
      dd["m6"] = tmp02.m6_avail
      dd["m7"] = tmp02.m7_avail
      dd["m8"] = tmp02.m8_avail
      dd["m9"] = tmp02.m9_avail
      dd["m10"] = tmp02.m10_avail
      dd["m11"] = tmp02.m11_avail
      dd["m12"] = tmp02.m12_avail
      dd["myLocation"] = tmp02.myLocation_id
      dd["Fat"] = tmp02.myFCT.Fat
      dd["Carbohydrate"] = tmp02.myFCT.Carbohydrate
      d.append(dd)
    context["mylist_available"] = d

    # 作物のローカル名を送る
    tmp = Crop_Name._meta.get_fields()
    logger.info(tmp[2])
    tmp01 = Crop_Name.objects.filter(
      myCountryName=Location.objects.filter(id=self.kwargs['myLocation']).first().country)
    d = []
    for tmp02 in tmp01:
      dd = {}
      dd["Food_grp"] = tmp02.Food_grp
      dd["Food_name"] = tmp02.Food_name
      dd["food_item_id"] = tmp02.myFCT_id
      d.append(dd)

    context["mylist_local_name"] = d

    # 現在選択されている作物をDiet_plan_formに送る
    # --------------------create 16 Crop_individual-------------------------
    # if __name__ == '__main__':
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation']).select_related('myFCT')
    myRange = [101, 102, 103, 104, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 301, 302, 303, 304,
               305, 306, 307, 308, 309, 310, 311, 312]

    d = []
    for i in myRange:
      tmp02 = tmp01.filter(id_table=i)
      tmp02_list = tmp02.values_list('pk', flat=True)
      tmp02_list = list(tmp02_list)
      if len(tmp02_list) == 0:
        dd = {}
        dd["name"] = ''
        dd["Energy"] = ''
        dd["Protein"] = ''
        dd["VITA_RAE"] = ''
        dd["FE"] = ''
        dd["target_scope"] = ''
        dd["food_item_id"] = ''
        dd["portion_size"] = ''
        dd["total_weight"] = ''
        dd["count_prod"] = ''
        dd["count_buy"] = ''
        dd["month"] = ''
        dd["myLocation"] = ''
        dd["num_tbl"] = i
        dd["share_prod_buy"] = 5
        dd["Fat"] = ''
        dd["Carbohydrate"] = ''
        d.append(dd)
      else:
        for tmp03 in tmp02:
          dd = {}
          dd["name"] = tmp03.myFCT.Food_name
          dd["Energy"] = tmp03.myFCT.Energy
          dd["Protein"] = tmp03.myFCT.Protein
          dd["VITA_RAE"] = tmp03.myFCT.VITA_RAE
          dd["FE"] = tmp03.myFCT.FE
          dd["target_scope"] = tmp03.target_scope
          dd["food_item_id"] = tmp03.myFCT.food_item_id
          dd["portion_size"] = tmp03.portion_size
          dd["total_weight"] = tmp03.total_weight
          dd["count_prod"] = tmp03.count_prod
          dd["count_buy"] = tmp03.count_buy
          dd["month"] = tmp03.month
          dd["myLocation"] = tmp03.myLocation_id
          dd["num_tbl"] = tmp03.id_table
          dd["share_prod_buy"] = tmp03.share_prod_buy
          dd["Fat"] = tmp03.myFCT.Fat
          dd["Carbohydrate"] = tmp03.myFCT.Carbohydrate
          d.append(dd)
    context["mylist_selected"] = d

    context['myuser'] = self.request.user

    tmp_Param = SetURL(400, self.request.user)
    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class IndexView(TemplateView):
  template_name = "myApp/index01.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user

    tmp_Param = SetURL(-1, self.request.user)
    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context

class Index10(TemplateView):
  template_name = "myApp/index10.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['nav_link1'] = ''
    context['nav_text1'] = ''
    context['nav_link2'] = ''
    context['nav_text2'] = 'NFA tool demo. version'
    context['nav_link3'] = ''
    context['nav_text3'] = ''
    context["mark_text"] = 'This is quick trial mode of NFA tool'
    context["stepid"] = -10

    return context


class Under_Construction_View(TemplateView):
  template_name = "myApp/under_construction.html"


class aboutNFA(TemplateView):
  template_name = "myApp/whatisNFA.html"


class IndexView02(LoginRequiredMixin, TemplateView):  # todo myCountyNameの設定がうまくいかない
  template_name = "myApp/index02.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    keys_all = self.request.user.profile
    if len(Location.objects.filter(id=keys_all.myLocation)) == 0:
      myCountry = 'none'
    else:
      myCountry = Location.objects.filter(id=keys_all.myLocation).first().country

    data = {
      'myLocation': keys_all.myLocation,
      'myCrop': keys_all.myCrop,
      'myTarget': keys_all.myTarget,
      'myDiet': keys_all.myDiet,
      'myCountryName': myCountry
    }
    json_str = json.dumps(data)

    tmp_Param = SetURL(0, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    context['myParam'] = json_str
    context['myuser'] = self.request.user

    return context


class Location_ListView(LoginRequiredMixin, ListView):
  model = Location
  context_object_name = "mylist"
  template_name = 'myApp/Location_list.html'
  num_loc = 0

  def get_queryset(self):
    queryset = super().get_queryset().filter(created_by=self.request.user)
    self.num_loc = queryset.count()
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    context['myuser_id'] = self.request.user.id
    context['myLocation'] = self.request.user.profile.myLocation

    tmp_Param = SetURL(100, self.request.user)
    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    context['count_loc'] = self.num_loc
    logger.info("self.num_loc")
    logger.info(self.num_loc)

    return context


@transaction.atomic
def create_user_profile(request):
  # global profile_form
  if request.method == 'POST':
    user_form = UserCreateForm(request.POST)
    profile_form = ProfileForm(request.POST)
    if user_form.is_valid():  # and profile_form.is_valid():
      myuser = user_form.save()
      profile_form = ProfileForm(request.POST, instance=myuser.profile)
      profile_form.save()
      logger.error('新ユーザー' + myuser.username + 'が作成されました')

      login(request, myuser)  # 認証

      return redirect('index01')
    else:
      logger.info('新ユーザー登録に失敗しました')
  else:
    user_form = UserCreateForm()
    profile_form = ProfileForm()
    logger.info('ユーザー情報を作成します')
  return render(request, 'myApp/profile.html', {
    'is_register': True,
    'user_form': user_form,
    'profile_form': profile_form
  })


@login_required
@transaction.atomic
def update_profile(request):
  if request.method == 'POST':
    user_form = UserForm(request.POST, instance=request.user)
    profile_form = ProfileForm(request.POST, instance=request.user.profile)
    if user_form.is_valid() and profile_form.is_valid():
      myuser = user_form.save()
      profile_form.save()
      logger.info('ユーザー(' + myuser.username + ')が更新されました')
      return redirect('index01')
    else:
      logger.error('新ユーザー登録に失敗しました')
  else:
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    logger.info('ユーザー情報(' + request.user.username + ')を更新します')
  return render(request, 'myApp/profile.html', {
    'is_register': False,
    'myuser': request.user,
    'user_form': user_form,
    'profile_form': profile_form
  })


class Location_DeleteView(LoginRequiredMixin, DeleteView):  # todo これをmodal dialogueにする,削除時のmyStatusへの反映
  model = Location
  template_name = 'myApp/Location_confirm_delete.html'
  success_url = reverse_lazy('Location_list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    return context


class Location_CreateView(LoginRequiredMixin, CreateView):
  model = Location
  form_class = LocationForm
  template_name = 'myApp/Location_form.html'
  success_url = reverse_lazy('Location_list')

  def form_invalid(self, form):
    res = super().form_invalid(form)
    res.status_code = 400
    return res

  def form_valid(self, form):
    form.instance.myCountry = Countries.objects.filter(
      GID_3=form.instance.community).first()
    form.instance.AEZ_id = form.instance.myCountry.AEZ_id
    form.instance.created_by = User.objects.get(id=self.request.user.id)
    return super(Location_CreateView, self).form_valid(form)

  def get_context_data(self, **kwargs):
    data = Countries.objects.all()
    context = super().get_context_data(**kwargs)
    context['countries'] = serializers.serialize('json', data)
    if self.request.method == 'POST':
      param_request = self.request.POST.dict()
      context['country_selected'] = param_request['country'] if 'country' in param_request else ''
      context['region_selected'] = param_request['region'] if 'region' in param_request else ''
      context['province_selected'] = param_request['province'] if 'province' in param_request else ''
      context['community_selected'] = param_request['community'] if 'community' in param_request else ''
    else:
      context['country_selected'] = ''
      context['region_selected'] = ''
      context['province_selected'] = ''
      context['community_selected'] = ''
    context['myuser'] = self.request.user

    tmp_Param = SetURL(101, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class Location_UpdateView(LoginRequiredMixin, UpdateView):
  model = Location
  form_class = LocationForm
  template_name = 'myApp/Location_form.html'
  success_url = reverse_lazy('Location_list')

  def get_context_data(self, **kwargs):
    data = Countries.objects.all()
    context = super().get_context_data(**kwargs)
    context['countries'] = serializers.serialize('json', data)
    myLocation = Location.objects.get(id=self.kwargs['pk'])
    context['country_selected'] = myLocation.country
    context['region_selected'] = myLocation.region
    context['province_selected'] = myLocation.province
    context['community_selected'] = myLocation.community
    context['myuser'] = self.request.user
    return context

  def form_invalid(self, form):
    res = super().form_invalid(form)
    res.status_code = 400
    return res

  def form_valid(self, form):
    form.instance.myCountry = Countries.objects.filter(
      GID_3=form.instance.community).first()
    form.instance.AEZ_id = form.instance.myCountry.AEZ_id
    form.instance.created_by = User.objects.get(id=self.request.user.id)
    return super(Location_UpdateView, self).form_valid(form)


@receiver(post_delete, sender=Location)
def Del_Crop_SubNational(sender, instance, **kwargs):
  if Crop_SubNational.objects.filter(myLocation_id=instance.pk):
    Crop_SubNational.objects.filter(myLocation_id=instance.pk).delete()
  logger.info("該当するCrop＿SubNationalを削除しました")
  if Person.objects.filter(myLocation_id=instance.pk):
    Person.objects.filter(myLocation_id=instance.pk).delete()
  logger.info("該当するPersonを削除しました")
  if Season.objects.filter(myLocation_id=instance.pk):
    Season.objects.filter(myLocation_id=instance.pk).delete()
  logger.info("該当するSeasonを削除しました")
  myUser = instance.created_by
  list_location = Location.objects.filter(created_by=myUser).all()
  key = myUser.profile
  key.myTarget = 0
  key.myCrop = 0
  key.myDiet = 0
  if len(list_location) > 0:
    key.myLocation = list_location[0].id
  else:
    key.myLocation = 0
  key.save()
  logger.info("Profileを更新しました")


@receiver(post_save, sender=Location)
def Init_Crop_SubNational(sender, instance, created, update_fields=None, **kwargs):
  # myProfileの設定----------------------------------
  myUser = instance.created_by
  myLocation = instance.pk
  key = myUser.profile
  key.myLocation = myLocation
  key.myTarget = 0
  key.myCrop = 0
  key.myDiet = 0
  key.save()
  logger.info("Profileを更新しました")

  nut_grp_list = ['child 0-23 month', 'child 24-59 month', 'child 6-9 yr', 'adolescent male', 'adolescent female',
                  'adult male', 'adult female', 'pregnant', 'lactating']

  # Crop_SubNationalの設定----------------------------------
  if not created:  # Updateの場合
    if update_fields:
      if 'province' in update_fields:
        logger.debug("ここまでOK")

        # -- delete existing dataset ------------------------
        Crop_SubNational.objects.filter(myLocation_id=myLocation).delete()
        logger.info("該当するCrop_SubNationalを削除しました")
        Person.objects.filter(myLocation_id=myLocation).delete()
        logger.info("該当するPersonを削除しました")
        Season.objects.filter(myLocation_id=myLocation).delete()
        logger.info("該当するSeasonを削除しました")

        # --------------------update Crop_SubNational-------------------------
        logger.info("これからCrop＿SubNationalを追加していきます")
        tmp_aez = Countries.objects.filter(GID_2=instance.province).first().AEZ_id
        instance.AEZ_id = tmp_aez
        tmp01 = Crop_National.objects.filter(AEZ_id=tmp_aez)
        if tmp01.count() != 0:
          logger.info("Crop＿Nationalの中に該当品目が存在しています")
          for tmp02 in tmp01:
            keys = {}
            keys['myLocation'] = Location.objects.get(id=instance.pk)
            keys['myFCT'] = FCT.objects.get(food_item_id=tmp02.myFCT.food_item_id)
            keys['selected_status'] = 0
            keys['created_by'] = User.objects.get(id=instance.created_by.id)
            p = Crop_SubNational.objects.create(**keys)
          logger.info("全ての該当品目をCrop_SubNationalに書き込みました!")

        # --------------------update Season-------------------------
        logger.info("これからSeasonの構成、初期値を追加していきます")
        Season.objects.create(
          myLocation=Location.objects.get(id=instance.pk),
          created_by=User.objects.get(id=instance.created_by.id),
        )
        logger.info("Seasonの書込み終了")

        # ---------------------
  else:  # 新規レコードの場合

    # --------------------update Crop_SubNational-------------------------
    tmp_aez = Countries.objects.filter(GID_2=instance.province).first().AEZ_id
    instance.AEZ_id = tmp_aez
    logger.info(tmp_aez)
    tmp01 = Crop_National.objects.filter(AEZ_id=tmp_aez)
    logger.info("これからCrop＿SubNationalを追加していきます")
    if tmp01.count() != 0:
      logger.info("Crop＿Nationalの中に該当品目が存在しています")
      for tmp02 in tmp01:
        keys = {}
        keys['myLocation'] = Location.objects.get(id=instance.pk)
        keys['myFCT'] = FCT.objects.get(food_item_id=tmp02.myFCT.food_item_id)
        keys['selected_status'] = 0
        keys['created_by'] = User.objects.get(id=instance.created_by.id)
        p = Crop_SubNational.objects.create(**keys)
      logger.info("全ての該当品目をCrop_SubNationalに書き込みました!")
    else:
      logger.info("Crop＿Nationalの中に該当品目が存在しません")
      tmp03 = FCT.objects.all()
      for tmp02 in tmp03:
        keys = {}
        keys['myLocation'] = Location.objects.get(id=instance.pk)
        keys['myFCT'] = tmp02
        keys['selected_status'] = 0
        keys['created_by'] = User.objects.get(id=instance.created_by.id)
        p = Crop_SubNational.objects.create(**keys)
      logger.info("全てのFCTをCrop_SubNationalに書き込みました!")

    logger.info("これからSeasonの構成、初期値を追加していきます")
    Season.objects.create(
      myLocation=Location.objects.get(id=instance.pk),
      created_by=User.objects.get(id=instance.created_by.id),
    )
    logger.info("Seasonの書込み終了")
    # ---------------------


class CropSelect(LoginRequiredMixin, TemplateView):  # Query数を削減
  template_name = "myApp/crop_available.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    # send filtered crop by AEZ ######
    myUser = self.request.user
    tmp01 = Crop_SubNational.objects.filter(myLocation_id=myUser.profile.myLocation).select_related('myFCT')

    d = []
    for tmp02 in tmp01:
      dd = {}
      dd["selected_status"] = tmp02.selected_status
      dd["Food_grp"] = tmp02.myFCT.Food_grp_unicef
      dd["Food_name"] = tmp02.myFCT.Food_name
      dd["food_item_id"] = tmp02.myFCT.food_item_id
      dd["En"] = tmp02.myFCT.Energy
      dd["Pr"] = tmp02.myFCT.Protein
      dd["Va"] = tmp02.myFCT.VITA_RAE
      dd["Fe"] = tmp02.myFCT.FE
      dd["m1"] = tmp02.m1_avail
      dd["m2"] = tmp02.m2_avail
      dd["m3"] = tmp02.m3_avail
      dd["m4"] = tmp02.m4_avail
      dd["m5"] = tmp02.m5_avail
      dd["m6"] = tmp02.m6_avail
      dd["m7"] = tmp02.m7_avail
      dd["m8"] = tmp02.m8_avail
      dd["m9"] = tmp02.m9_avail
      dd["m10"] = tmp02.m10_avail
      dd["m11"] = tmp02.m11_avail
      dd["m12"] = tmp02.m12_avail
      d.append(dd)
    context["dat_mycrop"] = d
    context['myuser'] = myUser

    # 作物のローカル名を送る
    tmp = Crop_Name._meta.get_fields()
    logger.info(tmp[2])
    tmp01 = Crop_Name.objects.filter(
      # myCountryName=Location.objects.filter(id=self.kwargs['myLocation']).first().country)
      myCountryName="ETH")  # 暫定的にエチオピアの物を利用
    d = []
    new_Food_grp = []
    for tmp02 in tmp01:
      dd = {}
      dd["Food_grp"] = tmp02.Food_grp
      dd["Food_name"] = tmp02.Food_name
      dd["food_item_id"] = tmp02.myFCT_id
      d.append(dd)
      tmp03 = tmp02.Food_grp
      if tmp03 not in new_Food_grp:
        new_Food_grp.append(tmp03)

    context["mylist_local_name"] = d
    context["mylist_Food_grp"] = new_Food_grp

    # 季節情報を送る
    tmp01 = Season.objects.filter(myLocation_id=myUser.profile.myLocation)
    d = []
    for tmp02 in tmp01:
      dd = {}
      dd["m1_season"] = tmp02.m1_season
      dd["m2_season"] = tmp02.m2_season
      dd["m3_season"] = tmp02.m3_season
      dd["m4_season"] = tmp02.m4_season
      dd["m5_season"] = tmp02.m5_season
      dd["m6_season"] = tmp02.m6_season
      dd["m7_season"] = tmp02.m7_season
      dd["m8_season"] = tmp02.m8_season
      dd["m9_season"] = tmp02.m9_season
      dd["m10_season"] = tmp02.m10_season
      dd["m11_season"] = tmp02.m11_season
      dd["m12_season"] = tmp02.m12_season
      dd["season_name1"] = tmp02.season_name1
      dd["season_name2"] = tmp02.season_name2
      dd["season_name3"] = tmp02.season_name3
      dd["season_name4"] = tmp02.season_name4
      d.append(dd)
    context["dat_season"] = d

    stepid = myUser.profile.stepid
    newstep = 0
    if int(stepid) <= 400:
      newstep = 300
    else:
      newstep = 600
    tmp_Param = SetURL(newstep, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


def registCropAvail(request):
  # json_str = request.body.decode("utf-8")
  json_data = json.loads(request.body)
  tmp_myLocation_id = 0
  tmp_newcrop_list = []

  dict_date_avaiable = {'selected_status': 0}
  for j in range(1, 13):
    dict_date_avaiable['m%d_avail' % (j)] = 0
  Crop_SubNational.objects.filter(myLocation_id=json_data['myLocation']).update(**dict_date_avaiable)

  logger.info('registCropAvail開始')
  for myrow in json_data['myJson']:
    newcrop = {}
    newcrop['myFCT'] = FCT.objects.get(food_item_id=myrow['myFCT_id'])
    newcrop['myLocation'] = Location.objects.get(id=myrow['myLocation'])
    newcrop['selected_status'] = myrow['selected_status']
    newcrop['created_by'] = request.user
    for j in range(1, 13):
      tmpM = myrow['m' + str(j)]
      if tmpM == '':
        tmpM = '0'
      newcrop['m' + str(j) + '_avail'] = tmpM

    logger.info('データ受信完了')
    logger.info(newcrop['selected_status'])

    tmp_myLocation_id = myrow['myLocation']  # 後で使う(part 2)
    tmp_newcrop_list.append(myrow['myFCT_id'])  # 後で使う(part 2)

    tmp = Crop_SubNational.objects.filter(myFCT_id=myrow['myFCT_id']).filter(
      myLocation_id=tmp_myLocation_id
    )
    p = tmp.update(**newcrop)

  # (part 2) delete non-selected records
  logger.info(tmp_newcrop_list)
  tmp = Crop_SubNational.objects.filter(myLocation_id=tmp_myLocation_id)
  logger.info('受信していない作物を選択リストから外します')
  for rec in tmp:
    if str(rec.myFCT.food_item_id) not in tmp_newcrop_list:
      logger.info(rec.myFCT.food_item_id)
      rec.selected_status = 0
      rec.save()

  # seasonの登録
  logger.info('season登録開始')
  for myrow in json_data['season']:
    logger.error(myrow['season_name1'])
    logger.error(myrow['season_count'])
    Season.objects.update_or_create(
      myLocation=Location.objects.get(id=myrow['myLocation']),
      defaults={
        'm1_season': myrow['m1'],
        'm2_season': myrow['m2'],
        'm3_season': myrow['m3'],
        'm4_season': myrow['m4'],
        'm5_season': myrow['m5'],
        'm6_season': myrow['m6'],
        'm7_season': myrow['m7'],
        'm8_season': myrow['m8'],
        'm9_season': myrow['m9'],
        'm10_season': myrow['m10'],
        'm11_season': myrow['m11'],
        'm12_season': myrow['m12'],
        'season_name1': myrow['season_name1'],
        'season_name2': myrow['season_name2'],
        'season_name3': myrow['season_name3'],
        'season_name4': myrow['season_name4'],
        'season_count': myrow['season_count'],
      }
    )

  # myStatusの設定
  key = request.user.profile
  key.myTarget = 0
  key.myCrop = 1
  key.myDiet = 0
  key.save()

  myURL = reverse_lazy('index02')  # crop_selectに戻れない場合はindex02
  try:
    myURL = reverse_lazy("crop_select",
                         kwargs={'myCountryName': Location.objects.filter(
                           id=request.user.profile.myLocation).first().country,
                                 'myLocation': int(request.user.profile.myLocation)})
  except:
    logger.error('無効な値を参照しています')

  return JsonResponse({
    'success': True,
    'url': myURL,
  })


class Person_ListView(LoginRequiredMixin, ListView):
  template_name = 'myApp/person_list.html'  # この行でテンプレート指定
  context_object_name = 'persons'
  model = Person

  def get_queryset(self):
    queryset = super().get_queryset().filter(
      myLocation=self.kwargs['myLocation'])
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    myLoc = Location.objects.get(id=self.kwargs['myLocation'])
    context['myLocation'] = myLoc
    context['myuser'] = self.request.user
    context['page'] = self.kwargs['page']

    myPop = Pop.objects.filter(GID_0=Location.objects.get(id=self.kwargs['myLocation']).country)
    dd = {}
    for myPop2 in myPop:
      myClass = myPop2.Age_class_id
      myShare = myPop2.share_Pop
      if myClass == 0:
        dd['class0'] = myShare
      elif myClass == 1:
        dd['class1'] = myShare
      elif myClass == 2:
        dd['class2'] = myShare
      elif myClass == 3:
        dd['class3'] = myShare - (myPop2.share_Preg + myPop2.share_BF)
        dd['class3_p'] = myPop2.share_Preg
        dd['class3_l'] = myPop2.share_BF
      elif myClass == 4:
        dd['class4'] = myShare
      elif myClass == 5:
        dd['class5'] = myShare - (myPop2.share_Preg + myPop2.share_BF)
        dd['class5_p'] = myPop2.share_Preg
        dd['class5_l'] = myPop2.share_BF
      elif myClass == 6:
        dd['class6'] = myShare

    context['myPop'] = dd
    context['myReturnURL'] = reverse_lazy('index01')

    myPerson = Person.objects.filter(myLocation=self.kwargs['myLocation'])
    dd1 = {}
    for myPerson02 in myPerson:
      nut_group = myPerson02.nut_group
      pop = myPerson02.target_pop
      if nut_group == 'child 0-23 month':
        dd1['class0'] = pop
      elif nut_group == 'child 24-59 month':
        dd1['class1'] = pop
      elif nut_group == 'child 6-9 yr':
        dd1['class2'] = pop
      elif nut_group == 'adolescent male':
        dd1['class3'] = pop
      elif nut_group == 'adolescent female':
        dd1['class4'] = pop
      elif nut_group == 'adult male':
        dd1['class5'] = pop
      elif nut_group == 'adult female':
        dd1['class6'] = pop
      elif nut_group == 'pregnant':
        dd1['class7'] = pop
      elif nut_group == 'lactating':
        dd1['class8'] = pop

    context['myCommunity'] = dd1

    if myLoc.country == 'ETH':  # エチオピア限定の暫定措置
      tmp_Param = SetURL(200, self.request.user)
    else:
      tmp_Param = SetURL(200, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class Person_UpdateView(LoginRequiredMixin, UpdateView):
  model = Person
  form_class = Person_Form
  template_name = 'myApp/person_form.html'

  def get_form_kwargs(self):
    """This method is what injects forms with their keyword
        arguments."""
    # grab the current set of form #kwargs
    kwargs = super(Person_UpdateView, self).get_form_kwargs()
    # Update the kwargs with the user_id
    kwargs['myLocation'] = self.kwargs['myLocation']
    return kwargs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    myLocation = self.kwargs['myLocation']
    mydata = Location.objects.get(id=myLocation)
    context['name'] = mydata
    context['myLocation'] = myLocation
    context["locations"] = Person.objects.filter(
      myLocation_id=myLocation)
    context['myuser'] = self.request.user
    context['mytarget_scope'] = self.kwargs['mytarget_scope']
    return context

  def get_success_url(self, **kwargs):
    return reverse_lazy('person_list',
                        kwargs={'myLocation': self.kwargs['myLocation'], 'page': self.kwargs['mytarget_scope']})

  def form_valid(self, form):
    self.object = form.save()
    form.instance.myDRI = DRI.objects.filter(
      nut_group=form.instance.nut_group).first()
    # form.instance.target_scope = self.kwargs['mytarget_scope']
    # do something with self.object
    # remember the import: from django.http import HttpResponseRedirect

    # myStatusの設定
    key = self.request.user.profile
    key.myTarget = 1
    key.myDiet = 0
    key.save()

    return HttpResponseRedirect(self.get_success_url())


class Person_CreateView(LoginRequiredMixin, CreateView):  # todo person毎のパネルの枠を太くする
  model = Person
  form_class = Person_Form
  template_name = 'myApp/person_form.html'

  def get_form_kwargs(self):
    """This method is what injects forms with their keyword
        arguments."""
    # grab the current set of form #kwargs
    kwargs = super(Person_CreateView, self).get_form_kwargs()
    # Update the kwargs with the user_id
    kwargs['myLocation'] = self.kwargs['myLocation']
    return kwargs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = self.kwargs['myLocation']
    context['mytarget_scope'] = self.kwargs['mytarget_scope']
    context['myuser'] = self.request.user
    return context

  def get_success_url(self, **kwargs):
    return reverse_lazy('person_list',
                        kwargs={'myLocation': self.kwargs['myLocation'], 'page': self.kwargs['mytarget_scope']})

  def form_valid(self, form):
    self.object = form.save()
    form.instance.created_by = self.request.user
    form.instance.myDRI = DRI.objects.filter(
      nut_group=form.instance.nut_group).first()
    form.instance.target_scope = self.kwargs['mytarget_scope']
    # do something with self.object
    # remember the import: from django.http import HttpResponseRedirect

    # myStatusの設定
    key = self.request.user.profile
    key.myTarget = 1
    key.myDiet = 0
    key.save()

    return super(Person_CreateView, self).form_valid(form)


#        return HttpResponseRedirect(self.get_success_url())

class Person_DeleteView(LoginRequiredMixin, DeleteView):
  model = Person
  template_name = 'myApp/person_confirm_delete.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = self.kwargs['myLocation']
    context['mytarget_scope'] = self.kwargs['mytarget_scope']
    context['myuser'] = self.request.user
    return context

  def get_success_url(self, **kwargs):
    return reverse_lazy('person_list',
                        kwargs={'myLocation': self.kwargs['myLocation'], 'page': self.kwargs['mytarget_scope']})

  def delete(self, *args, **kwargs):
    self.object = self.get_object()
    # myStatusの設定
    key = self.request.user.profile
    key.myTarget = 0
    key.myDiet = 0
    key.save()

    return super(Person_DeleteView, self).delete(*args, **kwargs)


def registPerson(request):
  logger.info('registPerson')
  json_data = json.loads(request.body)
  nut_grp_list = ['child 0-23 month', 'child 24-59 month', 'child 6-9 yr', 'adolescent male', 'adolescent female',
                  'adult male', 'adult female', 'pregnant', 'lactating']

  form = PersonListForm(json_data)
  if (not form.is_valid()):
    return JsonResponse({
      'success': False,
      'messages': form.errors
    })

  for myrow in json_data['myJson']:
    # 最初に参照するキー（複数可）を指定する
    # defaultsで指定した列・値で更新する
    tmp_group = nut_grp_list[int(myrow['nut_group_id']) - 1]
    if myrow['target_scope'] == '1':  # 個人ターゲットの場合
      Person.objects.update_or_create(
        myLocation=Location.objects.get(id=myrow['myLocation']),
        target_scope=int(myrow['target_scope']),
        defaults={
          'target_pop': int(myrow['target_pop']),
          'nut_group': tmp_group,
          'created_by': request.user,
          'myDRI': DRI.objects.get(nut_group=tmp_group)
        }
      )
    else:  # 家族・コミュニティターゲットの場合
      Person.objects.update_or_create(
        myLocation=Location.objects.get(id=myrow['myLocation']),
        nut_group=tmp_group,
        target_scope=int(myrow['target_scope']),
        defaults={
          'target_pop': int(myrow['target_pop']),
          'created_by': request.user,
          'myDRI': DRI.objects.get(nut_group=tmp_group)
        }
      )

  # update myStatus
  key = request.user.profile
  key.myTarget = 1
  key.myDiet = 0
  key.save()

  myrow = json_data['myJson'][0]
  myURL = reverse_lazy('person_list',
                       kwargs={'myLocation': myrow['myLocation'], 'page': myrow['target_scope']})
  return JsonResponse({
    'success': True,
    'url': myURL,
  })


class Diet_Plan1(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Diet_Plan.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    myLoc = Location.objects.get(id=self.kwargs['myLocation'])
    context['myLocation'] = myLoc
    myseason = Season.objects.get(myLocation=self.kwargs['myLocation'])
    context['season_count'] = myseason.season_count
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation']).select_related('myDRI')
    context['nutrient_target'] = tmp_nut_group[0].nut_group
    nut_group_list = [
      'child 0-23 month',
      'child 24-59 month',
      'child 6-9 yr',
      'adolescent male',
      'adolescent female',
      'adult male',
      'adult female',
      'pregnant',
      'lactating',
      'adult',
      'adolescent pregnant',
      'adolescent lact',
      'adolescent all',
    ]

    tmp_dri = DRI.objects.all()
    # tmp_group_list = list(tmp_dri.values_list('nut_group', flat=True))
    tmp_dri_count = len(nut_group_list)
    tmp_en_by_class = [-1] * tmp_dri_count
    tmp_pr_by_class = [-1] * tmp_dri_count
    tmp_va_by_class = [-1] * tmp_dri_count
    tmp_fe_by_class = [-1] * tmp_dri_count
    tmp_vo_by_class = [-1] * tmp_dri_count
    for mydri in tmp_dri:
      logger.info(mydri.nut_group)
      index = nut_group_list.index(mydri.nut_group)
      logger.info(index)
      tmp_en_by_class[index] = mydri.energy
      tmp_pr_by_class[index] = mydri.protein
      tmp_va_by_class[index] = mydri.vita
      tmp_fe_by_class[index] = mydri.fe
      tmp_vo_by_class[index] = mydri.max_vol
    context['dri_list_en'] = tmp_en_by_class
    context['dri_list_pr'] = tmp_pr_by_class
    context['dri_list_va'] = tmp_va_by_class
    context['dri_list_fe'] = tmp_fe_by_class
    context['dri_list_vo'] = tmp_vo_by_class

    ########### send number of season   ###########
    tmp = Season.objects.filter(myLocation=self.kwargs['myLocation'])[0]
    season_field = ['m1_season', 'm2_season', 'm3_season', 'm4_season', 'm5_season', 'm6_season',
                    'm7_season', 'm8_season', 'm9_season', 'm10_season', 'm11_season', 'm12_season']
    month_text = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov',
                  'Dec']
    mydat = {}
    myseason = []
    season_name = []
    month_season1 = {}
    month_season2 = {}
    month_season1_text = {}
    month_season2_text = {}
    prev_dat = -1
    myRange = []
    season_index = 0
    for myindex, myfield in enumerate(season_field):
      tmpdat = str(getattr(tmp, myfield))
      mydat[myfield] = tmpdat
      if prev_dat != tmpdat:  # 各シーズンの最初と最後の月を記録
        season_index += 1
        month_season1[season_index] = (myindex + 1)
        if season_index > 0:
          month_season2[season_index - 1] = myindex
        prev_dat = tmpdat
      if myindex == 11:  # 最終月の処理
        month_season2[season_index] = 12  # 最後の季節を12月で締める
        if mydat['m1_season'] == mydat['m12_season']:  # 季節が年をまたいでいる場合の処理
          month_season1[1] = month_season1[season_index]
          del month_season1[season_index]
          del month_season2[season_index]

    context["season"] = mydat
    context["month_season_start"] = month_season1
    context["month_season_end"] = month_season2

    for myindex, mymonth in month_season1.items():
      month_season1_text[myindex] = month_text[mymonth - 1]
    for myindex, mymonth in month_season2.items():
      month_season2_text[myindex] = month_text[mymonth - 1]
    context["month_season_start_text"] = month_season1_text
    context["month_season_end_text"] = month_season2_text

    # queryの簡素化検討
    tmp_scope = list(
      tmp_nut_group.values_list('target_scope', flat=True).order_by(
        'target_scope').distinct())
    context['myTarget'] = tmp_scope

    tmpdat = str(getattr(tmp, 'season_count'))
    for i in range(int(tmpdat)):
      myseason.append(i + 1)
      for scope in tmp_scope:
        myRange.append(i + 1 + (int(scope) + 1) * 100)
    logger.info('myRange=')
    logger.info(myRange)

    context['season_list'] = myseason

    season_name.append(str(getattr(tmp, 'season_name1')))
    season_name.append(str(getattr(tmp, 'season_name2')))
    season_name.append(str(getattr(tmp, 'season_name3')))
    season_name.append(str(getattr(tmp, 'season_name4')))
    context['season_name'] = season_name

    #######################################################

    # send selected crop by community ######
    tmp01 = Crop_SubNational.objects.filter(myLocation_id=self.kwargs['myLocation']).select_related('myFCT')
    d = []
    for tmp02 in tmp01:
      dd = {}
      dd["selected_status"] = tmp02.selected_status
      dd["Food_grp"] = tmp02.myFCT.Food_grp_unicef
      dd["Food_name"] = tmp02.myFCT.Food_name
      dd["Energy"] = tmp02.myFCT.Energy
      dd["Protein"] = tmp02.myFCT.Protein
      dd["VITA_RAE"] = tmp02.myFCT.VITA_RAE
      dd["FE"] = tmp02.myFCT.FE
      dd["Weight"] = 0
      dd["food_item_id"] = tmp02.myFCT.food_item_id
      dd["portion_size"] = tmp02.myFCT.portion_size_init
      dd["count_buy"] = 0
      dd["count_prod"] = 0
      dd["portion_size"] = tmp02.myFCT.portion_size_init
      dd["m1"] = tmp02.m1_avail
      dd["m2"] = tmp02.m2_avail
      dd["m3"] = tmp02.m3_avail
      dd["m4"] = tmp02.m4_avail
      dd["m5"] = tmp02.m5_avail
      dd["m6"] = tmp02.m6_avail
      dd["m7"] = tmp02.m7_avail
      dd["m8"] = tmp02.m8_avail
      dd["m9"] = tmp02.m9_avail
      dd["m10"] = tmp02.m10_avail
      dd["m11"] = tmp02.m11_avail
      dd["m12"] = tmp02.m12_avail
      dd["myLocation"] = tmp02.myLocation_id
      dd["Fat"] = tmp02.myFCT.Fat
      dd["Carbohydrate"] = tmp02.myFCT.Carbohydrate
      d.append(dd)
    context["mylist_available"] = d

    # 作物のローカル名を送る
    tmp = Crop_Name._meta.get_fields()
    logger.info(tmp[2])
    tmp01 = Crop_Name.objects.filter(
      # myCountryName=Location.objects.filter(id=self.kwargs['myLocation']).first().country)
      myCountryName="ETH")  # 暫定措置
    d = []
    new_Food_grp = []
    for tmp02 in tmp01:
      dd = {}
      dd["Food_grp"] = tmp02.Food_grp
      dd["Food_name"] = tmp02.Food_name
      dd["food_item_id"] = tmp02.myFCT_id
      d.append(dd)
      tmp03 = tmp02.Food_grp
      if tmp03 not in new_Food_grp:
        new_Food_grp.append(tmp03)

    context["mylist_local_name"] = d
    context["mylist_Food_grp"] = new_Food_grp

    # 現在選択されている作物をDiet_plan_formに送る
    # --------------------create 16 Crop_individual-------------------------
    # if __name__ == '__main__':
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation']).select_related('myFCT')
    tmp01_list = list(tmp01.values())
    myFCT_list = list(FCT.objects.values())
    tmp_ref01 = list(Crop_SubNational.objects.filter(myLocation_id=self.kwargs['myLocation']).values())

    context["crop_ind_count"] = tmp01.count()

    d = []
    for i in myRange:
      tmp02_list = [d for d in tmp01_list if d['id_table'] == i]
      tmp02_key_list = [d['id'] for d in tmp02_list]
      logger.info('tmp02_list=')
      logger.info(tmp02_key_list)
      if not tmp02_key_list:
        dd = {}
        dd["Food_grp"] = ''
        dd["name"] = ''
        dd["Energy"] = ''
        dd["Protein"] = ''
        dd["VITA_RAE"] = ''
        dd["FE"] = ''
        dd["target_scope"] = ''
        dd["food_item_id"] = ''
        dd["portion_size"] = ''
        dd["total_weight"] = ''
        dd["count_prod"] = ''
        dd["count_buy"] = ''
        dd["month"] = ''
        dd["month_availability"] = ''
        dd["myLocation"] = ''
        dd["num_tbl"] = i
        dd["share_prod_buy"] = 5
        dd["Fat"] = ''
        dd["Carbohydrate"] = ''
        d.append(dd)
      else:
        for tmp03 in tmp02_list:
          dd = {}
          tmp_FCT = {}
          for myFCT_item in myFCT_list:
            if myFCT_item['food_item_id'] == tmp03['myFCT_id']:
              tmp_FCT.update(myFCT_item)
          dd["Food_grp"] = tmp_FCT['Food_grp_unicef']
          dd["name"] = tmp_FCT['Food_name']
          dd["Energy"] = tmp_FCT['Energy']
          dd["Protein"] = tmp_FCT['Protein']
          dd["VITA_RAE"] = tmp_FCT['VITA_RAE']
          dd["FE"] = tmp_FCT['FE']
          dd["target_scope"] = tmp03['target_scope']
          dd["food_item_id"] = tmp_FCT['food_item_id']
          dd["portion_size"] = tmp03['portion_size']
          dd["total_weight"] = tmp03['total_weight']
          dd["count_prod"] = tmp03['count_prod']
          dd["count_buy"] = tmp03['count_buy']
          dd["month"] = tmp03['month']
          #          dd["month_availability"] = tmp03.serializable_value('m' + str(tmp03.month) + '_avail')
          tmp_avail = 0
          for tmp_ref02 in tmp_ref01:
            if tmp_ref02['myFCT_id'] == tmp_FCT['food_item_id']:
              tmp_avail = tmp_ref02['m' + str(tmp03['month']) + '_avail']
              break
          dd["month_availability"] = tmp_avail
          #          dd["month_availability"] = tmp_ref.filter(myFCT_id=tmp03.myFCT.food_item_id)[0].serializable_value(
          #            'm' + str(tmp03.month) + '_avail')
          logger.info('dd["month_availability"]')
          logger.info(dd["month_availability"])
          dd["myLocation"] = tmp03['myLocation_id']
          dd["num_tbl"] = tmp03['id_table']
          dd["share_prod_buy"] = tmp03['share_prod_buy']
          dd["Fat"] = tmp_FCT['Fat']
          dd["Carbohydrate"] = tmp_FCT['Carbohydrate']
          d.append(dd)
    context["mylist_selected"] = d

    context['myuser'] = self.request.user

    stepid = self.request.user.profile.stepid
    newstep = 0
    if int(stepid) < 600:
      newstep = 400
    else:
      if myLoc.country == 'ETH':  # エチオピア限定の暫定措置
        newstep = 700
      else:
        newstep = 400
    tmp_Param = SetURL(newstep, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class Diet_instant(TemplateView):
  template_name = "myApp/Diet_instant.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    nut_group_list = [
      'child 0-23 month',
      'child 24-59 month',
      'child 6-9 yr',
      'adolescent male',
      'adolescent female',
      'adult male',
      'adult female',
      'pregnant',
      'lactating',
      'adult',
      'adolescent pregnant',
      'adolescent lact',
      'adolescent all',
    ]

    context['recepi_id'] = self.kwargs['recepi_id']

    tmp_dri = DRI.objects.all()
    # tmp_group_list = list(tmp_dri.values_list('nut_group', flat=True))
    tmp_dri_count = len(nut_group_list)
    tmp_en_by_class = [-1] * tmp_dri_count
    tmp_pr_by_class = [-1] * tmp_dri_count
    tmp_va_by_class = [-1] * tmp_dri_count
    tmp_fe_by_class = [-1] * tmp_dri_count
    tmp_vo_by_class = [-1] * tmp_dri_count
    for mydri in tmp_dri:
      logger.info(mydri.nut_group)
      index = nut_group_list.index(mydri.nut_group)
      logger.info(index)
      tmp_en_by_class[index] = mydri.energy
      tmp_pr_by_class[index] = mydri.protein
      tmp_va_by_class[index] = mydri.vita
      tmp_fe_by_class[index] = mydri.fe
      tmp_vo_by_class[index] = mydri.max_vol
    context['dri_list_en'] = tmp_en_by_class
    context['dri_list_en'] = tmp_en_by_class
    context['dri_list_pr'] = tmp_pr_by_class
    context['dri_list_va'] = tmp_va_by_class
    context['dri_list_fe'] = tmp_fe_by_class
    context['dri_list_vo'] = tmp_vo_by_class


    #######################################################

    # send selected crop by community ######
    #tmp01 = Crop_SubNational.objects.filter(myLocation_id=self.kwargs['myLocation']).select_related('myFCT')
    tmp01 = FCT.objects.all()
    d = []
    for tmp02 in tmp01:
      dd = {}
      dd["selected_status"] = 0
      dd["Food_grp"] = tmp02.Food_grp_unicef
      dd["Food_name"] = tmp02.Food_name
      dd["Energy"] = tmp02.Energy
      dd["Protein"] = tmp02.Protein
      dd["VITA_RAE"] = tmp02.VITA_RAE
      dd["FE"] = tmp02.FE
      dd["total_weight"] = 0
      dd["food_item_id"] = tmp02.food_item_id
      dd["portion_size"] = tmp02.portion_size_init
      dd["count_buy"] = 0
      dd["count_prod"] = 0
      dd["portion_size"] = tmp02.portion_size_init
      dd["m1"] = 0
      dd["m2"] = 0
      dd["m3"] = 0
      dd["m4"] = 0
      dd["m5"] = 0
      dd["m6"] = 0
      dd["m7"] = 0
      dd["m8"] = 0
      dd["m9"] = 0
      dd["m10"] = 0
      dd["m11"] = 0
      dd["m12"] = 0
      dd["myLocation"] = 0
      dd["Fat"] = tmp02.Fat
      dd["Carbohydrate"] = tmp02.Carbohydrate
      d.append(dd)
    context["mylist_available"] = d

    # 作物のローカル名を送る
    tmp = Crop_Name._meta.get_fields()
    logger.info(tmp[2])
    tmp01 = Crop_Name.objects.filter(
      # myCountryName=Location.objects.filter(id=self.kwargs['myLocation']).first().country)
      myCountryName="ETH")  # 暫定措置
    d = []
    new_Food_grp = []
    for tmp02 in tmp01:
      dd = {}
      dd["Food_grp"] = tmp02.Food_grp
      dd["Food_name"] = tmp02.Food_name
      dd["food_item_id"] = tmp02.myFCT_id
      d.append(dd)
      tmp03 = tmp02.Food_grp
      if tmp03 not in new_Food_grp:
        new_Food_grp.append(tmp03)

    context["mylist_local_name"] = d
    context["mylist_Food_grp"] = new_Food_grp

######## 現在選択されている作物をDiet_plan_formに送る

    d = []
    tmp01 = Crop_Individual_instant.objects.filter(recepi_id=self.kwargs['recepi_id'])
    myFCT_list = list(FCT.objects.values())
    myName = ''

    for tmp02 in tmp01:
      dd = {}
      tmp_FCT = {}
      for myFCT_item in myFCT_list:
        if myFCT_item['food_item_id'] == tmp02.myFCT_id:
          tmp_FCT.update(myFCT_item)
      myName = tmp02.myName
      dd["selected_status"] = 1
      dd["Food_grp"] = tmp_FCT['Food_grp_unicef']
      dd["name"] = tmp_FCT['Food_name']
      dd["Energy"] = tmp_FCT['Energy']
      dd["Protein"] = tmp_FCT['Protein']
      dd["VITA_RAE"] = tmp_FCT['VITA_RAE']
      dd["FE"] = tmp_FCT['FE']
      dd["total_weight"] = tmp02.total_weight
      dd["food_item_id"] = tmp_FCT['food_item_id']
      dd["portion_size"] = tmp02.portion_size
      dd["count_buy"] = tmp02.count_buy
      dd["count_prod"] = tmp02.count_prod
      dd["m1"] = 0
      dd["m2"] = 0
      dd["m3"] = 0
      dd["m4"] = 0
      dd["m5"] = 0
      dd["m6"] = 0
      dd["m7"] = 0
      dd["m8"] = 0
      dd["m9"] = 0
      dd["m10"] = 0
      dd["m11"] = 0
      dd["m12"] = 0
      dd["myLocation"] = 0
      dd["Fat"] = tmp_FCT['Fat']
      dd["Carbohydrate"] = tmp_FCT['Carbohydrate']
      d.append(dd)
    context["mylist_selected"] = d
    context['myName'] = myName

    #######


    #context['myuser'] = self.request.user

    context['nav_link1'] = reverse_lazy("index10")
    context['nav_text1'] = "menu"
    context['nav_link2'] = ""
    context['nav_text2'] = "instant mode"
    context['nav_link3'] = ""
    context['nav_text3'] = ""
    context["mark_text"] = 'diet nutrition calculator'
    context["stepid"] = 1000

    return context

class Diet_instant_ListView(ListView):
  template_name = 'myApp/diet_instant_list.html'  # この行でテンプレート指定
  context_object_name = 'mylist'
  model = Crop_Individual_instant

  # def get_queryset(self):
  #   queryset = Crop_Individual_instant.objects.all().values_list('recepi_id', 'myName', 'created_at').order_by('recepi_id').distinct()
  #   return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['nav_link1'] = reverse_lazy("index10")
    context['nav_text1'] = "menu"
    context['nav_link2'] = ""
    context['nav_text2'] = "instant mode"
    context['nav_link3'] = ""
    context['nav_text3'] = ""
    context["mark_text"] = 'diet nutrition calculator'
    context["stepid"] = 1000

    return context


def delete_TableRec(request, tblName):
  myTable = apps.get_app_config('myApp').get_model(tblName)
  myTable.objects.all().delete()
  result = f"{tblName} data have been deleted"
  return HttpResponse(result)


class initTable(TemplateView):
  template_name = "myApp/_initTable.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    myTables = apps.get_app_config('myApp').get_models()
    myTableName = []
    myTableName.append('---select table---')
    for myTable in myTables:
      myTableName.append(myTable._meta.model_name)
    context['myTables'] = myTableName

    return context


def registDiet(request):
  # json_str = request.body.decode("utf-8")
  json_data = json.loads(request.body)
  tmp_myLocation_id = 0
  # tmp_newcrop_list = []

  for myrow in json_data['myJson']:
    # 最初に参照するキー（複数可）を指定する
    # defaultsで指定した列・値で更新する
    logger.error(myrow['month'])
    Crop_Individual.objects.update_or_create(
      myFCT=FCT.objects.get(food_item_id=int(myrow['food_item_id'])),
      month=int(myrow['month']),
      target_scope=int(myrow['target_scope']),
      defaults={
        'id_table': int(myrow['myid_tbl']),
        'myLocation': Location.objects.get(id=myrow['myLocation']),
        'created_by': request.user,
        'total_weight': int(myrow['total_weight']),
        'portion_size': int(myrow['portion_size']),
        'count_prod': int(myrow['count_prod']),
        'count_buy': int(myrow['count_buy']),
        'share_prod_buy': int(myrow['share_prod_buy'])
      }
    )

  # update myStatus
  key = request.user.profile
  key.myDiet = 1
  key.save()

  myURL = reverse_lazy('diet1',
                       kwargs={'myLocation': request.user.profile.myLocation})
  return JsonResponse({
    'success': True,
    'url': myURL,
  })

def registDiet2(request):
  # json_str = request.body.decode("utf-8")
  json_data = json.loads(request.body)
  tmp_myLocation_id = 0
  # tmp_newcrop_list = []

  recepi_num = json_data['myJson'][0]['recepi_id']
  if recepi_num == 0:
    try:
      recepi_num = int(Crop_Individual_instant.objects.all().aggregate(Max('recepi_id'))['recepi_id__max']) + 1
    except:
      recepi_num = 1
  else:
    Crop_Individual_instant.objects.filter(recepi_id=recepi_num).delete()

  for myrow in json_data['myJson']:
    Crop_Individual_instant.objects.create(
      myFCT=FCT.objects.get(food_item_id=int(myrow['food_item_id'])),
      total_weight=int(myrow['total_weight']),
      portion_size=int(myrow['portion_size']),
      count_prod=int(myrow['count_prod']),
      count_buy=int(myrow['count_buy']),
      share_prod_buy=int(myrow['share_prod_buy']),
      target_scope=int(myrow['target_scope']),
      myName = myrow['myName'],
      recepi_id = recepi_num
    )

  myURL = reverse_lazy('diet_instant', kwargs={'recepi_id':recepi_num})
  return JsonResponse({
    'success': True,
    'url': myURL,
  })


class Output1(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output1.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    # tmp_nut_group = Person.objects.filter(
    #  myLocation=self.kwargs['myLocation'])
    tmp_nut_group1 = Person.objects.filter(myLocation=self.kwargs['myLocation']).values_list('nut_group', 'target_scope'
                                                                                             ).order_by('nut_group').distinct()
    tmp_nut_group2 = {}
    for a, b in tmp_nut_group1:
      tmp_id = str((int(b) + 1) * 100)
      tmp_nut_group2[tmp_id] = a

    context['nutrient_target2'] = tmp_nut_group2

    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation']).select_related('myDRI')
    context['nutrient_target'] = tmp_nut_group[0].nut_group
    nut_group_list = [
      'child 0-23 month',
      'child 24-59 month',
      'child 6-9 yr',
      'adolescent male',
      'adolescent female',
      'adult male',
      'adult female',
      'pregnant',
      'lactating',
      'adult',
      'adolescent pregnant',
      'adolescent lact',
      'adolescent all',
    ]

    tmp_dri = DRI.objects.all()


    month_field = ['m1_season', 'm2_season', 'm3_season', 'm4_season', 'm5_season', 'm6_season',
                   'm7_season', 'm8_season', 'm9_season', 'm10_season', 'm11_season', 'm12_season']
    tmp_seasons = Season.objects.get(myLocation_id=self.kwargs['myLocation'])
    month = []
    season_name = []
    season_field = ['season_name4', 'season_name1', 'season_name2', 'season_name3']

    tmp_dri = DRI.objects.all()
    # tmp_group_list = list(tmp_dri.values_list('nut_group', flat=True))
    tmp_dri_count = len(nut_group_list)
    tmp_en_by_class = [-1] * tmp_dri_count
    tmp_pr_by_class = [-1] * tmp_dri_count
    tmp_va_by_class = [-1] * tmp_dri_count
    tmp_fe_by_class = [-1] * tmp_dri_count
    tmp_vo_by_class = [-1] * tmp_dri_count
    for mydri in tmp_dri:
      logger.info(mydri.nut_group)
      index = nut_group_list.index(mydri.nut_group)
      logger.info(index)
      tmp_en_by_class[index] = mydri.energy
      tmp_pr_by_class[index] = mydri.protein
      tmp_va_by_class[index] = mydri.vita
      tmp_fe_by_class[index] = mydri.fe
      tmp_vo_by_class[index] = mydri.max_vol
    context['dri_list_en'] = tmp_en_by_class
    context['dri_list_pr'] = tmp_pr_by_class
    context['dri_list_va'] = tmp_va_by_class
    context['dri_list_fe'] = tmp_fe_by_class
    context['dri_list_vo'] = tmp_vo_by_class

    # queryの簡素化検討
    tmp_scope = list(
      tmp_nut_group.values_list('target_scope', flat=True).order_by(
        'target_scope').distinct())
    context['myTarget'] = tmp_scope

    myseason = []
    myRange = []
    tmp = Season.objects.filter(myLocation=self.kwargs['myLocation'])[0]
    tmpdat = str(getattr(tmp, 'season_count'))
    for i in range(int(tmpdat)):
      myseason.append(i + 1)
      for scope in tmp_scope:
        myRange.append(i + 1 + (int(scope) + 1) * 100)
    logger.info('myRange=')
    logger.info(myRange)

    context['season_list'] = myseason

    season_name.append(str(getattr(tmp, 'season_name1')))
    season_name.append(str(getattr(tmp, 'season_name2')))
    season_name.append(str(getattr(tmp, 'season_name3')))
    season_name.append(str(getattr(tmp, 'season_name4')))
    context['season_name'] = season_name

    # send selected crop by community ######
    # --------------------create 16 Crop_individual-------------------------
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation']).select_related('myFCT')
    tmp01_list = list(tmp01.values())
    myFCT_list = list(FCT.objects.values())

    d = []
    if len(tmp01_list) > 0:
      for tmp02 in tmp01_list:
        dd = {}
        tmp_FCT = {}
        for myFCT_item in myFCT_list:
          if myFCT_item['food_item_id'] == tmp02['myFCT_id']:
            tmp_FCT.update(myFCT_item)
        dd["Food_grp"] = tmp_FCT['Food_grp_unicef']
        dd["name"] = tmp_FCT['Food_name']
        dd["Energy"] = tmp_FCT['Energy']
        dd["Protein"] = tmp_FCT['Protein']
        dd["VITA_RAE"] = tmp_FCT['VITA_RAE']
        dd["FE"] = tmp_FCT['FE']
        dd["target_scope"] = tmp02['target_scope']
        dd["food_item_id"] = tmp_FCT['food_item_id']
        dd["portion_size"] = tmp02['portion_size']
        dd["total_weight"] = tmp02['total_weight']
        dd["count_prod"] = tmp02['count_prod']
        dd["count_buy"] = tmp02['count_buy']
        dd["month"] = tmp02['month']
        dd["myLocation"] = tmp02['myLocation_id']
        dd["myid_tbl"] = tmp02['id_table']
        d.append(dd)
    context["mylist_selected"] = d

    context['myuser'] = self.request.user

    tmp_Param = SetURL(801, self.request.user)
    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class Output2(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output2.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation'])
    context['nutrient_target'] = tmp_nut_group[0].nut_group

    month_field = ['m1_season', 'm2_season', 'm3_season', 'm4_season', 'm5_season', 'm6_season',
                   'm7_season', 'm8_season', 'm9_season', 'm10_season', 'm11_season', 'm12_season']
    tmp_seasons = Season.objects.get(myLocation_id=self.kwargs['myLocation'])
    month = []
    season_name = []
    season_field = ['season_name4', 'season_name1', 'season_name2', 'season_name3']
    for tmp in month_field:
      s_val = getattr(tmp_seasons, tmp)
      if s_val not in month:
        month.append(s_val)
    for tmp2 in month:
      season_name.append(getattr(tmp_seasons, season_field[tmp2]))
    context["season_name"] = season_name

    tmp_nut_group1 = tmp_nut_group.filter(target_scope=1)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    for tmp in tmp_nut_group1:
      tmp_e += tmp.myDRI.energy
      tmp_p += tmp.myDRI.protein
      tmp_v += tmp.myDRI.vita
      tmp_f += tmp.myDRI.fe
    context['dri_e1'] = tmp_e
    context['dri_p1'] = tmp_p
    context['dri_v1'] = tmp_v
    context['dri_f1'] = tmp_f

    tmp_nut_group2 = tmp_nut_group.filter(target_scope=2)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    for tmp in tmp_nut_group2:
      tmp_e += tmp.myDRI.energy
      tmp_p += tmp.myDRI.protein
      tmp_v += tmp.myDRI.vita
      tmp_f += tmp.myDRI.fe
    context['dri_e2'] = tmp_e
    context['dri_p2'] = tmp_p
    context['dri_v2'] = tmp_v
    context['dri_f2'] = tmp_f

    tmp_nut_group3 = tmp_nut_group.filter(target_scope=3)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    for tmp in tmp_nut_group3:
      tmp_e += tmp.myDRI.energy
      tmp_p += tmp.myDRI.protein
      tmp_v += tmp.myDRI.vita
      tmp_f += tmp.myDRI.fe
    context['dri_e3'] = tmp_e
    context['dri_p3'] = tmp_p
    context['dri_v3'] = tmp_v
    context['dri_f3'] = tmp_f

    # send selected crop by community ######
    # --------------------create 16 Crop_individual-------------------------
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation']).filter(target_scope=2)
    # myRange = [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212]
    d = []
    if tmp01.count() > 0:
      for tmp02 in tmp01:
        dd = {}
        dd["name"] = tmp02.myFCT.Food_name
        dd["Energy"] = tmp02.myFCT.Energy
        dd["Protein"] = tmp02.myFCT.Protein
        dd["VITA_RAE"] = tmp02.myFCT.VITA_RAE
        dd["FE"] = tmp02.myFCT.FE
        dd["target_scope"] = tmp02.target_scope
        dd["food_item_id"] = tmp02.myFCT.food_item_id
        dd["portion_size"] = tmp02.portion_size
        dd["total_weight"] = tmp02.total_weight
        dd["count_prod"] = tmp02.count_prod
        dd["count_buy"] = tmp02.count_buy
        dd["month"] = tmp02.month
        dd["myLocation"] = tmp02.myLocation_id
        dd["myid_tbl"] = tmp02.id_table
        d.append(dd)
    context["mylist_selected"] = d

    context['myuser'] = self.request.user

    tmp_Param = SetURL(802, self.request.user)
    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class Output3(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output3.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation'])
    context['nutrient_target'] = tmp_nut_group[0].nut_group

    # send selected crop by community ######
    # --------------------create 16 Crop_individual-------------------------
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation'])
    # myRange = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    d = []
    tmp02 = tmp01.filter(target_scope=2)
    if tmp02.count() != 0:
      for tmp03 in tmp02:
        dd = {}
        dd["name"] = tmp03.myFCT.Food_name
        dd["Energy"] = tmp03.myFCT.Energy
        dd["Protein"] = tmp03.myFCT.Protein
        dd["VITA_RAE"] = tmp03.myFCT.VITA_RAE
        dd["FE"] = tmp03.myFCT.FE
        dd["target_scope"] = tmp03.target_scope
        dd["food_item_id"] = tmp03.myFCT.food_item_id
        dd["portion_size"] = tmp03.portion_size
        dd["total_weight"] = tmp03.total_weight
        dd["count_prod"] = tmp03.count_prod
        dd["count_buy"] = tmp03.count_buy
        dd["month"] = tmp03.month
        dd["myLocation"] = tmp03.myLocation_id
        dd["myid_tbl"] = tmp03.id_table
        d.append(dd)

    context["mylist_selected"] = d

    context['myuser'] = self.request.user

    tmp_Param = SetURL(803, self.request.user)
    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class Output4(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output4.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation'])
    context['nutrient_target'] = tmp_nut_group[0].nut_group

    # ------------------------------------------
    # return object from dict found by value
    # ------------------------------------------
    def get_key_from_value(d, val):
      keys = [k for k, v in d.items() if v == val]
      if keys:
        return int(keys[0])
      return None

    # ------------------------------------------

    # send selected crop by community ######
    # --------------------create 16 Crop_individual-------------------------
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation'])
    tmp01_list = list(tmp01.values())
    myFCT_list = list(FCT.objects.values())
    # myRange = [301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312]
    d = []
    food_list = {}

    tmp02 = tmp01.filter(target_scope=3)
    if len(tmp01_list) > 0:
      for tmp03 in tmp01_list:
        found = get_key_from_value(food_list, str(tmp03['myFCT_id']) + "_" + str(tmp03['month']))
        if found != None:
          d[found]["total_weight"] += tmp03['total_weight']

        else:
          dd = {}
          tmp_FCT = {}
          for myFCT_item in myFCT_list:
            if myFCT_item['food_item_id'] == tmp03['myFCT_id']:
              tmp_FCT.update(myFCT_item)

          dd["name"] = tmp_FCT['Food_name']
          dd["Energy"] = tmp_FCT['Energy']
          dd["Protein"] = tmp_FCT['Protein']
          dd["VITA_RAE"] = tmp_FCT['VITA_RAE']
          dd["FE"] = tmp_FCT['FE']
          dd["target_scope"] = tmp03['target_scope']
          dd["food_item_id"] = tmp_FCT['food_item_id']
          dd["portion_size"] = tmp03['portion_size']
          dd["total_weight"] = tmp03['total_weight']
          dd["count_prod"] = tmp03['count_prod']
          dd["count_buy"] = tmp03['count_buy']
          dd["month"] = tmp03['month']
          dd["myLocation"] = tmp03['myLocation_id']
          dd["myid_tbl"] = tmp03['id_table']
          d.append(dd)
          food_list[len(d) - 1] = str(tmp03['myFCT_id']) + "_" + str(tmp03['month'])
    context["mylist_selected"] = d

    # --------------------create populationl-------------------------
    tmp01 = Person.objects.filter(myLocation_id=self.kwargs['myLocation'])
    if tmp01.count() > 0:
      dd = {}
      for tmp02 in tmp01:
        dd[tmp02.nut_group] = tmp02.target_pop
      context["mylist_target"] = dd

    context['myuser'] = self.request.user

    if Location.objects.get(id=self.kwargs['myLocation']).country == 'ETH':  # エチオピア限定の暫定措置
      tmp_Param = SetURL(804, self.request.user)
    else:
      tmp_Param = SetURL(804, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class Output_list(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output_list.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = self.kwargs['myLocation']
    context['myuser'] = self.request.user

    if Location.objects.get(id=self.kwargs['myLocation']).country == 'ETH':  # エチオピア限定の暫定措置
      tmp_Param = SetURL(800, self.request.user)
    else:
      tmp_Param = SetURL(805, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class Crop_Feas_CreateView(LoginRequiredMixin, CreateView):
  model = Crop_Feasibility
  form_class = Crop_Feas_Form
  template_name = 'myApp/Crop_Feas_form.html'
  success_url = reverse_lazy('crop_feas_list')

  def get_form_kwargs(self):
    kwargs = super(Crop_Feas_CreateView, self).get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    context['isUpdate'] = 0
    myLoc = Location.objects.get(id=self.request.user.profile.myLocation)
    context['myLocation'] = myLoc
    tmp_nut_group = Person.objects.filter(myLocation=myLoc).select_related('myDRI')

    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    tmp_vol = 0
    tmp_target = ''
    if len(tmp_nut_group) > 0:
      tmp_nut_group1 = tmp_nut_group[0]
      tmp_e = tmp_nut_group1.myDRI.energy
      tmp_p = tmp_nut_group1.myDRI.protein
      tmp_v = tmp_nut_group1.myDRI.vita
      tmp_f = tmp_nut_group1.myDRI.fe
      tmp_vol = tmp_nut_group1.myDRI.max_vol
      tmp_target = tmp_nut_group1.nut_group

    context['dri_e1'] = tmp_e
    context['dri_p1'] = tmp_p
    context['dri_v1'] = tmp_v
    context['dri_f1'] = tmp_f
    context['dri_vol1'] = tmp_vol
    context['nutrient_target'] = tmp_target

    # send non-available crop in the original list ######
    available_list = []
    if myLoc.country == 'ETH':  # エチオピア限定の暫定措置
      tmp01 = Crop_SubNational.objects.filter(myLocation_id=myLoc).select_related(
        'myFCT')
      for tmp02 in tmp01:
        available_list.append(tmp02.myFCT.id)

    tmp01 = FCT.objects.all()
    d = []
    for tmp02 in tmp01:
      if tmp02.id not in available_list:
        dd = {}
        dd["selected_status"] = 0
        dd["Food_grp"] = tmp02.Food_grp_unicef
        dd["Food_name"] = tmp02.Food_name
        dd["Energy"] = tmp02.Energy
        dd["Protein"] = tmp02.Protein
        dd["VITA_RAE"] = tmp02.VITA_RAE
        dd["FE"] = tmp02.FE
        dd["Weight"] = 0
        dd["food_item_id"] = tmp02.food_item_id
        dd["portion_size"] = tmp02.portion_size_init
        dd["count_buy"] = 0
        dd["count_prod"] = 0
        dd["m1"] = 0
        dd["m2"] = 0
        dd["m3"] = 0
        dd["m4"] = 0
        dd["m5"] = 0
        dd["m6"] = 0
        dd["m7"] = 0
        dd["m8"] = 0
        dd["m9"] = 0
        dd["m10"] = 0
        dd["m11"] = 0
        dd["m12"] = 0
        # dd["myLocation"] = tmp02.myLocation_id
        d.append(dd)

    context["mylist_available"] = d

    if myLoc.country == 'ETH':  # エチオピア限定の暫定措置
      tmp_Param = SetURL(501, self.request.user)
    else:
      tmp_Param = SetURL(701, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context

  def form_valid(self, form):
    #    self.object = form.save()
    form.instance.created_by = self.request.user
    form.instance.myLocation = Location.objects.get(id=self.request.user.profile.myLocation)
    return super(Crop_Feas_CreateView, self).form_valid(form)


@receiver(post_save, sender=Crop_Feasibility)
def create_cropFeas(sender, instance, created, **kwargs):
  if created:
    # --------------------add Crop_SubNational-------------------------
    logger.info("これからCrop＿SubNationalを追加していきます")
    # keys = {}
    # keys['selected_status'] = 1
    # keys['created_by'] = User.objects.get(id=instance.created_by.id)
    # keys['myFCT'] = instance.myFCT
    # keys['crop_feas'] = Crop_Feasibility.objects.get(id=instance.pk)
    # keys['myLocation'] = Location.objects.get(id=instance.myLocation.id)
    # p = Crop_SubNational.objects.create(**keys)

    Crop_SubNational.objects.update_or_create(
      myLocation=Location.objects.get(id=instance.myLocation.id),
      myFCT=instance.myFCT,
      defaults={
        'crop_feas': Crop_Feasibility.objects.get(id=instance.pk),
        'selected_status': 1,
        'created_by': User.objects.get(id=instance.created_by.id),
      }
    )
    logger.info("Crop_SubNationalに書き込みました!")


class Crop_Feas_ListView(LoginRequiredMixin, ListView):
  context_object_name = "mylist"
  template_name = 'myApp/Crop_Feas_list.html'

  def get_queryset(self):
    tmp0 = Crop_Feasibility.objects.filter(created_by=self.request.user).filter(
      myLocation=self.request.user.profile.myLocation)
    score_nut = []
    score_soc = []
    score_tec = []
    score_inv = []
    score_sus = []
    for tmp1 in tmp0:
      score_nut.append(round(tmp1.feas_DRI_e * 10 / 3))
      score_soc.append(round((tmp1.feas_soc_acceptable + tmp1.feas_soc_acceptable_wo + tmp1.feas_soc_acceptable_c5 +
                              tmp1.feas_affordability) * 10 / 12))
      score_tec.append(round((tmp1.feas_prod_skill + tmp1.feas_workload + tmp1.feas_tech_service) * 10 / 12))
      score_inv.append(round((tmp1.feas_invest_fixed + tmp1.feas_invest_variable) * 10 / 8))
      score_sus.append(round((tmp1.feas_availability_prod + tmp1.feas_storability) * 10 / 6))
    tmp1 = zip(tmp0, score_nut, score_inv, score_soc, score_sus, score_tec)
    logger.info(self.request.user)
    logger.info(self.request.user.profile.myLocation)

    return tmp1
    logger.info(self.request.user)
    logger.info(self.request.user.profile.myLocation)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['isUpdate'] = 0
    context['myuser'] = self.request.user
    context['myLocation'] = self.request.user.profile.myLocation
    context['myLocation_name'] = Location.objects.get(id=self.request.user.profile.myLocation).name

    if Location.objects.get(id=self.request.user.profile.myLocation).country == 'ETH':  # エチオピア限定の暫定措置
      tmp_Param = SetURL(500, self.request.user)
    else:
      tmp_Param = SetURL(701, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    context["mylist_available"] = []

    return context


class Crop_Feas_DeleteView(LoginRequiredMixin, DeleteView):  # todo これをmodal dialogueにする
  model = Crop_Feasibility
  template_name = 'myApp/Crop_Feas_confirm_delete.html'
  success_url = reverse_lazy('crop_feas_list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    return context

  def delete(self, *args, **kwargs):
    self.object = self.get_object()
    # Crop_Subnationalからの削除
    Crop_SubNational.objects.filter(
      myLocation=Location.objects.get(id=self.request.user.profile.myLocation)).filter(
      myFCT=Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT
    ).delete()

    return super(Crop_Feas_DeleteView, self).delete(*args, **kwargs)


class Crop_Feas_UpdateView(LoginRequiredMixin, UpdateView):
  model = Crop_Feasibility
  form_class = Crop_Feas_Form
  template_name = 'myApp/Crop_Feas_form.html'
  success_url = reverse_lazy('crop_feas_list')

  def get_form_kwargs(self):
    kwargs = super(Crop_Feas_UpdateView, self).get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

  def get_initial(self):
    return {
      'crop_name': Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.Food_name,
      'crop_name_id': Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.food_item_id
    }

  def get_context_data(self, **kwargs):  # todo 無意味なcrop_listの送信をやめる
    context = super().get_context_data(**kwargs)
    context['isUpdate'] = 1
    context['myuser'] = self.request.user
    myLoc = Location.objects.get(id=self.request.user.profile.myLocation)
    context['myLocation'] = myLoc
    context['crop_name'] = Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.Food_name
    context['crop_name_id'] = Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.food_item_id
    context['crop_en'] = Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.Energy
    context['crop_pr'] = Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.Protein
    context['crop_va'] = Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.VITA_RAE
    context['crop_fe'] = Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.FE
    context['myLocation_name'] = myLoc.name

    tmp_nut_group = Person.objects.filter(
      myLocation=myLoc).select_related('myDRI')
    context['nutrient_target'] = tmp_nut_group[0].nut_group

    tmp_nut_group1 = tmp_nut_group.filter(target_scope=1)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    tmp_vol = 0
    if len(tmp_nut_group1) > 0:
      for tmp in tmp_nut_group1:
        tmp_e += tmp.myDRI.energy
        tmp_p += tmp.myDRI.protein
        tmp_v += tmp.myDRI.vita
        tmp_f += tmp.myDRI.fe
        tmp_vol += tmp.myDRI.max_vol
    context['dri_e1'] = tmp_e
    context['dri_p1'] = tmp_p
    context['dri_v1'] = tmp_v
    context['dri_f1'] = tmp_f
    context['dri_vol1'] = tmp_vol

    # send non-available crop in the original list 無意味なのですが######
    available_list = []
    if myLoc.country == 'ETH':  # エチオピア限定の暫定措置
      tmp01 = Crop_SubNational.objects.filter(myLocation_id=self.request.user.profile.myLocation)
      for tmp02 in tmp01:
        available_list.append(tmp02.myFCT.id)

    tmp01 = FCT.objects.all()
    d = []
    for tmp02 in tmp01:
      if tmp02.id not in available_list:
        dd = {}
        dd["Food_grp"] = tmp02.Food_grp
        dd["Food_name"] = tmp02.Food_name
        dd["Energy"] = tmp02.Energy
        dd["Protein"] = tmp02.Protein
        dd["VITA_RAE"] = tmp02.VITA_RAE
        dd["FE"] = tmp02.FE
        dd["food_item_id"] = tmp02.food_item_id
        d.append(dd)

    context["mylist_crop"] = d

    if myLoc.country == 'ETH':  # エチオピア限定の暫定措置
      tmp_Param = SetURL(501, self.request.user)
    else:
      tmp_Param = SetURL(701, self.request.user)

    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context

  def form_valid(self, form):
    #    self.object = form.save()
    form.instance.created_by = self.request.user
    form.instance.myLocation = Location.objects.get(id=self.request.user.profile.myLocation)
    return super(Crop_Feas_UpdateView, self).form_valid(form)


class Crop_Feas2_CreateView(CreateView):
  model = Crop_Feasibility_instant
  form_class = Crop_Feas2_Form
  template_name = 'myApp/Crop_Feas2_form.html'
  success_url = reverse_lazy('crop_feas2_list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    nut_group_list = [
      'child 0-23 month',
      'child 24-59 month',
      'child 6-9 yr',
      'adolescent male',
      'adolescent female',
      'adult male',
      'adult female',
      'pregnant',
      'lactating',
      'adult',
      'adolescent pregnant',
      'adolescent lact',
      'adolescent all',
    ]
    context['isUpdate'] = 0

    tmp_dri = DRI.objects.all()
    # tmp_group_list = list(tmp_dri.values_list('nut_group', flat=True))
    tmp_dri_count = len(nut_group_list)
    tmp_en_by_class = [-1] * tmp_dri_count
    tmp_pr_by_class = [-1] * tmp_dri_count
    tmp_va_by_class = [-1] * tmp_dri_count
    tmp_fe_by_class = [-1] * tmp_dri_count
    tmp_vo_by_class = [-1] * tmp_dri_count
    for mydri in tmp_dri:
      logger.info(mydri.nut_group)
      index = nut_group_list.index(mydri.nut_group)
      logger.info(index)
      tmp_en_by_class[index] = mydri.energy
      tmp_pr_by_class[index] = mydri.protein
      tmp_va_by_class[index] = mydri.vita
      tmp_fe_by_class[index] = mydri.fe
      tmp_vo_by_class[index] = mydri.max_vol
    context['dri_list_en'] = tmp_en_by_class
    context['dri_list_pr'] = tmp_pr_by_class
    context['dri_list_va'] = tmp_va_by_class
    context['dri_list_fe'] = tmp_fe_by_class
    context['dri_list_vo'] = tmp_vo_by_class

    # send non-available crop in the original list ######
    available_list = []

    tmp01 = FCT.objects.all()
    d = []
    for tmp02 in tmp01:
      dd = {}
      dd["selected_status"] = 0
      dd["Food_grp"] = tmp02.Food_grp_unicef
      dd["Food_name"] = tmp02.Food_name
      dd["Energy"] = tmp02.Energy
      dd["Protein"] = tmp02.Protein
      dd["VITA_RAE"] = tmp02.VITA_RAE
      dd["FE"] = tmp02.FE
      dd["Weight"] = 0
      dd["food_item_id"] = tmp02.food_item_id
      dd["portion_size"] = tmp02.portion_size_init
      dd["count_buy"] = 0
      dd["count_prod"] = 0
      dd["m1"] = 0
      dd["m2"] = 0
      dd["m3"] = 0
      dd["m4"] = 0
      dd["m5"] = 0
      dd["m6"] = 0
      dd["m7"] = 0
      dd["m8"] = 0
      dd["m9"] = 0
      dd["m10"] = 0
      dd["m11"] = 0
      dd["m12"] = 0
      # dd["myLocation"] = tmp02.myLocation_id
      d.append(dd)

    context["mylist_available"] = d

    context['nav_link1'] = reverse_lazy("crop_feas2_list")
    context['nav_text1'] = "list"
    context['nav_link2'] = ""
    context['nav_text2'] = "feasibility check"
    context['nav_link3'] = ""
    context['nav_text3'] = ""
    context["mark_text"] = 'quick feasibility assessment'
    context["stepid"] = 1000
    return context


class Crop_Feas2_ListView( ListView):
  context_object_name = "mylist"
  template_name = 'myApp/Crop_Feas2_list.html'

  def get_queryset(self):
    tmp0 = Crop_Feasibility_instant.objects.all()
    score_nut = []
    score_soc = []
    score_tec = []
    score_inv = []
    score_sus = []
    for tmp1 in tmp0:
      score_nut.append(round(tmp1.feas_DRI_e * 10 / 3))
      score_soc.append(round((tmp1.feas_soc_acceptable + tmp1.feas_soc_acceptable_wo + tmp1.feas_soc_acceptable_c5 +
                              tmp1.feas_affordability) * 10 / 12))
      score_tec.append(round((tmp1.feas_prod_skill + tmp1.feas_workload + tmp1.feas_tech_service) * 10 / 12))
      score_inv.append(round((tmp1.feas_invest_fixed + tmp1.feas_invest_variable) * 10 / 8))
      score_sus.append(round((tmp1.feas_availability_prod + tmp1.feas_storability) * 10 / 6))
    tmp1 = zip(tmp0, score_nut, score_inv, score_soc, score_sus, score_tec)
    return tmp1

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['isUpdate'] = 0

    context['nav_link1'] = reverse_lazy("index10")
    context['nav_text1'] = "menu"
    context['nav_link2'] = ""
    context['nav_text2'] = "feasibility check"
    context['nav_link3'] = ""
    context['nav_text3'] = ""
    context["mark_text"] = 'quick feasibility assessment'
    context["stepid"] = 1000

    context["mylist_available"] = []

    return context


class Crop_Feas2_DeleteView( DeleteView):  # todo これをmodal dialogueにする
  model = Crop_Feasibility_instant
  template_name = 'myApp/Crop_Feas2_confirm_delete.html'
  success_url = reverse_lazy('crop_feas2_list')


class Crop_Feas2_UpdateView(UpdateView):
  model = Crop_Feasibility_instant
  form_class = Crop_Feas2_Form
  template_name = 'myApp/Crop_Feas2_form.html'
  success_url = reverse_lazy('crop_feas2_list')

  def get_initial(self):
    return {
      'crop_name': Crop_Feasibility_instant.objects.get(id=self.kwargs['pk']).myFCT.Food_name,
      'crop_name_id': Crop_Feasibility_instant.objects.get(id=self.kwargs['pk']).myFCT.food_item_id
    }

  def get_context_data(self, **kwargs):  # todo 無意味なcrop_listの送信をやめる
    context = super().get_context_data(**kwargs)
    context['isUpdate'] = 1
    context['crop_name'] = Crop_Feasibility_instant.objects.get(id=self.kwargs['pk']).myFCT.Food_name
    context['crop_name_id'] = Crop_Feasibility_instant.objects.get(id=self.kwargs['pk']).myFCT.food_item_id
    context['crop_en'] = Crop_Feasibility_instant.objects.get(id=self.kwargs['pk']).myFCT.Energy
    context['crop_pr'] = Crop_Feasibility_instant.objects.get(id=self.kwargs['pk']).myFCT.Protein
    context['crop_va'] = Crop_Feasibility_instant.objects.get(id=self.kwargs['pk']).myFCT.VITA_RAE
    context['crop_fe'] = Crop_Feasibility_instant.objects.get(id=self.kwargs['pk']).myFCT.FE

    nut_group_list = [
      'child 0-23 month',
      'child 24-59 month',
      'child 6-9 yr',
      'adolescent male',
      'adolescent female',
      'adult male',
      'adult female',
      'pregnant',
      'lactating',
      'adult',
      'adolescent pregnant',
      'adolescent lact',
      'adolescent all',
    ]

    tmp_dri = DRI.objects.all()
    # tmp_group_list = list(tmp_dri.values_list('nut_group', flat=True))
    tmp_dri_count = len(nut_group_list)
    tmp_en_by_class = [-1] * tmp_dri_count
    tmp_pr_by_class = [-1] * tmp_dri_count
    tmp_va_by_class = [-1] * tmp_dri_count
    tmp_fe_by_class = [-1] * tmp_dri_count
    tmp_vo_by_class = [-1] * tmp_dri_count
    for mydri in tmp_dri:
      logger.info(mydri.nut_group)
      index = nut_group_list.index(mydri.nut_group)
      logger.info(index)
      tmp_en_by_class[index] = mydri.energy
      tmp_pr_by_class[index] = mydri.protein
      tmp_va_by_class[index] = mydri.vita
      tmp_fe_by_class[index] = mydri.fe
      tmp_vo_by_class[index] = mydri.max_vol
    context['dri_list_en'] = tmp_en_by_class
    context['dri_list_pr'] = tmp_pr_by_class
    context['dri_list_va'] = tmp_va_by_class
    context['dri_list_fe'] = tmp_fe_by_class
    context['dri_list_vo'] = tmp_vo_by_class

    tmp01 = FCT.objects.all()
    d = []
    for tmp02 in tmp01:
      dd = {}
      dd["selected_status"] = 0
      dd["Food_grp"] = tmp02.Food_grp_unicef
      dd["Food_name"] = tmp02.Food_name
      dd["Energy"] = tmp02.Energy
      dd["Protein"] = tmp02.Protein
      dd["VITA_RAE"] = tmp02.VITA_RAE
      dd["FE"] = tmp02.FE
      dd["Weight"] = 0
      dd["food_item_id"] = tmp02.food_item_id
      dd["portion_size"] = tmp02.portion_size_init
      dd["count_buy"] = 0
      dd["count_prod"] = 0
      dd["m1"] = 0
      dd["m2"] = 0
      dd["m3"] = 0
      dd["m4"] = 0
      dd["m5"] = 0
      dd["m6"] = 0
      dd["m7"] = 0
      dd["m8"] = 0
      dd["m9"] = 0
      dd["m10"] = 0
      dd["m11"] = 0
      dd["m12"] = 0
      # dd["myLocation"] = tmp02.myLocation_id
      d.append(dd)
    context["mylist_available"] = d

    context['nav_link1'] = reverse_lazy("crop_feas2_list")
    context['nav_text1'] = "list"
    context['nav_link2'] = ""
    context['nav_text2'] = "feasibility check"
    context['nav_link3'] = ""
    context['nav_text3'] = ""
    context["mark_text"] = 'quick feasibility assessment'
    context["stepid"] = 1000

    return context


class FCT_ListView(LoginRequiredMixin, ListView):
  model = FCT
  context_object_name = "mylist"
  template_name = 'myApp/FCT_list.html'

  def get_queryset(self):
    queryset = FCT.objects.filter(food_item_id__gte=800)
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user

    tmp_Param = SetURL(501, self.request.user)
    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class FCT_UpdateView(LoginRequiredMixin, UpdateView):
  model = FCT
  form_class = FCTForm
  template_name = 'myApp/FCT_form.html'
  success_url = reverse_lazy('fct_list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    return context


class FCT_CreateView(LoginRequiredMixin, CreateView):  # todo fail to register new record
  model = FCT
  form_class = FCTForm
  template_name = 'myApp/FCT_form.html'
  success_url = reverse_lazy('fct_list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    return context


class IndexView04(LoginRequiredMixin, TemplateView):
  template_name = "myApp/index04.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    context['myCountryName'] = Location.objects.filter(id=self.request.user.profile.myLocation).first().country

    tmp_Param = SetURL(500, self.request.user)
    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    return context


class Crop_Name_ListView(LoginRequiredMixin, ListView):
  model = Crop_Name
  context_object_name = "mylist"
  template_name = 'myApp/Crop_Name_list.html'

  def get_queryset(self):
    queryset = Crop_Name.objects.filter(myCountryName=self.kwargs['myCountryName'])
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    tmp_Param = SetURL(501, self.request.user)
    context['nav_link1'] = tmp_Param['back_URL']
    context['nav_text1'] = tmp_Param['back_Title']
    context['nav_link2'] = tmp_Param['main_URL']
    context['nav_text2'] = tmp_Param['main_Title']
    context['nav_link3'] = tmp_Param['forward_URL']
    context['nav_text3'] = tmp_Param['forward_Title']
    context["mark_text"] = tmp_Param['guide_text']
    context["stepid"] = tmp_Param['stepid']

    context['myuser'] = self.request.user
    context['myCountryName'] = self.kwargs['myCountryName']

    return context


class Crop_Name_CreateView(LoginRequiredMixin, CreateView):  # todo distinct country listで問題あり
  model = Crop_Name
  form_class = Crop_Name_Form
  template_name = 'myApp/Crop_Name_form.html'
  success_url = reverse_lazy('crop_name_list')

  def get_success_url(self):
    return reverse_lazy('crop_name_list', kwargs={'myCountryName': self.kwargs['myCountryName']})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    context['myCountryName'] = self.kwargs['myCountryName']
    return context

  def get_form_kwargs(self):
    kwargs = super(Crop_Name_CreateView, self).get_form_kwargs()

    # myCountryドロップダウンリスト用のデータ作成
    Country_list = []
    country_set = (
      self.kwargs['myCountryName'], Countries.objects.filter(GID_0=self.kwargs['myCountryName']).first().NAME_0)
    Country_list.append(country_set)

    # myFCTドロップダウンリスト用のデータ作成
    tmp_FCTs = FCT.objects.exclude(food_item_id__in=[x.myFCT_id for x in Crop_Name.objects.all()])
    myFCT_list = tuple((tmp_FCT.food_item_id, tmp_FCT.Food_name) for tmp_FCT in tmp_FCTs)
    logger.info(myFCT_list)

    # Food_grpドロップダウンリスト用のデータ作成
    tmp_Food_grps = FCT.objects.values_list('Food_grp_unicef', flat=True).distinct()
    Food_grp_list = tuple((tmp_Food_grp, tmp_Food_grp) for tmp_Food_grp in tmp_Food_grps)

    kwargs['Country_list'] = Country_list
    kwargs['FCT_list'] = myFCT_list
    kwargs['Food_grp_list'] = Food_grp_list
    return kwargs


class Crop_Name_UpdateView(LoginRequiredMixin, UpdateView):  # todo distinct country listで問題あり
  model = Crop_Name
  form_class = Crop_Name_Form
  template_name = 'myApp/Crop_Name_form.html'
  success_url = reverse_lazy('crop_name_list')

  def get_success_url(self):
    return reverse_lazy('crop_name_list', kwargs={'myCountryName': self.kwargs['myCountryName']})

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    context['myCountryName'] = self.kwargs['myCountryName']
    return context

  def get_form_kwargs(self):
    kwargs = super(Crop_Name_UpdateView, self).get_form_kwargs()

    # myCountryドロップダウンリスト用のデータ作成
    Country_list = []
    country_set = (
      self.kwargs['myCountryName'], Countries.objects.filter(GID_0=self.kwargs['myCountryName']).first().NAME_0)
    Country_list.append(country_set)

    # myFCTドロップダウンリスト用のデータ作成
    myFCT_list = []
    tmp_FCT = Crop_Name.objects.get(id=self.kwargs['pk']).myFCT
    FCT_set = (tmp_FCT.id, tmp_FCT.Food_name)
    myFCT_list.append(FCT_set)
    logger.info(myFCT_list)

    # Food_grpドロップダウンリスト用のデータ作成
    tmp_Food_grps = FCT.objects.values_list('Food_grp_unicef', flat=True).distinct()
    Food_grp_list = tuple((tmp_Food_grp, tmp_Food_grp) for tmp_Food_grp in tmp_Food_grps)

    kwargs['Country_list'] = Country_list
    kwargs['FCT_list'] = myFCT_list
    kwargs['Food_grp_list'] = Food_grp_list
    return kwargs


def change_location(request, myUser, myLocation):
  # myLocation = request.POST.get('myLocation')
  # count = request.POST['count']
  # myLocation = 0
  # if "row_id" in request.GET:
  # myLocation = int(request.GET["myLocation"])

  # myProfileの設定----------------------------------
  myUser = User.objects.get(id=myUser)
  key = myUser.profile
  key.myLocation = myLocation
  key.myTarget = 0
  key.myCrop = 0
  key.myDiet = 0
  key.save()
  logger.info("Profileを更新しました")

  myURL = reverse_lazy('Location_list')
  return redirect(myURL)


def SetURL(stepid, myUser):
  if stepid > 0:
    myLocation = myUser.profile.myLocation
    key = myUser.profile
    key.stepid = stepid
    key.save()
  myResult = {}
  main_URL = ""
  back_Title = ""
  main_Title = ""
  forward_Title = ""
  back_URL = ""
  forward_URL = ""

  if stepid == 0:
    back_Title = "back"
    main_Title = "menu"
    forward_Title = "step1"
    guide_text = 'please select your action'
    try:
      back_URL = reverse_lazy("index01")
      forward_URL = reverse_lazy("Location_list")
    except:
      logger.error('無効な値を参照しています')

  elif stepid == -1:
    back_Title = ""
    main_Title = "step0/8"
    forward_Title = "menu"
    guide_text = 'welcome to NFA tool! this tool help you to optimize diet and crop for selected beneficiaries'
    try:
      back_URL = ""
      forward_URL = reverse_lazy("index02")
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 100:
    back_Title = "menu"
    main_Title = "step1/8"
    forward_Title = "step2"
    guide_text = 'Here, you need to specify the location of your target area'
    try:
      back_URL = reverse_lazy("index02")
      forward_URL = reverse_lazy("person_list", kwargs={'myLocation': myLocation, 'page': 1})
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 200:
    back_Title = "step1"
    main_Title = "step2/8"
    forward_Title = "step3"
    guide_text = 'Here, you identify your target beneficiary in three level: individual, family, community'
    try:
      back_URL = reverse_lazy("Location_list")
      forward_URL = reverse_lazy("crop_select", kwargs={'myLocation': myLocation,
                                                        'myCountryName': Location.objects.filter(
                                                          id=myLocation).first().country})
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 300:
    back_Title = "step2"
    main_Title = "step3/8"
    forward_Title = "step4"
    guide_text = 'Here, you identify food item you ordinary see in target area'
    try:
      back_URL = reverse_lazy("person_list", kwargs={'myLocation': myLocation, 'page': 1})
      forward_URL = reverse_lazy("diet1", kwargs={'myLocation': myLocation})
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 400:
    back_Title = "step3"
    main_Title = "step4/8"
    forward_Title = "step5"
    guide_text = 'Here, you discuss about optimal combination of food item to satisfy nutrient needs of your target'
    try:
      back_URL = reverse_lazy("crop_select", kwargs={'myLocation': myLocation,
                                                     'myCountryName': Location.objects.filter(
                                                       id=myLocation).first().country})
      forward_URL = reverse_lazy("crop_feas_list")
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 500:
    back_Title = "step4"
    main_Title = "step5/8"
    forward_Title = "step6"
    guide_text = 'you can explore to introduce new food crop in target area'
    try:
      back_URL = reverse_lazy("diet1", kwargs={'myLocation': myLocation})
      forward_URL = reverse_lazy("crop_select", kwargs={'myLocation': myLocation,
                                                        'myCountryName': Location.objects.filter(
                                                          id=myLocation).first().country})
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 600:
    back_Title = "step5"
    main_Title = "step6/8"
    forward_Title = "step7"
    guide_text = 'Here, you set year-round availailibty of selected food item'
    try:
      back_URL = reverse_lazy("crop_feas_list")
      forward_URL = reverse_lazy("diet1", kwargs={'myLocation': myLocation})
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 700:
    back_Title = "step6"
    main_Title = "step7/8"
    forward_Title = "step8"
    guide_text = 'Here, you examine optimal combination of food item by making use of newly added food item'
    try:
      back_URL = reverse_lazy("crop_select", kwargs={'myLocation': myLocation,
                                                     'myCountryName': Location.objects.filter(
                                                       id=myLocation).first().country})
      forward_URL = reverse_lazy("output_list", kwargs={'myLocation': myLocation})
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 701:
    back_Title = "step4"
    main_Title = "step5/8"
    forward_Title = "step8"
    guide_text = 'Here, you examine feasibility of NDF you are going to introduce'
    try:
      back_URL = reverse_lazy("diet1", kwargs={'myLocation': myLocation})
      forward_URL = reverse_lazy("output_list", kwargs={'myLocation': myLocation})
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 800:
    back_Title = "step7"
    main_Title = "step8/8"
    forward_Title = ""
    guide_text = 'please select output you want to check'
    try:
      back_URL = reverse_lazy("diet1", kwargs={'myLocation': myLocation})
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 101:
    back_Title = ""
    main_Title = "step0/8"
    forward_Title = "menu"
    guide_text = 'Please indicate target area for your activity'
    try:
      back_URL = reverse_lazy("Location_list")
      forward_URL = ""
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 501:
    back_Title = "step4"
    main_Title = "step5/8"
    forward_Title = ""
    guide_text = 'you can explore to introduce new food crop in target area'
    try:
      back_URL = reverse_lazy("index04")
      forward_URL = ""
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 801:
    back_Title = "step8"
    main_Title = "output1"
    forward_Title = ""
    guide_text = 'this is nutrient balance for individual target'
    try:
      back_URL = reverse_lazy("output_list", kwargs={'myLocation': myLocation})
      forward_URL = ""
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 802:
    back_Title = "step8"
    main_Title = "output2"
    forward_Title = ""
    guide_text = 'this is nutrient balance for family target'
    try:
      back_URL = reverse_lazy("output_list",
                              kwargs={'myLocation': myLocation})
      forward_URL = ""
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 803:
    back_Title = "step8"
    main_Title = "output3"
    forward_Title = ""
    guide_text = 'this is crop calendar for target family'
    try:
      back_URL = reverse_lazy("output_list",
                              kwargs={'myLocation': myLocation})
      forward_URL = ""
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 804:
    back_Title = "step8"
    main_Title = "output4"
    forward_Title = ""
    guide_text = 'this is nutrient balance for target group'
    try:
      back_URL = reverse_lazy("output_list",
                              kwargs={'myLocation': myLocation})
      forward_URL = ""
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 805:
    back_Title = "step5"
    main_Title = "step8/8"
    forward_Title = ""
    guide_text = 'please select output you want to check'
    try:
      back_URL = reverse_lazy("crop_feas_list")
    except:
      logger.error('無効な値を参照しています')

  elif stepid == 1000:
    back_Title = "menu"
    main_Title = "instant mode"
    forward_Title = ""
    guide_text = 'diet nutrition calculator'
    try:
      back_URL = reverse_lazy("index01")
    except:
      logger.error('無効な値を参照しています')

  myResult['back_URL'] = back_URL
  myResult['back_Title'] = back_Title
  myResult['main_URL'] = main_URL
  myResult['main_Title'] = main_Title
  myResult['forward_URL'] = forward_URL
  myResult['forward_Title'] = forward_Title
  myResult["guide_text"] = guide_text
  myResult["stepid"] = stepid

  return myResult
