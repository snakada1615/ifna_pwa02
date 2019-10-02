from django import forms
from django.contrib.admin import widgets
from django.db.models import Q, Sum
from .models import Family, Person, DRI, DRI_women, Crop, FCT

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

class Person_Create_Form(forms.ModelForm):
    class Meta:
        model = Person
        fields = ("familyid", "name" ,"age", "sex", "women_s", "protein", "vita", "fe")
        widgets = {'name': forms.HiddenInput(),'familyid': forms.HiddenInput(),'protein': forms.HiddenInput(), 'vita': forms.HiddenInput(), 'fe': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.myid = kwargs.pop('myid')
        super(Person_Create_Form, self).__init__(*args, **kwargs)

    def clean_familyid(self):
        familyid = self.myid
        return familyid

    def clean_name(self):
        name = Family.objects.get(id = self.myid).name
        return name

    def clean_women_s(self):
        a = self.cleaned_data['women_s']
        if self.cleaned_data['sex'] == 1:
            a = 0
        women_s = a
        return women_s

    def clean_protein(self):
        a = int(self.cleaned_data['age'])
        b = int(self.cleaned_data['women_s'])
        v1 = DRI.objects.get(age_id = a)
        if self.cleaned_data['sex'] == 1:
            protein = v1.male_protain
        else:
            try:
                v2 = DRI_women.objects.get(status = b)
                protein = v1.female_protain + v2.female_prot2
            except:
                protein = v1.female_protain
        return protein

    def clean_vita(self):
        a = int(self.cleaned_data['age'])
        b = int(self.cleaned_data['women_s'])
        v1 = DRI.objects.get(age_id = a)
        if self.cleaned_data['sex'] == 1:
            vita = v1.male_vitA
        else:
            try:
                v2 = DRI_women.objects.get(status = b)
                vita = v2.female_vit2
            except:
                vita = v1.female_vitA
        return vita

    def clean_fe(self):
        a = int(self.cleaned_data['age'])
        b = int(self.cleaned_data['women_s'])
        v1 = DRI.objects.get(age_id = a)
        if self.cleaned_data['sex'] == 1:
            fe = v1.male_fe
        else:
            try:
                v2 = DRI_women.objects.get(status = b)
                if v2.female_fe2 == 0:
                    fe = v1.female_fe
                else:
                    fe = v2.female_fe2
            except:
                fe = v1.female_fe
        return fe

class CropForm(forms.ModelForm):

    class Meta:
        model = Crop
        fields = ("familyid", "Food_name", "feas_DRI", "feas_soc_acceptable",
            "feas_prod_skill", "feas_tech_service", "feas_invest_fixed",
            "feas_invest_variable", "feas_availability",
            "diet_type", "food_item_id", "protein", "vita", "fe"
            )
        widgets = {
            'familyid': forms.HiddenInput(),
            'diet_type': forms.RadioSelect(),
            'food_item_id': forms.HiddenInput(),
            'protein': forms.HiddenInput(),
            'vita': forms.HiddenInput(),
            'fe': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.myid = kwargs.pop('myid')
        super(CropForm, self).__init__(*args, **kwargs)
        myquery = FCT.objects.all()
        self.fields['Food_name'] = forms.ModelChoiceField(queryset=myquery, empty_label='select food', to_field_name='Food_name')

    def clean(self):
        cleaned_data = super(CropForm, self).clean()
        myfood = FCT.objects.get(Food_name = self.cleaned_data['Food_name'])
        self.cleaned_data['food_item_id'] = myfood.food_item_id
        self.cleaned_data['protein'] = myfood.Protein
        self.cleaned_data['vita'] = myfood.VITA_RAE
        self.cleaned_data['fe'] = myfood.FE
        self.cleaned_data['familyid'] = self.myid
        return cleaned_data
