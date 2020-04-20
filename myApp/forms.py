from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from .models import Location, Person, Profile, Crop_Feasibility, FCT
from django.contrib.auth.models import User


class LocationForm(forms.ModelForm):
  class Meta:
    model = Location
    fields = (
      "name", "country", "region", "province", "community",
      "AEZ_id", "stunting_rate", "wasting_rate", "anemia_rate"
    )
    widgets = {
      'country': forms.Select(attrs={'onchange': "selCnt();"}),
      'region': forms.Select(attrs={'onchange': "selSub1();"}),
      'province': forms.Select(),
      'AEZ_id': forms.HiddenInput(),
      'stunting_rate': forms.HiddenInput(),
      'wasting_rate': forms.HiddenInput(),
      'anemia_rate': forms.HiddenInput(),
    }
    labels = {
      "region": "Region",
      "province": "Zone",
      "community": "Woreda",
      "Location": "Kebele",
    }


class Person_Form(forms.ModelForm):
  class Meta:
    model = Person
    fields = ("myLocation", "nut_group", "target_pop", "myDRI",)
    widgets = {
      'myLocation': forms.HiddenInput(),
      'myDRI': forms.HiddenInput(),
    }

  def __init__(self, *args, **kwargs):
    self.myLocation = kwargs.pop('myLocation')
    super(Person_Form, self).__init__(*args, **kwargs)

  def clean(self):
    cleaned_data = super(Person_Form, self).clean()
    self.cleaned_data['myLocation'] = Location.objects.get(id=self.myLocation)

    return cleaned_data


class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username', 'is_staff')
    widgets = {
      'is_staff': forms.HiddenInput(),
    }

  def clean(self):
    cleaned_data = super(UserForm, self).clean()
    self.cleaned_data['is_staff'] = 1  # staffステータスの設定
    return cleaned_data


class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('organization', 'title')


class Crop_Feas_Form(forms.ModelForm):
  crop_name = forms.CharField(max_length=200)
  crop_name_id = forms.IntegerField()

  class Meta:
    model = Crop_Feasibility
    fields = (
      'crop_name', 'crop_name_id', 'feas_DRI_e', 'feas_DRI_p', 'feas_DRI_a', 'feas_DRI_f', 'feas_soc_acceptable',
      'feas_soc_acceptable_wo',
      'feas_soc_acceptable_c5', 'feas_prod_skill', 'feas_workload', 'feas_tech_service', 'feas_invest_fixed',
      'feas_invest_variable', 'feas_availability_prod', 'feas_availability_non', 'feas_affordability',
      'feas_storability', 'crop_score', 'myFCT', 'created_by')
    widgets = {
      'crop_score': forms.HiddenInput(),
      'myFCT': forms.HiddenInput(),
      'created_by': forms.HiddenInput(),
      'crop_name': forms.TextInput(attrs={'readonly': 'readonly'}),
      'crop_name_id': forms.HiddenInput(),
    }

  def clean(self):
    cleaned_data = super(Crop_Feas_Form, self).clean()
    self.cleaned_data['myFCT'] = FCT.objects.get(food_item_id=self.cleaned_data['crop_name_id'])
    self.cleaned_data['crop_score'] = int(self.cleaned_data['feas_DRI_e']) + int(
      self.cleaned_data['feas_DRI_p']) + int(self.cleaned_data['feas_DRI_a']) + int(
      self.cleaned_data['feas_DRI_f']) + int(self.cleaned_data['feas_soc_acceptable']) + int(
      self.cleaned_data['feas_soc_acceptable_c5']) + int(self.cleaned_data['feas_soc_acceptable_wo']) + int(
      self.cleaned_data['feas_prod_skill']) + int(self.cleaned_data['feas_workload']) + int(
      self.cleaned_data['feas_tech_service']) + int(
      self.cleaned_data['feas_invest_fixed']) + int(self.cleaned_data['feas_invest_variable']) + int(
      self.cleaned_data['feas_availability_prod']) + int(self.cleaned_data['feas_availability_non']) + int(
      self.cleaned_data['feas_affordability']) + int(self.cleaned_data['feas_storability'])

    return cleaned_data
