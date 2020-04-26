# to get all the models in myApp
from django.apps import apps
from django.contrib import admin

# immport messaging framework
from django.contrib import messages

# import receiver
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import re
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
from django.http.response import JsonResponse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import LocationForm, Person_Form, UserForm, ProfileForm, Crop_Feas_Form
from .forms import UserEditForm, UserCreateForm, FCTForm

from .models import Location, Countries, Crop_National, Crop_SubNational
from .models import FCT, DRI, Crop_Feasibility, Crop_Individual, Person, Pop, Crop_Name

# for user registration
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login
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


class IndexView(TemplateView):
  template_name = "myApp/index01.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    messages.error(
      self.request,
      "this application is currently under development. user input data may be lost due to update"
    )
    #    context['message_dont_close'] = "true"
    return context


class Under_Construction_View(TemplateView):
  template_name = "myApp/under_construction.html"


class aboutNFA(TemplateView):
  template_name = "myApp/whatisNFA.html"


class IndexView02(LoginRequiredMixin, TemplateView):
  template_name = "myApp/index02.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    keys_all = self.request.user.profile
    data = {
      'myLocation': keys_all.myLocation,
      'myCrop': keys_all.myCrop,
      'myTarget': keys_all.myTarget,
      'myDiet': keys_all.myDiet,
    }
    json_str = json.dumps(data)
    context['myParam'] = json_str
    context['myuser'] = self.request.user

    return context


class Location_ListView(LoginRequiredMixin, ListView):
  model = Location
  context_object_name = "mylist"
  template_name = 'myApp/Location_list.html'

  def get_queryset(self):
    queryset = super().get_queryset().filter(created_by=self.request.user)
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myuser'] = self.request.user
    context['myLocation'] = self.request.user.profile.myLocation
    return context


@transaction.atomic
def create_user_profile(request):
  if request.method == 'POST':
    user_form = UserCreateForm(request.POST)
    # profile_form = ProfileForm(request.POST)
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
      GID_2=form.instance.province).first()
    form.instance.AEZ_id = form.instance.myCountry.AEZ_id
    form.instance.created_by = User.objects.get(id=self.request.user.id)
    return super(Location_CreateView, self).form_valid(form)

  def get_context_data(self, **kwargs):
    data = Countries.objects.all()
    context = super().get_context_data(**kwargs)
    context['countries'] = serializers.serialize('json', data)
    context['coutry_selected'] = ''
    context['region_selected'] = ''
    context['province_selected'] = ''
    context['myuser'] = self.request.user
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
    context['coutry_selected'] = myLocation.country
    context['region_selected'] = myLocation.region
    context['province_selected'] = myLocation.province
    context['myuser'] = self.request.user
    return context

  def form_invalid(self, form):
    res = super().form_invalid(form)
    res.status_code = 400
    return res

  def form_valid(self, form):
    form.instance.myCountry = Countries.objects.filter(
      GID_2=form.instance.province).first()
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

        # --------------------update Crop_SubNational-------------------------
        logger.info("これからCrop＿SubNationaを追加していきます")
        tmp_aez = Countries.objects.filter(GID_2=instance.province).first().AEZ_id
        instance.AEZ_id = tmp_aez
        tmp01 = Crop_National.objects.filter(AEZ_id=tmp_aez)
        if tmp01.count() != 0:
          logger.info("Crop＿Natinalの中に該当品目が存在しています")
          for tmp02 in tmp01:
            keys = {}
            keys['myLocation'] = Location.objects.get(id=instance.pk)
            keys['myFCT'] = FCT.objects.get(food_item_id=tmp02.myFCT.food_item_id)
            keys['selected_status'] = 0
            keys['created_by'] = User.objects.get(id=instance.created_by.id)
            p = Crop_SubNational.objects.create(**keys)
          logger.info("全ての該当品目をCrop_SubNationalに書き込みました!")

        # --------------------update myTarget-community-------------------------
        nut_grp_list = ['child 0-23 month', 'child 24-59 month', 'child 6-9 yr', 'adolescent all',
                        'adolescent pregnant',
                        'adolescent lact', 'adult', 'adult pregnant', 'adult lact']
        logger.info("これからTarget communityの人口構成、初期値を追加していきます")
        for i in range(9):
          Person.objects.create(
            myLocation=Location.objects.get(id=instance.pk),
            nut_group=nut_grp_list[i],
            target_scope=3,
            target_pop=100,
            created_by=instance.created_by,
            myDRI=DRI.objects.get(nut_group=nut_grp_list[i])
          )
        logger.info("Target communityの書込み終了")
        # ---------------------
  else:  # 新規レコードの場合

    # --------------------update Crop_SubNational-------------------------
    tmp_aez = Countries.objects.filter(GID_2=instance.province).first().AEZ_id
    instance.AEZ_id = tmp_aez
    tmp01 = Crop_National.objects.filter(AEZ_id=tmp_aez)
    logger.info("これからCrop＿SubNationaを追加していきます")
    if tmp01.count() != 0:
      logger.info("Crop＿Natinalの中に該当品目が存在しています")
      for tmp02 in tmp01:
        keys = {}
        keys['myLocation'] = Location.objects.get(id=instance.pk)
        keys['myFCT'] = FCT.objects.get(food_item_id=tmp02.myFCT.food_item_id)
        keys['selected_status'] = 0
        keys['created_by'] = User.objects.get(id=instance.created_by.id)
        p = Crop_SubNational.objects.create(**keys)
      logger.info("全ての該当品目をCrop_SubNationalに書き込みました!")

    # --------------------update myTarget-community-------------------------
    nut_grp_list = ['child 0-23 month', 'child 24-59 month', 'child 6-9 yr', 'adolescent all', 'adolescent pregnant',
                    'adolescent lact', 'adult', 'adult pregnant', 'adult lact']
    logger.info("これからTarget communityの人口構成、初期値を追加していきます")
    for i in range(9):
      Person.objects.create(
        myLocation=Location.objects.get(id=instance.pk),
        nut_group=nut_grp_list[i],
        target_scope=3,
        target_pop=100,
        created_by=User.objects.get(id=instance.created_by.id),
        myDRI=DRI.objects.get(nut_group=nut_grp_list[i])
      )
    logger.info("Target communityの書込み終了")
    # ---------------------


class CropSelect(LoginRequiredMixin, TemplateView):  # todo まだ縦横表示がおかしいです
  template_name = "myApp/crop_available.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    # send filtered crop by AEZ ######
    tmp01 = Crop_SubNational.objects.filter(myLocation=self.kwargs['myLocation'])
    myUser = self.request.user
    tmp_country_crops = Crop_Name.objects.filter(myCountry_id=myUser.profile.myLocation)

    d = []
    for tmp02 in tmp01:
      dd = {}
      dd["selected_status"] = tmp02.selected_status
      dd["Food_grp"] = tmp02.myFCT.Food_grp
      dd["Food_name"] = tmp02.myFCT.Food_name
      if len(tmp_country_crops) != 0:
        tmp_country = tmp_country_crops.filter().first()
        if len(tmp_country) != 0:
          dd["Food_grp"] = tmp02.myFCT.Food_grp
          dd["Food_name"] = tmp02.myFCT.Food_name
      dd["food_item_id"] = tmp02.myFCT.food_item_id
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

    return context


def registCropAvail(request):
  # json_str = request.body.decode("utf-8")
  json_data = json.loads(request.body)
  tmp_myLocation_id = 0
  tmp_newcrop_list = []

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

    tmp_myLocation_id = myrow['myLocation']  # 後で使う(part 2)
    tmp_newcrop_list.append(myrow['myFCT_id'])  # 後で使う(part 2)

    tmp = Crop_SubNational.objects.filter(myFCT_id=myrow['myFCT_id']).filter(
      myLocation_id=tmp_myLocation_id
    )
    p = tmp.update(**newcrop)

  # (part 2) delete non-selected records
  tmp = Crop_SubNational.objects.filter(myLocation_id=tmp_myLocation_id)
  for rec in tmp:
    if int(rec.myFCT.food_item_id) not in tmp_newcrop_list:
      rec.selected_status = 0
      rec.save()

  # myStatusの設定
  key = request.user.profile
  key.myTarget = 0
  key.myCrop = 1
  key.myDiet = 0
  key.save()

  myURL = reverse_lazy('index02')
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

    tmpClass1 = 0
    tmpClass2 = 0
    tmpClass3 = 0
    tmpClass_sum = 0
    tmpPersons = Person.objects.filter(myLocation=self.kwargs['myLocation'])
    for tmpPerson in tmpPersons:
      if tmpPerson.target_scope == 1:
        tmpClass1 = 1
      if tmpPerson.target_scope == 2:
        tmpClass2 = 1
      if tmpPerson.target_scope == 3:
        tmpClass3 = 1
    tmpClass_sum = 100 * tmpClass1 + 10 * tmpClass2 + tmpClass3

    context['mytarget_scope_Sum'] = tmpClass_sum
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    context['myuser'] = self.request.user
    context['page'] = self.kwargs['page']

    myPop = Pop.objects.filter(GID_0=Location.objects.get(id=self.kwargs['myLocation']).country)
    dd = {}
    dd['class0'] = myPop.get(Age_class_id=0).share_Pop
    dd['class1'] = myPop.get(Age_class_id=1).share_Pop
    dd['class2'] = myPop.get(Age_class_id=2).share_Pop
    dd['class3'] = myPop.get(Age_class_id=3).share_Pop
    dd['class3_p'] = myPop.get(Age_class_id=3).share_Preg
    dd['class3_l'] = myPop.get(Age_class_id=3).share_BF
    dd['class4'] = myPop.get(Age_class_id=4).share_Pop
    dd['class5'] = myPop.get(Age_class_id=5).share_Pop
    dd['class5_p'] = myPop.get(Age_class_id=5).share_Preg
    dd['class5_l'] = myPop.get(Age_class_id=5).share_BF
    dd['class6'] = myPop.get(Age_class_id=6).share_Pop
    context['myPop'] = dd
    context['myReturnURL'] = reverse_lazy('index01')

    myPerson = Person.objects.filter(myLocation=self.kwargs['myLocation']).filter(target_scope=3);
    dd = {}
    dd['class0'] = myPerson.get(nut_group='child 0-23 month').target_pop
    dd['class1'] = myPerson.get(nut_group='child 24-59 month').target_pop
    dd['class2'] = myPerson.get(nut_group='child 6-9 yr').target_pop
    dd['class3'] = myPerson.get(nut_group='adolescent all').target_pop
    dd['class4'] = myPerson.get(nut_group='adolescent pregnant').target_pop
    dd['class5'] = myPerson.get(nut_group='adolescent lact').target_pop
    dd['class6'] = myPerson.get(nut_group='adult').target_pop
    dd['class7'] = myPerson.get(nut_group='adult pregnant').target_pop
    dd['class8'] = myPerson.get(nut_group='adult lact').target_pop
    context['myCommunity'] = dd

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
  # json_str = request.body.decode("utf-8")
  json_data = json.loads(request.body)
  nut_grp_list = ['child 0-23 month', 'child 24-59 month', 'child 6-9 yr', 'adolescent all', 'adolescent pregnant',
                  'adolescent lact', 'adult', 'adult pregnant', 'adult lact']

  for myrow in json_data['myJson']:
    # 最初に参照するキー（複数可）を指定する
    # defaultsで指定した列・値で更新する
    tmp_group = nut_grp_list[int(myrow['nut_group_id']) - 1]
    Person.objects.update_or_create(
      myLocation=Location.objects.get(id=myrow['myLocation']),
      nut_group=tmp_group,
      target_scope=3,
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

  myURL = reverse_lazy('index02')
  return JsonResponse({
    'success': True,
    'url': myURL,
  })


class Diet_Plan1(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Diet_Plan.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation'])
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

    # send selected crop by community ######
    tmp01 = Crop_SubNational.objects.filter(myLocation_id=self.kwargs['myLocation']).filter(selected_status__gt=0)
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
      d.append(dd)
    context["mylist_available"] = d

    # send selected crop by community ######
    # --------------------create 16 Crop_individual-------------------------
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation'])
    myRange = [101, 102, 103, 104, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212]
    d = []
    for i in myRange:
      tmp02 = tmp01.filter(id_table=i)
      if tmp02.count() == 0:
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
        dd["myid_tbl"] = i
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
          dd["myid_tbl"] = tmp03.id_table
          d.append(dd)
    context["mylist_selected"] = d

    context['myuser'] = self.request.user

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
  tmp_newcrop_list = []

  for myrow in json_data['myJson']:
    # 最初に参照するキー（複数可）を指定する
    # defaultsで指定した列・値で更新する
    Crop_Individual.objects.update_or_create(
      id_table=int(myrow['myid_tbl']),
      myFCT=FCT.objects.get(food_item_id=myrow['food_item_id']),
      defaults={
        'myLocation': Location.objects.get(id=myrow['myLocation']),
        'target_scope': int(myrow['target_scope']),
        'created_by': request.user,
        'month': int(myrow['month']),
        'total_weight': int(myrow['total_weight']),
        'portion_size': int(myrow['portion_size']),
        'count_prod': int(myrow['count_prod']),
        'count_buy': int(myrow['count_buy'])
      }
    )

  # update myStatus
  key = request.user.profile
  key.myDiet = 1
  key.save()

  myURL = reverse_lazy('index02')
  return JsonResponse({
    'success': True,
    'url': myURL,
  })


class Output1(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output1.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation'])
    context['nutrient_target'] = tmp_nut_group[0].nut_group

    tmp_nut_group1 = tmp_nut_group.filter(target_scope=1)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    for tmp in tmp_nut_group1:
      tmp_e += tmp.myDRI.energy
      tmp_p += tmp.myDRI.protein
      tmp_v += tmp.myDRI.vita
      tmp_p += tmp.myDRI.fe
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
      tmp_p += tmp.myDRI.fe
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
      tmp_p += tmp.myDRI.fe
    context['dri_e3'] = tmp_e
    context['dri_p3'] = tmp_p
    context['dri_v3'] = tmp_v
    context['dri_f3'] = tmp_f

    # send selected crop by community ######
    # --------------------create 16 Crop_individual-------------------------
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation'])
    myRange = [101, 102, 103, 104]
    d = []
    for i in myRange:
      tmp02 = tmp01.filter(id_table=i)
      if tmp02.count() == 0:
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
        dd["myid_tbl"] = i
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
          dd["myid_tbl"] = tmp03.id_table
          d.append(dd)
    context["mylist_selected"] = d

    context['myuser'] = self.request.user

    return context


class Output2(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output2.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation'])
    context['nutrient_target'] = tmp_nut_group[0].nut_group

    tmp_nut_group1 = tmp_nut_group.filter(target_scope=1)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    for tmp in tmp_nut_group1:
      tmp_e += tmp.myDRI.energy
      tmp_p += tmp.myDRI.protein
      tmp_v += tmp.myDRI.vita
      tmp_p += tmp.myDRI.fe
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
      tmp_p += tmp.myDRI.fe
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
      tmp_p += tmp.myDRI.fe
    context['dri_e3'] = tmp_e
    context['dri_p3'] = tmp_p
    context['dri_v3'] = tmp_v
    context['dri_f3'] = tmp_f

    # send selected crop by community ######
    # --------------------create 16 Crop_individual-------------------------
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation'])
    myRange = [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212]
    d = []
    for i in myRange:
      tmp02 = tmp01.filter(id_table=i)
      if tmp02.count() == 0:
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
        dd["myid_tbl"] = i
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
          dd["myid_tbl"] = tmp03.id_table
          d.append(dd)
    context["mylist_selected"] = d

    context['myuser'] = self.request.user

    return context


class Output3(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output3.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation'])
    context['nutrient_target'] = tmp_nut_group[0].nut_group

    tmp_nut_group1 = tmp_nut_group.filter(target_scope=1)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    for tmp in tmp_nut_group1:
      tmp_e += tmp.myDRI.energy
      tmp_p += tmp.myDRI.protein
      tmp_v += tmp.myDRI.vita
      tmp_p += tmp.myDRI.fe
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
      tmp_p += tmp.myDRI.fe
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
      tmp_p += tmp.myDRI.fe
    context['dri_e3'] = tmp_e
    context['dri_p3'] = tmp_p
    context['dri_v3'] = tmp_v
    context['dri_f3'] = tmp_f

    # send selected crop by community ######
    # --------------------create 16 Crop_individual-------------------------
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation'])
    myRange = [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212]
    d = []
    for i in myRange:
      tmp02 = tmp01.filter(id_table=i)
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

    return context


class Output4(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output4.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
    tmp_nut_group = Person.objects.filter(
      myLocation=self.kwargs['myLocation'])
    context['nutrient_target'] = tmp_nut_group[0].nut_group

    tmp_nut_group1 = tmp_nut_group.filter(target_scope=1)
    tmp_e = 0
    tmp_p = 0
    tmp_v = 0
    tmp_f = 0
    for tmp in tmp_nut_group1:
      tmp_e += tmp.myDRI.energy
      tmp_p += tmp.myDRI.protein
      tmp_v += tmp.myDRI.vita
      tmp_p += tmp.myDRI.fe
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
      tmp_p += tmp.myDRI.fe
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
      tmp_p += tmp.myDRI.fe
    context['dri_e3'] = tmp_e
    context['dri_p3'] = tmp_p
    context['dri_v3'] = tmp_v
    context['dri_f3'] = tmp_f

    # send selected crop by community ######
    # --------------------create 16 Crop_individual-------------------------
    tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation'])
    myRange = [301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312]
    d = []
    for i in myRange:
      tmp02 = tmp01.filter(id_table=i)
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

    return context


class Output_list(LoginRequiredMixin, TemplateView):
  template_name = "myApp/Output_list.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['myLocation'] = self.kwargs['myLocation']
    context['myuser'] = self.request.user
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

    # send non-available crop in the original list ######
    tmp01 = Crop_SubNational.objects.filter(myLocation_id=self.request.user.profile.myLocation)
    available_list = []
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
    return context

  def form_valid(self, form):
    self.object = form.save()
    form.instance.created_by = self.request.user
    form.instance.myLocation = Location.objects.get(id=self.request.user.profile.myLocation)
    return super(Crop_Feas_CreateView, self).form_valid(form)


class Crop_Feas_ListView(LoginRequiredMixin, ListView):
  model = Crop_Feasibility
  context_object_name = "mylist"
  template_name = 'myApp/Crop_Feas_list.html'

  def get_queryset(self):
    queryset = super().get_queryset().filter(created_by=self.request.user).filter(
      myLocation=self.request.user.profile.myLocation)
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['isUpdate'] = 0
    context['myuser'] = self.request.user
    context['myLocation'] = self.request.user.profile.myLocation
    context['myLocation_name'] = Location.objects.get(id=self.request.user.profile.myLocation).name
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

  def get_context_data(self, **kwargs):  # todo 無意味なcrop_listの送信をやめる
    context = super().get_context_data(**kwargs)
    context['isUpdate'] = 1
    context['myuser'] = self.request.user
    context['myLocation'] = self.request.user.profile.myLocation
    context['crop_name'] = Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.Food_name
    context['crop_name_id'] = Crop_Feasibility.objects.get(id=self.kwargs['pk']).myFCT.food_item_id
    context['myLocation_name'] = Location.objects.get(id=self.request.user.profile.myLocation).name

    # send non-available crop in the original list 無意味なのですが######
    tmp01 = Crop_SubNational.objects.filter(myLocation_id=self.request.user.profile.myLocation)
    available_list = []
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
    return context


class FCT_ListView(LoginRequiredMixin, ListView):
  model = FCT
  context_object_name = "mylist"
  template_name = 'myApp/FCT_list.html'

  def get_queryset(self):
    queryset = FCT.objects.filter(food_item_id__gte=800)
    return queryset


class FCT_UpdateView(LoginRequiredMixin, UpdateView):
  model = FCT
  form_class = FCTForm
  template_name = 'myApp/FCT_form.html'
  success_url = reverse_lazy('fct_list')


class FCT_CreateView(LoginRequiredMixin, CreateView):  # todo fail to register new record
  model = FCT
  form_class = FCTForm
  template_name = 'myApp/FCT_form.html'
  success_url = reverse_lazy('fct_list')


class IndexView04(LoginRequiredMixin, TemplateView):
  template_name = "myApp/index04.html"
