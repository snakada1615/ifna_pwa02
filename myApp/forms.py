from django import forms
from django.contrib.admin import widgets
from django.db.models import Q, Sum
from .models import Family, Person, DRI, DRI_women, Crop, FCT

Choice_FoodGrp = {
    ('0','food name'),
    ('1','protein'),
    ('2','iron'),
    ('3','Vitamin-A'),
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
        fields = (
            "name", "remark", "country", "region", "province", "community",
            "wasting_rate", "stunting_rate", "anemia_rate",
            "nutrition_target", "major_commodity", "protein", "vita",
            "fe", "size", "crop_list", "id"
        )
        widgets = {
            'protein': forms.HiddenInput(),
            'vita': forms.HiddenInput(),
            'fe': forms.HiddenInput(),
            'size': forms.HiddenInput(),
            'crop_list': forms.HiddenInput(),
            'id': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.myid = kwargs.pop('myid')
        super(FamilyForm, self).__init__(*args, **kwargs)

    def clean_crop_list(self):
        d='0'
        if self.myid != '0':
            d = ''
            for crp in Crop.objects.filter(familyid = self.myid):
                d += "-" + str(crp.food_item_id)
                if d[0] == '-':
                    d = d[1:]
        crop_list = d
        return crop_list


class Person_Create_Form(forms.ModelForm):
    class Meta:
        model = Person
        fields = ("familyid", "name" ,"age", "sex", "women_s",
            "protein", "vita", "fe", "target_pop")
        widgets = {
            'name': forms.HiddenInput(),
            'familyid': forms.HiddenInput(),
            'protein': forms.HiddenInput(),
            'vita': forms.HiddenInput(),
            'fe': forms.HiddenInput(),
            }
        labels = {
            "age":"age",
            "sex":"sex",
            "women_s": "additional description of women in reproduction stage",
            "target_pop":"number of community members with the above attributes",
        }


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
        fields = ("familyid", "Food_name", "nutrient_target",
            "food_wt", "food_wt_p", "food_wt_va", "food_wt_fe",
            "feas_DRI_p", "feas_DRI_a", "feas_DRI_f", "feas_soc_acceptable",
            "feas_soc_acceptable_wo", "feas_soc_acceptable_c5",
            "feas_prod_skill", "feas_workload", "feas_tech_service",
            "feas_invest_fixed",
            "feas_invest_variable",
            "feas_affordability", "feas_storability",
            "diet_type", "food_item_id", "food_grp", "protein", "vita", "fe", "crop_score",
            "feas_availability_non", "feas_availability_prod"
            )
        widgets = {
            'familyid': forms.HiddenInput(),
            'food_grp': forms.HiddenInput(),
            'nutrient_target': forms.RadioSelect(attrs={'id': 'value'}),
            'diet_type': forms.RadioSelect(),
            'food_item_id': forms.HiddenInput(),
            'protein': forms.HiddenInput(),
            'vita': forms.HiddenInput(),
            'fe': forms.HiddenInput(),
            'food_wt': forms.HiddenInput(),
            'food_wt_p': forms.HiddenInput(),
            'food_wt_va': forms.HiddenInput(),
            'food_wt_fe': forms.HiddenInput(),
            'crop_score': forms.HiddenInput(),
            'feas_availability_non': forms.HiddenInput(),
            'feas_availability_prod': forms.HiddenInput(),
        }
        labels = {
            "food_wt_p": "required amount of production(t) to meet daily protein requirement",
            "food_wt_va": "required amount of production(t) to meet daily VitA requirement",
            "food_wt_fe": "required amount of production(t) to meet daily Iron requirement",
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
            "diet_type": "is this commodity new for target area?",
        }

    def __init__(self, *args, **kwargs):
        self.myid = kwargs.pop('myid')
        self.food_item_id = kwargs.pop('food_item_id')
        super(CropForm, self).__init__(*args, **kwargs)
#        myquery = FCT.objects.all()
        self.fields['Food_name'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super(CropForm, self).clean()

        myfood = FCT.objects.get(food_item_id = str(self.food_item_id))
        if myfood.Protein == '':
            myfood.Protein = 0
        if myfood.VITA_RAE == '':
            myfood.VITA_RAE = 0
        if myfood.FE == '':
            myfood.FE = 0

        mytarget = Family.objects.get(pk = self.myid)
        self.cleaned_data['food_grp'] = myfood.Food_grp
        self.cleaned_data['protein'] = myfood.Protein
        self.cleaned_data['vita'] = myfood.VITA_RAE
        self.cleaned_data['fe'] = myfood.FE
        self.cleaned_data['familyid'] = self.myid

        if myfood.Protein >0:
            self.cleaned_data['food_wt_p'] = round(mytarget.protein *100 *365 / myfood.Protein / 1000000, 1)
        else:
            self.cleaned_data['food_wt_p'] = 0

        if myfood.VITA_RAE > 0:
            self.cleaned_data['food_wt_va'] = round(mytarget.vita *100 *365 / myfood.VITA_RAE / 1000000, 1)
        else:
            self.cleaned_data['food_wt_va'] = 0

        if myfood.FE > 0:
            self.cleaned_data['food_wt_fe'] = round(mytarget.fe *100 *365 / myfood.FE / 1000000, 1)
        else:
            self.cleaned_data['food_wt_fe'] = 0

        if cleaned_data['nutrient_target'] == 1:
            self.cleaned_data['food_wt'] = self.cleaned_data['food_wt_p']
        elif cleaned_data['nutrient_target'] == 2:
            self.cleaned_data['food_wt'] = self.cleaned_data['food_wt_va']
        else:
            self.cleaned_data['food_wt'] = self.cleaned_data['food_wt_fe']

        self.cleaned_data['crop_score'] = self.cleaned_data['feas_soc_acceptable'] \
            + self.cleaned_data['feas_soc_acceptable_wo'] +self.cleaned_data['feas_soc_acceptable_c5'] \
            + self.cleaned_data['feas_DRI_p'] +self.cleaned_data['feas_DRI_a'] \
            + self.cleaned_data['feas_DRI_f'] +  self.cleaned_data['feas_prod_skill'] \
            + self.cleaned_data['feas_workload'] \
            + self.cleaned_data['feas_invest_fixed']\
            + self.cleaned_data['feas_tech_service']\
            + self.cleaned_data['feas_invest_variable']\
            + self.cleaned_data['feas_availability_non']\
            + self.cleaned_data['feas_availability_prod']\
            + self.cleaned_data['feas_storability']

        return cleaned_data
