from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from .models import Location, Person, Profile

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = (
            "name", "country", "region", "province", "community",
            "AEZ_id", "stunting_rate", "wasting_rate", "anemia_rate"
        )
        widgets = {
            'country': forms.Select(attrs = {'onchange' : "selCnt();"}),
            'region': forms.Select(attrs = {'onchange' : "selSub1();"}),
            'province': forms.Select(),
            'AEZ_id': forms.HiddenInput(),
            'stunting_rate': forms.HiddenInput(),
            'wasting_rate': forms.HiddenInput(),
            'anemia_rate': forms.HiddenInput(),
        }
        labels = {
            "region":"Region",
            "province":"Zone",
            "community":"Woreda",
            "Location":"Kebele",
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
    fields = ('first_name', 'last_name', 'username')


class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('organization', 'title')
