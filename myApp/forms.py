from django import forms
from django.contrib.admin import widgets
from django.db.models import Q, Sum
from .models import Family

Choice_FoodGrp = {
    ('0','food name'),
    ('1','protein'),
    ('2','iron'),
    ('3','Vitamine-A'),
}

class BS4RadioSelect(forms.RadioSelect):
    input_type = 'radio'
    template_name = 'myApp/widgets/bs4_radio.html'


class Order_Key_Form(forms.Form):
    key1 = forms.ChoiceField(
        label='Order_key',
        widget=BS4RadioSelect,
        choices= Choice_FoodGrp,
        initial=1,
        )

class FamilyForm(forms.ModelForm):

    class Meta:
        model = Family
        fields = ("name", "remark")
