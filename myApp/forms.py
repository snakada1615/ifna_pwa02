from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.db.models import Q, Sum # 集計関数の追加
from django.db.models import Max  # 集計関数の追加
from .models import Location, Person, Profile, Crop_Feasibility, FCT, Crop_SubNational, Countries, Crop_Name
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# logging用の設定
from logging import getLogger

logger = getLogger(__name__)


class LocationForm(forms.ModelForm):
  class Meta:
    logger.debug('Metaまで来てるのか？')
    model = Location
    fields = (
      "country", "region", "province", "community", "name",
      "AEZ_id", "stunting_rate", "wasting_rate", "anemia_rate", "myCountry", "created_by"
    )
    widgets = {
      'country': forms.Select(attrs={'onchange': "selCnt();", 'required': 'required'}),
      'region': forms.Select(attrs={'onchange': "selSub1();", 'required': 'required'}),
      'province': forms.Select(attrs={'onchange': "selSub2();", 'required': 'required'}),
      'community': forms.Select(attrs={'required': 'required'}),
      'AEZ_id': forms.HiddenInput(),
      'stunting_rate': forms.HiddenInput(),
      'wasting_rate': forms.HiddenInput(),
      'anemia_rate': forms.HiddenInput(),
      'myCountry': forms.HiddenInput(),
      'created_by': forms.HiddenInput(),
    }
    labels = {
      "region": "Region",
      "province": "Zone",
      "community": "Woreda",
      "Location": "Kebele",
      "name": "village or other",
    }

  def clean(self):
    cleaned_data = super(LocationForm, self).clean()
    has_country = False
    if 'country' in cleaned_data and cleaned_data['country'] != '':
      country = Countries.objects.filter(GID_0=cleaned_data['country'])
      if len(country) == 0:
        raise ValidationError({'country': [_('Your input for %(field_name)s is invalid.') % {'field_name': _('Country')}]})
      has_country = True

    has_region = False
    if ('region' in cleaned_data and cleaned_data['region'] != '') and has_country:
      region = Countries.objects.filter(GID_0=cleaned_data['country'], GID_1=cleaned_data['region'])
      if len(region) == 0:
        raise ValidationError({'region': [_('Your input for %(field_name)s is invalid.') % {'field_name': _('Region')}]})
      has_region = True

    has_province = False
    if ('province' in cleaned_data and cleaned_data['province'] != '') and has_country and has_region:
      province = Countries.objects.filter(GID_0=cleaned_data['country'], GID_1=cleaned_data['region'],
                                          GID_2=cleaned_data['province'])
      if len(province) == 0:
        raise ValidationError({'province': [_('Your input for %(field_name)s is invalid.') % {'field_name': _('Zone')}]})
      has_province = True
    if ('community' in cleaned_data and cleaned_data[
      'community'] != '') and has_country and has_region and has_province:
      community = Countries.objects.filter(GID_0=cleaned_data['country'], GID_1=cleaned_data['region'],
                                          GID_2=cleaned_data['province'], GID_3=cleaned_data['community'])
      if len(community) == 0:
        raise ValidationError({'community': [_('Your input for %(field_name)s is invalid.') % {'field_name': _('Woreda')}]})

    return cleaned_data


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


class PersonListForm(forms.Form):

  SCOPE_FAMILY = 2
  SCOPE_COMMUNITY = 3

  def __init__(self, *args, **kwargs):
    super(PersonListForm, self).__init__(*args, **kwargs)

  def clean(self):
    cleaned_data = super(PersonListForm, self).clean()
    my_json = self.data['myJson']
    for index, row in enumerate(my_json):
      nut_group = int(row['nut_group_id']) - 1
      key = '#inpNum_fam%d' % (nut_group) if int(row['target_scope']) == self.SCOPE_FAMILY else '#inpNum%d' % (nut_group)
      field = forms.IntegerField(required=True, min_value=0)
      self.fields.update({key: field})
      try:
        field.clean(row['target_pop'])
      except ValidationError as ex:
        self.add_error(key, ex.messages)

    # validate total pop
    my_data_pop = self.data['dataPop']
    for value, index in enumerate(my_data_pop):
      field = forms.IntegerField(required=True, min_value=1)
      self.fields.update({
        index: field
      })
      try:
        field.clean(my_data_pop[index])
      except ValidationError as ex:
        self.add_error(index, ex.messages)
    return cleaned_data


class UserEditForm(UserChangeForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username')


class UserCreateForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name',
              'username', 'password1', 'password2', 'is_staff')
    widgets = {
      'is_staff': forms.HiddenInput(),
    }

  def clean(self):
    cleaned_data = super(UserCreateForm, self).clean()
    self.cleaned_data['is_staff'] = 1  # staffステータスの設定
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

  def __init__(self, *args, **kwargs):
    self.user = kwargs.pop('user')
    super(Crop_Feas_Form, self).__init__(*args, **kwargs)

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
    labels = {
      "feas_DRI_e": "Is required amount for energy target feasible?",
      "feas_DRI_p": "Is required amount for protein target feasible?",
      "feas_DRI_a": "Is required amount for vit-A target feasible?",
      "feas_DRI_f": "Is required amount for Iron target feasible?",
      "feas_soc_acceptable": "Is there any social bariier to consume this commodity in general?",
      "feas_soc_acceptable_wo": "Is there any social barrier to consume this commodity for women?",
      "feas_soc_acceptable_c5": "Is there any social barrier to consume this commodity for child?",
      "feas_prod_skill": "do target beneficiary have enough skill to grow this commodity?",
      "feas_workload": "Does this commodity imply incremental workload for women?",
      "feas_tech_service": "Is technical service available for this commodity?",
      "feas_invest_fixed": "Is there need for specific infrastructure (irrigation / postharvest, etc.)?",
      "feas_invest_variable": "Is production input (fertilizer, seed, feed) become financial burden for small farmer?",
      "feas_availability_non": "How many month is this commodity NOT available in a year?",
      "feas_availability_prod": "How many month can you harvest this commodity in a year?",
      "feas_affordability": "Is this commodity affordable in the market for ordinary population?",
      "feas_storability": "Are there any feasible storage medhod available for this commodity?",
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

    logger.info(self.cleaned_data['crop_score'])
    logger.info(self.cleaned_data['myFCT'])
    for ele in self.cleaned_data:
      logger.info(ele)

    # add to Crop_subnational if score is over 35
    if self.cleaned_data['crop_score'] >= 35:
      logger.info('high score')
      Crop_SubNational.objects.update_or_create(
        myLocation=Location.objects.get(id=self.user.profile.myLocation),
        myFCT=self.cleaned_data['myFCT'],
        defaults={
          'selected_status': '0',
          'created_by': self.user
        }
      )
    else:
      logger.info('low score')
      Crop_SubNational.objects.filter(
        myLocation=Location.objects.get(id=self.user.profile.myLocation)).filter(
        myFCT=self.cleaned_data['myFCT']
      ).delete()

    return cleaned_data


class FCTForm(forms.ModelForm):
  class Meta:
    model = FCT
    fields = (
      'Food_grp', 'Food_name', 'Energy', 'WATER', 'Protein', 'Fat', 'Carbohydrate', 'Fiber', 'ASH', 'CA',
      'FE', 'MG', 'P', 'K', 'NA', 'ZN', 'CU', 'VITA_RAE', 'RETOL', 'B_Cart_eq', 'VITD', 'VITE', 'THIA', 'RIBF',
      'NIA', 'VITB6C', 'FOL', 'VITB12', 'VITC', 'FCT_id', 'food_item_id', 'Crop_ref'
    )
    widgets = {
      'FCT_id': forms.HiddenInput(),
      'food_item_id': forms.HiddenInput(),
      'Crop_ref': forms.HiddenInput(),
    }

  def clean(self):
    cleaned_data = super(FCTForm, self).clean()
    self.cleaned_data['Crop_ref'] = 0  # staffステータスの設定
    if self.cleaned_data['food_item_id'] > 0:
      i = 0  # dummy
    else:
      self.cleaned_data['food_item_id'] = FCT.objects.aggregate(Max('food_item_id'))['food_item_id__max'] + 1
      self.cleaned_data['FCT_id'] = FCT.objects.aggregate(Max('FCT_id'))['FCT_id__max'] + 1
    return cleaned_data


class Crop_Name_Form(forms.ModelForm):
  #set queryset
  # Food_grp = forms.ModelChoiceField(label='local food group',
  #                           queryset=FCT.objects.values_list('Food_grp_unicef', flat=True).distinct())
  Food_grp = forms.ChoiceField(label='local food group')
  myCountry = forms.ChoiceField(label='country name')
  myFCT = forms.ChoiceField(label='FAO defined food name')

  def __init__(self, *args, **kwargs):
    self.Country_list = kwargs.pop('Country_list', None)
    self.FCT_list = kwargs.pop('FCT_list', None)
    self.Food_grp_list = kwargs.pop('Food_grp_list', None)
    super(Crop_Name_Form, self).__init__(*args, **kwargs)

    self.fields['myCountry'].choices = self.Country_list
    self.fields['myFCT'].choices = self.FCT_list
    self.fields['Food_grp'].choices = self.Food_grp_list

  class Meta:
    model = Crop_Name
    fields = ('myCountry', 'myFCT', 'Food_grp', 'Food_name')
    labels = {
      "Food_name": "local food name",
    }


  def clean(self):
    cleaned_data = super(Crop_Name_Form, self).clean()
    logger.info(self.cleaned_data['Food_grp'])
    self.cleaned_data['myFCT'] = FCT.objects.get(food_item_id=self.cleaned_data['myFCT'])
    self.cleaned_data['myCountry'] = Countries.objects.get(id=self.cleaned_data['myCountry'])

    return cleaned_data




