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

    def __init__(self, *args, **kwargs):
        self.myid = kwargs.pop('myid')
        super(LocationForm, self).__init__(*args, **kwargs)

    def clean_crop_list(self):
        d='0'
        if self.myid != '0':
            d = ''
            for crp in Crop.objects.filter(Locationid = self.myid):
                d += "-" + str(crp.food_item_id)
                if d[0] == '-':
                    d = d[1:]
        crop_list = d
        return crop_list
