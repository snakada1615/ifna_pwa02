from django import forms
from django.contrib.admin import widgets
from django.db.models import Q, Sum
from .models import Location


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
            "province":"Woreda",
            "Location":"Kebele",
        }
