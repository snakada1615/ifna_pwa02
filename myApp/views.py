from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers

from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import FCT, Person, DRI, DRI_women, Family, Crop, myProgress, Countries
from .forms import Order_Key_Form, FamilyForm, Person_Create_Form, CropForm, Person_new_Create_Form
from django.db.models import Q, Sum

# for user registration
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

#for 正規表現チェック
import re
import logging
#from tkinter import messagebox

class Diet_Plan1(TemplateView):
    template_name = "myApp/Diet_Plan1.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['families'] = Person.objects.filter(
            familyid=self.kwargs['familyid'])
        context['name'] = Family.objects.get(id=self.kwargs['familyid'])
        context['myid'] = Family.objects.get(id=self.kwargs['familyid']).id
        context['country'] = Family.objects.get(
            id=self.kwargs['familyid']).country
        context['region'] = Family.objects.get(
            id=self.kwargs['familyid']).region
        context['nutrition_target'] = Family.objects.get(
            id=self.kwargs['familyid']).nutrition_target
        context['dri_p'] = Family.objects.get(
            id=self.kwargs['familyid']).protein
        context['dri_v'] = Family.objects.get(id=self.kwargs['familyid']).vita
        context['dri_f'] = Family.objects.get(id=self.kwargs['familyid']).fe

        tmp_sex = ''
        try:
            data = Person.objects.filter(familyid=self.kwargs['familyid'])[0]
            tmp_sex = Person.SEX_CHOICES[data.sex - 1][1]
        except:
            tmp_sex = 'no data'
        tmp_age = ''
        try:
            data = Person.objects.filter(familyid=self.kwargs['familyid'])[0]
            tmp_age = Person.AGE_CHOICES[data.age - 1][1]
        except:
            tmp_age = 'no data'
        context['sex'] = tmp_sex
        context['age'] = tmp_age

        tmp = Family.objects.get(id=self.kwargs['familyid']).crop_list
        crops = []
        if ('-' in tmp):
            for crop in tmp.split('-'):
                crops.append(FCT.objects.get(food_item_id=crop).Food_name)
        context['crop_list'] = crops
        return context

class Person_new_UpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = Person_new_Create_Form
    template_name = 'myApp/person_new_form.html'

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Person_new_UpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['familyid']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        myid = self.kwargs['familyid']
        mydata = Family.objects.get(id=myid)
        context['name'] = mydata
        context['myid'] = myid
        context["families"] = Person.objects.filter(
            familyid=self.kwargs['familyid']).order_by('age')
        return context

    def form_valid(self, form):
        self.object = form.save()
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        myid = self.kwargs['familyid']
        protein1 = 0
        vita1 = 0
        fe1 = 0

        Persons = Person.objects.filter(familyid=myid)
        if Persons.count() > 0:
            rec = Family.objects.filter(id=myid).first()
            rec.size = Persons.count()

            for myPerson in Persons:
                protein1 += myPerson.protein * myPerson.target_pop
                vita1 += myPerson.vita * myPerson.target_pop
                fe1 += myPerson.fe * myPerson.target_pop
                rec = Family.objects.filter(id=myid).first()

            rec.protein = protein1
            rec.vita = vita1
            rec.fe = fe1
            rec.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse_lazy('person_list', kwargs={'familyid': self.kwargs['familyid']})


class Person_new_CreateView(LoginRequiredMixin, CreateView):
    model = Person
    form_class = Person_new_Create_Form
    template_name = 'myApp/person_new_form.html'

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Person_new_CreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['familyid']
        return kwargs

    def get_context_data(self, **kwargs):
        myid = self.kwargs['familyid']
        mydata = Family.objects.get(id=myid)
        context = super().get_context_data(**kwargs)
        context['myid'] = myid
        context['name'] = mydata
        context["families"] = Family.objects.filter(
            id=self.kwargs['familyid']).order_by('age')
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('person_list', kwargs={'familyid': self.kwargs['familyid']})

    def form_valid(self, form):
        self.object = form.save()
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        form.instance.created_by = self.request.user
        myid = self.kwargs['familyid']

        protein1 = 0
        vita1 = 0
        fe1 = 0

        Persons = Person.objects.filter(familyid=myid)
        if Persons.count() > 0:
            rec = Family.objects.filter(id=myid).first()
            rec.size = Persons.count()

            for myPerson in Persons:
                protein1 += myPerson.protein * myPerson.target_pop
                vita1 += myPerson.vita * myPerson.target_pop
                fe1 += myPerson.fe * myPerson.target_pop
                rec = Family.objects.filter(id=myid).first()

            rec.protein = protein1
            rec.vita = vita1
            rec.fe = fe1
            rec.save()

        myProg_rec = myProgress.objects.filter(
            user_id=self.request.user.id).first()
        myProg_rec.person_id = form.instance.pk

        myProg_rec.save()

        return super(Person_new_CreateView, self).form_valid(form)
#        return HttpResponseRedirect(self.get_success_url())


def myConsole(output):
    path_w = 'myApp/output_log.txt'
    with open(path_w, mode='w') as f:
        f.write(output)

class TestView01(LoginRequiredMixin, TemplateView):
    template_name = "myApp/index03.html"

# Create your views here.
class convCrop_Grow(TemplateView):
    template_name = "myApp/conv_crop_grow.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['name'] = Family.objects.get(id=self.kwargs['familyid'])

        tmp = Family.objects.get(id=self.kwargs['familyid']).conv_crop_grow
        crops = []
        if ('-' in tmp):
            for crop in tmp.split('-'):
                crops.append(FCT.objects.get(food_item_id=crop).Food_name)
        context['crop_list'] = crops
        return context


class convCrop_Sold(TemplateView):
    template_name = "myApp/conv_crop_sold.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Family.objects.get(id=self.kwargs['familyid'])

        tmp = Family.objects.get(id=self.kwargs['familyid']).conv_crop_sold
        crops = []
        if ('-' in tmp):
            for crop in tmp.split('-'):
                crops.append(FCT.objects.get(food_item_id=crop).Food_name)
        context['crop_list'] = crops
        return context

def registConvCrops_grow(request, familyid, items):
    #   update crop_list to match with DCT_datatable selection
    Family.objects.filter(id=familyid).update(conv_crop_grow=items)
    myProgress.objects.filter(user_id=request.user.id).update(
        conv_crop_grow_list=items)


#    move to crop list page
    myURL = reverse_lazy('index02')
    return HttpResponseRedirect(myURL)


def registConvCrops_sold(request, familyid, items):
    #    tmp = Family.objects.get(id=familyid).crop_list

    #   update crop_list to match with DCT_datatable selection
    Family.objects.filter(id=familyid).update(conv_crop_sold=items)
    myProgress.objects.filter(user_id=request.user.id).update(
        conv_crop_sold_list=items)

#    move to crop list page
    myURL = reverse_lazy('index02')
    return HttpResponseRedirect(myURL)


class FCTdatable_View(TemplateView):
    template_name = "myApp/FCT_datable.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['families'] = Person.objects.filter(familyid = self.kwargs['familyid'])
        context['name'] = Family.objects.get(id = self.kwargs['familyid'])
        context['myid'] = Family.objects.get(id = self.kwargs['familyid']).id
        context['country'] = Family.objects.get(id = self.kwargs['familyid']).country
        context['region'] = Family.objects.get(id = self.kwargs['familyid']).region
        context['nutrition_target'] = Family.objects.get(id = self.kwargs['familyid']).nutrition_target
        context['dri_p'] = Family.objects.get(id = self.kwargs['familyid']).protein
        context['dri_v'] = Family.objects.get(id = self.kwargs['familyid']).vita
        context['dri_f'] = Family.objects.get(id = self.kwargs['familyid']).fe

        tmp_sex=''
        try:
            data = Person.objects.filter(familyid = self.kwargs['familyid'])[0]
            tmp_sex = Person.SEX_CHOICES[data.sex-1][1]
        except:
            tmp_sex = 'no data'
        tmp_age=''
        try:
            data = Person.objects.filter(familyid = self.kwargs['familyid'])[0]
            tmp_age = Person.AGE_CHOICES[data.age-1][1]
        except:
            tmp_age = 'no data'
        context['sex'] = tmp_sex
        context['age'] = tmp_age

        tmp = Family.objects.get(id = self.kwargs['familyid']).crop_list
        crops = []
        if ('-' in tmp):
            for crop in tmp.split('-'):
                crops.append(FCT.objects.get(food_item_id = crop).Food_name)
        context['crop_list'] = crops
        return context


class Under_Construction_View(TemplateView):
    template_name = "myApp/under_construction.html"

class Crop_Calendar_View(TemplateView):
    template_name = "myApp/crop_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crop_name'] = Crop.objects.get(id = self.kwargs['pk']).Food_name
        return context

class Crop_Feas_View(TemplateView):
    template_name = "myApp/feasibility_result.html"

class Trial_View(TemplateView):
    template_name = "myApp/trial.html"

class TestOfflineView(TemplateView):
    template_name = "myApp/offline/test.html"

class off_FCT_view(TemplateView):
    template_name = "myApp/offline/off_FCT_view.html"

class off_Family_ListView(TemplateView):
    template_name = "myApp/offline/family_list.html"

class off_Family_CreateView(TemplateView):
    template_name = "myApp/offline/family_form.html"

class TestView(TemplateView):
    template_name = "myApp/index.html"

class WhoamI_View(TemplateView):
    template_name = "myApp/acknowledge.html"

class Usage_View(TemplateView):
    template_name = "myApp/usage.html"

class OfflineView(TemplateView):
    template_name = "myApp/offline.html"

class FCT_show(LoginRequiredMixin, ListView):
    template_name = 'myApp/FCT_view.html'  # この行でテンプレート指定
    context_object_name = 'foods1'
    model = FCT
    paginate_by = 20
    Choice_Sortkey =	{
      0: 'Food_name',
      1: '-Protein',
      2: '-FE',
      3: '-VITA_RAE',
    }
    Categ_FoodGrp = {
		1: 'Cereals and their products',
		2: 'Roots, tubers and their products',
		3: 'Legumes and their products',
		4: 'Vegetables and their products',
		5: 'Fruits and their products',
		6: 'Nuts, Seeds and their products',
		7: 'Meat, poultry and their products',
		8: 'Eggs and their products',
		9: 'Fish and their products',
		10: 'Milk and their products',
		11: 'Bevarages and their products',
		12: 'Miscellaneous',
    }

    def get_queryset(self):
        queryset = super().get_queryset().filter(food_grp_id = self.kwargs['categ']).order_by(self.Choice_Sortkey[self.kwargs['order']])
        return queryset

    def get_context_data(self, **kwargs):
        form = Order_Key_Form()
        context = super().get_context_data(**kwargs)
        context['order1'] = form
        context['categ_id'] = self.kwargs['categ']
        context['categ'] = self.Categ_FoodGrp[self.kwargs['categ']]
        return context

class Family_ListView(LoginRequiredMixin, ListView):
    model = Family
    context_object_name = "mylist"
    template_name = 'myApp/family_list.html'

class FamilyFiltered_ListView(LoginRequiredMixin, ListView):
    model = Family
    context_object_name = "mylist"
    template_name = 'myApp/family_list_filtered.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(created_by = self.request.user)
        return queryset

class Family_DeleteView(LoginRequiredMixin, DeleteView):
    model = Family
    template_name = 'myApp/family_confirm_delete.html'
    success_url = reverse_lazy('Family_filter')

class Family_CreateView(LoginRequiredMixin, CreateView):
    model = Family
    form_class = FamilyForm
    template_name = 'myApp/family_form.html'
    success_url = reverse_lazy('Family_filter')

    def form_valid(self, form):
        self.object = form.save()
# --------------------update myProgress-------------------------
        keys = {}
        keys['family_id'] = form.instance.pk
        keys['conv_crop_grow_list'] = "0"
        keys['conv_crop_sold_list'] = "0"
        keys['person_id'] = 0
        tmp = myProgress.objects.filter(user_id=self.request.user.id)
        if tmp.count() == 0:
            keys['user_id'] = self.request.user.id
            p = myProgress.objects.create(**keys)
        else:
            p = tmp.update(**keys)

#        keys_all.update(**keys)
# ---------------------
        form.instance.created_by = self.request.user
        form.instance.country_test = Countries.objects.filter(GID_2 = form.instance.province).first()
        return super(Family_CreateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Family_CreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = '0'
        return kwargs

    def get_context_data(self, **kwargs):
        data = Countries.objects.all()
        context = super().get_context_data(**kwargs)
        context['countries'] = serializers.serialize('json', data)
        context['coutry_selected'] = ''
        context['region_selected'] = ''
        context['province_selected'] = ''
        return context


class Family_UpdateView(LoginRequiredMixin, UpdateView):
    model = Family
    form_class = FamilyForm
    template_name = 'myApp/family_form.html'
    success_url = reverse_lazy('Family_index')

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Family_UpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['pk']
        return kwargs


class Person_ListView(LoginRequiredMixin, ListView):
    template_name = 'myApp/person_list.html'  # この行でテンプレート指定
    context_object_name = 'persons'
    model = Person

    def get_queryset(self):
        queryset = super().get_queryset().filter(familyid = self.kwargs['familyid']).order_by('age')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myfamily'] = Family.objects.get(id = self.kwargs['familyid'])

        return context

# 登録画面
class Person_CreateView(LoginRequiredMixin, CreateView):
    model = Person
    form_class = Person_Create_Form
    template_name = 'myApp/person_form.html'

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Person_CreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['familyid']
        return kwargs

    def get_context_data(self, **kwargs):
        myid = self.kwargs['familyid']
        mydata = Family.objects.get(id = myid)
        context = super().get_context_data(**kwargs)
        context['myid'] = myid
        context['name'] = mydata
        context["families"] = Family.objects.filter(id = self.kwargs['familyid']).order_by('age')
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('person_list', kwargs = {'familyid': self.kwargs['familyid']})

    def form_valid(self, form):
        self.object = form.save()
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        form.instance.created_by = self.request.user
        myid = self.kwargs['familyid']

        protein1 = 0
        vita1 = 0
        fe1 = 0

        Persons = Person.objects.filter(familyid = myid)
        if Persons.count() > 0:
            rec = Family.objects.filter(id = myid).first()
            rec.size = Persons.count()

            for myPerson in Persons:
                protein1 += myPerson.protein * myPerson.target_pop
                vita1 += myPerson.vita * myPerson.target_pop
                fe1 += myPerson.fe * myPerson.target_pop
                rec = Family.objects.filter(id = myid).first()

            rec.protein = protein1
            rec.vita = vita1
            rec.fe = fe1
            rec.save()

        return super(Person_CreateView, self).form_valid(form)
#        return HttpResponseRedirect(self.get_success_url())

# 更新画面
class Person_UpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = Person_Create_Form
    template_name = 'myApp/person_form.html'

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Person_UpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['familyid']
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        myid = self.kwargs['familyid']
        protein1 = 0
        vita1 = 0
        fe1 = 0

        Persons = Person.objects.filter(familyid = myid)
        if Persons.count() > 0:
            rec = Family.objects.filter(id = myid).first()
            rec.size = Persons.count()

            for myPerson in Persons:
                protein1 += myPerson.protein * myPerson.target_pop
                vita1 += myPerson.vita * myPerson.target_pop
                fe1 += myPerson.fe * myPerson.target_pop
                rec = Family.objects.filter(id = myid).first()

            rec.protein = protein1
            rec.vita = vita1
            rec.fe = fe1
            rec.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        myid = self.kwargs['familyid']
        mydata = Family.objects.get(id = myid)
        context = super().get_context_data(**kwargs)
        context['name'] = mydata
        context['myid'] = myid
        context["families"] = Person.objects.filter(familyid = self.kwargs['familyid']).order_by('age')
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('person_list', kwargs = {'familyid': self.kwargs['familyid']})


# 削除画面
class Person_DeleteView(LoginRequiredMixin, DeleteView):
    model = Person
    template_name = 'myApp/person_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['familyid'] = self.kwargs['familyid']
        return context

    def get_success_url(self, **kwargs):
        if  kwargs != None:
            return reverse_lazy('person_list', kwargs = {'familyid': self.kwargs['familyid']})
        else:
            return reverse_lazy('person_list', args = (self.object.id,))

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        success_url = self.get_success_url()

        myid = self.kwargs['familyid']
        protein1 = 0
        vita1 = 0
        fe1 = 0

        Persons = Person.objects.filter(familyid = myid)
        if Persons.count() > 0:
            rec = Family.objects.filter(id = myid).first()
            rec.size = Persons.count()

            for myPerson in Persons:
                protein1 += myPerson.protein * myPerson.target_pop
                vita1 += myPerson.vita * myPerson.target_pop
                fe1 += myPerson.fe * myPerson.target_pop
                rec = Family.objects.filter(id = myid).first()

            rec.protein = protein1
            rec.vita = vita1
            rec.fe = fe1
            rec.save()

        return HttpResponseRedirect(success_url)

def SetFoodTarget(id):
    # calculate required food weight per commodity, person
    person_food_target = {}
    prot_weights = {}
    vita_weights = {}
    fe_weights = {}
    for person in Person.objects.filter(familyid = id):
        food_target = {}
        for crop in Crop.objects.filter(familyid = id):
            f_weights = {}
            if crop.protein>0:
                f_weights['protein'] = round(person.protein *100 / crop.protein, 1)
            else:
                f_weights['protein'] = 0
            if crop.vita>0:
                f_weights['vit-a'] = round(person.vita *100 / crop.vita, 1)
            else:
                f_weights['vit-a'] = 0
            if crop.fe>0:
                f_weights['iron'] = round(person.fe *100 / crop.fe, 1)
            else:
                f_weights['iron'] = 0
            food_target[crop.id] = f_weights
        person_food_target[person.id] = food_target
    return person_food_target


class Crop_ListView(LoginRequiredMixin, ListView):
    model = Crop
    context_object_name = "crops"
    template_name = 'myApp/crop_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(familyid = self.kwargs['familyid'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Persons'] = Person.objects.filter(familyid = self.kwargs['familyid'])
        context['myfamily'] = Family.objects.get(id = self.kwargs['familyid'])

        mydats = Crop.objects.filter(familyid = self.kwargs['familyid'])
        myitems = {}
        for mydat in mydats:
            myitem = ''
            for i in range(1,3):
                for j in range(1,13):
                    if (getattr(mydat, 'm'+str(j)+'_p') == 1):
                        myitem += str(j) + ':1' + '-'
                    if (getattr(mydat, 'm'+str(j)+'_m') == 1):
                        myitem += str(j) + ':2' + '-'
            if (len(myitem)>0):
                myitem = myitem[:-1]
            else:
                myitem = '0'
            myitems[mydat.id] = myitem

        crop_names = []
        if ('-' in Family.objects.get(id = self.kwargs['familyid']).crop_list):
            for crop in Family.objects.get(id = self.kwargs['familyid']).crop_list.split('-'):
                crop_names.append(FCT.objects.get(food_item_id = crop).Food_name)
        context['crop_list'] = crop_names
        context['myCal'] = myitems
        context['person_food_target'] = SetFoodTarget(self.kwargs['familyid'])

        return context

class Crop_DeleteView(LoginRequiredMixin, DeleteView):
    model = Crop
    template_name = 'myApp/crop_confirm_delete.html'
    success_url = reverse_lazy('crop_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['familyid'] = self.kwargs['familyid']
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('crop_list', kwargs = {'familyid': self.kwargs['familyid']})


class Crop_CreateView(LoginRequiredMixin, CreateView):
    model = Crop
    form_class = CropForm
    template_name = 'myApp/crop_form.html'

    def get_context_data(self, **kwargs):
        myid = self.kwargs['familyid']
        context = super().get_context_data(**kwargs)
        context['myid'] = myid
        context['dri_p'] = Family.objects.get(id = self.kwargs['familyid']).protein
        context['dri_v'] = Family.objects.get(id = self.kwargs['familyid']).vita
        context['dri_f'] = Family.objects.get(id = self.kwargs['familyid']).fe
        return context

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Crop_CreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['familyid']
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(Crop_CreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('crop_list', kwargs = {'familyid': self.kwargs['familyid']})


class Crop_UpdateView(LoginRequiredMixin, UpdateView):
    model = Crop
    form_class = CropForm
    template_name = 'myApp/crop_form.html'

    def get_context_data(self, **kwargs):
        myid = self.kwargs['familyid']

        mydat = Crop.objects.get(pk = self.kwargs['pk'])
        myitem = ''
        for i in range(1,3):
            for j in range(1,13):
                if (getattr(mydat, 'm'+str(j)+'_p') == 1):
                    myitem += str(j) + ':1' + '-'
                if (getattr(mydat, 'm'+str(j)+'_m') == 1):
                    myitem += str(j) + ':2' + '-'
        if (len(myitem)>0):
            myitem = myitem[:-1]
        else:
            myitem = '0'

        context = super().get_context_data(**kwargs)
        context['persons'] = Person.objects.filter(familyid = self.kwargs['familyid'])
        context['person_food_target'] = SetFoodTarget(self.kwargs['familyid'])
        context['f_name'] = Crop.objects.get(id = self.kwargs['pk']).Food_name
        context['n_target'] = Crop.objects.get(id = self.kwargs['pk']).get_nutrient_target_display
        context['myid'] = myid
        context['myCal'] = myitem
        context['pk'] = self.kwargs['pk']
        context['dri_p'] = Family.objects.get(id = self.kwargs['familyid']).protein
        context['dri_v'] = Family.objects.get(id = self.kwargs['familyid']).vita
        context['dri_f'] = Family.objects.get(id = self.kwargs['familyid']).fe
        return context

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""

        # grab the current set of form #kwargs
        kwargs = super(Crop_UpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['familyid']
        kwargs['food_item_id'] = Crop.objects.get(pk = self.kwargs['pk']).food_item_id
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse_lazy('crop_list', kwargs = {'familyid': self.kwargs['familyid']})

def getNFA(request, store_id, familyid):
    results = FCT.objects.all()
    if store_id == 1:
        results = FCT.objects.all()
    if store_id == 2:
        results = DRI.objects.all()
    if store_id == 3:
        results = DRI_women.objects.all()
    if store_id == 4:
        results = Person.objects.all()
    if store_id == 5:
        results = Crop.objects.filter(familyid = familyid)
    if store_id == 6:
        results = Family.objects.all()

    jsondata = serializers.serialize('json',results)
    return HttpResponse(jsondata)


def registCalendar(request, familyid, pk, itemstr):
    pattern = '^(\d+:\d+)(-\d+:\d+)*$'
    myURL = reverse_lazy('crop_list', kwargs = {'familyid': familyid})

    if (re.match(pattern, itemstr) == False) and (itemstr != '0'):
        return HttpResponseRedirect(myURL)

    # update calendar
    newcalendar = {}
    pm_choice = ['_p','_m']
    items = itemstr.split('-')
    for i in range(1,3):
        for j in range(1,13):
            myitem = str(j) + ':' + str(i)
            if (myitem in items):
                newcalendar['m' + str(j) + pm_choice[i-1] ] = 1
            else:
                newcalendar['m' + str(j) + pm_choice[i-1] ] = 0

    avail_p = 0
    avail_non = 0
    for i in range(1, 13):
        avail_p += newcalendar['m' + str(i) + '_p' ]
        if ((newcalendar['m' + str(i) + '_p' ] == 0) and (newcalendar['m' + str(i) + '_m' ] == 0)):
            avail_non+=1

    if avail_p < 4:
        avail_p_all = 0
    elif avail_p < 7:
        avail_p_all = 1
    elif avail_p < 10:
        avail_p_all = 2
    else:
        avail_p_all = 3
    newcalendar['feas_availability_prod'] = avail_p_all

    if avail_non < 4:
        avail_non_all = 3
    elif avail_non < 7:
        avail_non_all = 2
    elif avail_non < 10:
        avail_non_all = 1
    else:
        avail_non_all = 0
    newcalendar['feas_availability_non'] = avail_non_all

#    logging.debug(newcalendar)
    p = Crop.objects.filter(id = pk).update(**newcalendar)


#    move to crop assessment page
    return HttpResponseRedirect(myURL)


def registCrops(request, familyid, items, items_w, avail_type):

    if items != '0':
        mytarget = Family.objects.get(pk=familyid)

        tmp = Family.objects.get(id=familyid).crop_list
        crops = []
        a = 0
        if ('-' in tmp):
            crops = tmp.split('-')
        else:
            crops.append(tmp)

        selectedItem = []
        if ('-' in items):
            selectedItem = items.split('-')
        else:
            selectedItem.append(items)

        Weight = []
        if ('-' in items_w):
            Weight = items_w.split('-')
        else:
            Weight.append(items_w)

#        myConsole(selectedItem)

        # set new/update crop item
        for i in range(len(selectedItem)):
#        for i in range(3):
            myfood = FCT.objects.get(food_item_id=selectedItem[i])
            newcrop = {}
            if myfood.Protein == '':
                myfood.Protein = 0
            if myfood.VITA_RAE == '':
                myfood.VITA_RAE = 0
            if myfood.FE == '':
                myfood.FE = 0

            newcrop['food_item_id'] = myfood.food_item_id
            newcrop['Food_name'] = myfood.Food_name
            newcrop['food_grp'] = myfood.Food_grp
            newcrop['protein'] = myfood.Protein
            newcrop['vita'] = myfood.VITA_RAE
            newcrop['fe'] = myfood.FE
            newcrop['familyid'] = familyid
            newcrop['avail_type'] = avail_type
            newcrop['food_wt'] = Weight[i]

            newcrop['created_by'] = request.user

            if myfood.Protein > 0:
                newcrop['food_wt_p'] = round(
                    mytarget.protein * 100 / myfood.Protein, 1)
            else:
                newcrop['food_wt_p'] = 0

            if myfood.VITA_RAE > 0:
                newcrop['food_wt_va'] = round(
                    mytarget.vita * 100 / myfood.VITA_RAE, 1)
            else:
                newcrop['food_wt_va'] = 0

            if myfood.FE > 0:
                newcrop['food_wt_fe'] = round(mytarget.fe * 100 / myfood.FE, 1)
            else:
                newcrop['food_wt_fe'] = 0

            tmp = Crop.objects.filter(familyid=familyid).filter(food_item_id=selectedItem[i])
            if tmp.count() == 0:
                p = Crop.objects.create(**newcrop)
            else:
                p = tmp.update(**newcrop)

    for crop in crops:
        if crop in selectedItem:
            a += 1  # do nothing"
        else:
            #            delete crop here"
            p = Crop.objects.filter(food_item_id=crop).delete()

#   update crop_list to match with DCT_datatable selection
    Family.objects.filter(id=familyid).update(crop_list=items)
    myProgress.objects.filter(
        user_id=request.user.id).update(crop_list=items)

#    move to crop list page
    myURL = reverse_lazy('index02')
    return HttpResponseRedirect(myURL)


def funcTest(request):
#    move to crop list page
    test = request.user.username + ':' + str(request.user.date_joined)
    if (request.user.date_joined > datetime.date(2019, 9,30)):
        test += ', yes new'
    else:
        test += ', no old'

    return HttpResponse(test)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("test")

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "myApp/signup.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "myApp/signup.html",
                  context={"form":form})


def SetCal(request):
    import json
    mydats = Crop.objects.all()
    myitem = {}
    result = {}
    i = 0
    for mydat in mydats:
        myitem = {}
        i = i+1
        myitem['id'] = getattr(mydat, 'id')
        myitem['prod_period'] = getattr(mydat, 'feas_availability_non')
        myitem['non_availability'] = getattr(mydat, 'feas_availability_prod')

        if (myitem['prod_period'] == 0):
            jmax = 1
        elif (myitem['prod_period'] == 1):
            jmax = 5
        elif (myitem['prod_period'] == 2):
            jmax = 8
        elif (myitem['prod_period'] == 3):
            jmax = 11

        newcalendar = {}
        for j in range(1,13):
            if (j <= jmax):
                newcalendar['m' + str(j) + '_p' ] = 1
            else:
                newcalendar['m' + str(j) + '_p' ] = 0

        if (myitem['non_availability'] == 0):
            tmp = 1
        elif (myitem['non_availability'] == 1):
            tmp = 5
        elif (myitem['non_availability'] == 2):
            tmp = 8
        elif (myitem['non_availability'] == 3):
            tmp = 11
        kmax = tmp + jmax
        if kmax > 12:
            kmax = 12

        for i in range(1, 13):
            if (i <= jmax):
                newcalendar['m' + str(i) + '_m' ] = 0
            elif (i <= kmax):
                newcalendar['m' + str(i) + '_m' ] = 0
            else:
                newcalendar['m' + str(i) + '_m' ] = 1

#        logging.debug(newcalendar)
        p = Crop.objects.filter(id = myitem['id']).update(**newcalendar)

#    jsondata = serializers.serialize('json',result)
        result[str(i)]=newcalendar

    return HttpResponse(json.dumps(result))
