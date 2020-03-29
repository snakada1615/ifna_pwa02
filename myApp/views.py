import re
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
from django.http.response import JsonResponse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import LocationForm, Person_Form

from .models import myStatus,Location, Countries, Crop_National, Crop_SubNational
from .models import FCT, DRI, Crop_Feasibility, Crop_Individual, Person


# for user registration
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

# python component
import json

class Trial_View(TemplateView):
    template_name = "myApp/_test.html"

class IndexView(TemplateView):
    template_name = "myApp/index01.html"

class Under_Construction_View(TemplateView):
    template_name = "myApp/under_construction.html"

class aboutNFA(TemplateView):
    template_name = "myApp/whatisNFA.html"

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class UserEdit(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "myApp/signup_edit.html"
    success_url = reverse_lazy('index01')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()  # formの情報を保存
            login(self.request, user)  # 認証
            self.object = user
            return HttpResponseRedirect(self.get_success_url())  # リダイレクト

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request=request,
                          template_name="myApp/signup_edit.html",
                          context={"form": form})


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1', 'password2')


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "myApp/signup.html"
    success_url = reverse_lazy('index01')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()  # formの情報を保存
            login(self.request, user)  # 認証
            self.object = user
            return HttpResponseRedirect(self.get_success_url())  # リダイレクト

        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request=request,
                          template_name="myApp/signup.html",
                          context={"form": form})

class IndexView02(LoginRequiredMixin, TemplateView):
    template_name = "myApp/index02.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ######## create record if not exists #########
        tmp = myStatus.objects.filter(curr_User=self.request.user.id)
        if tmp.count() == 0:
            keys = {}
            keys['curr_User'] = self.request.user.id
            p = myStatus.objects.create(**keys)
        ###############################################

        keys_all = myStatus.objects.get(curr_User=self.request.user.id)
        data = {
            'curr_User': keys_all.curr_User,
            'myLocation': keys_all.myLocation,
            'myCrop': keys_all.myCrop,
            'myTarget': keys_all.myTarget,
            'myDiet': keys_all.myDiet,
        }
        json_str = json.dumps(data)
        context['myParam'] = json_str

        return context


class Location_ListView(LoginRequiredMixin, ListView):
    model =Location
    context_object_name = "mylist"
    template_name = 'myApp/Location_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(created_by=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myLocation'] = myStatus.objects.all().first().myLocation
        context['myuser'] = self.request.user
        return context


class Location_DeleteView(LoginRequiredMixin, DeleteView):
    model =Location
    template_name = 'myApp/Location_confirm_delete.html'
    success_url = reverse_lazy('Location_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context


class Location_CreateView(LoginRequiredMixin, CreateView):
    model =Location
    form_class = LocationForm
    template_name = 'myApp/Location_form.html'
    success_url = reverse_lazy('Location_list')

    def form_invalid(self, form):
        res = super().form_invalid(form)
        res.status_code = 400
        return res

    def form_valid(self, form):
        self.object = form.save()
# --------------------update myStatus-------------------------
        keys = {}
        keys['myLocation'] = form.instance.pk
        tmp = myStatus.objects.filter(curr_User = self.request.user.id)
        if tmp.count() == 0:
            keys['curr_User'] = self.request.user.id
            p = myStatus.objects.create(**keys)
        elif tmp.count() == 1:
            p = tmp.update(**keys)
        else:
            raise Exception("例外が発生しました")

#        keys_all.update(**keys)
# ---------------------
# --------------------update myCrop-------------------------
        tmp_aez = Countries.objects.filter(
            GID_2=form.instance.province).first().AEZ_id
        tmp = Crop_National.objects.filter(AEZ_id=tmp_aez)
        if tmp.count() != 0:
            for tmp01 in tmp:
                keys = {}
                keys['myLocation'] =Location.objects.get(id=form.instance.pk)
                keys['myFCT'] = FCT.objects.get(food_item_id=tmp01.myFCT.food_item_id)
                keys['selected_status'] = 0
                keys['created_by'] = self.request.user
                p = Crop_SubNational.objects.create(**keys)
# ---------------------
        form.instance.AEZ_id = tmp_aez
        form.instance.myCountry = Countries.objects.filter(
            GID_2=form.instance.province).first()
        form.instance.created_by = self.request.user
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
    model =Location
    form_class =LocationForm
    template_name = 'myApp/Location_form.html'
    success_url = reverse_lazy('Location_list')

    def get_context_data(self, **kwargs):
        data = Countries.objects.all()
        context = super().get_context_data(**kwargs)
        context['countries'] = serializers.serialize('json', data)
        myLocation =Location.objects.get(id=self.kwargs['pk'])
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
        self.object = form.save()
# --------------------update myStatus-------------------------
        keys = {}
        keys['myLocation'] = form.instance.pk
        tmp = myStatus.objects.filter(curr_User = self.request.user.id)
        if tmp.count() == 0:
            keys['curr_User'] = self.request.user.id
            p = myStatus.objects.create(**keys)
        elif tmp.count() == 1:
            p = tmp.update(**keys)
        else:
            raise Exception("例外が発生しました")

#        keys_all.update(**keys)
# ---------------------
# --------------------update myCrop-------------------------
        Crop_SubNational.objects.filter(myLocation_id=form.instance.pk).delete()
        tmp_aez = Countries.objects.filter(
            GID_2=form.instance.province).first().AEZ_id
        tmp = Crop_National.objects.filter(AEZ_id = tmp_aez)
        if tmp.count() != 0:
            for tmp01 in tmp:
                keys = {}
                keys['myLocation'] = Location.objects.get(id=form.instance.pk)
                keys['myFCT'] = FCT.objects.get(food_item_id=tmp01.myFCT.food_item_id)
                keys['selected_status'] = 0
                keys['created_by'] = self.request.user
                p = Crop_SubNational.objects.create(**keys)
# ---------------------
        form.instance.AEZ_id = tmp_aez
        form.instance.created_by = self.request.user
        return super(Location_UpdateView, self).form_valid(form)


class CropSelect(TemplateView):
    template_name = "myApp/crop_available.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # send filtered crop by AEZ ######
        tmp01 = Crop_SubNational.objects.filter(myLocation=self.kwargs['myLocation'])
        d = []
        for tmp02 in tmp01:
            dd = {}
            dd["selected_status"] = tmp02.selected_status
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


        return context


def registCropAvail(request):

    #json_str = request.body.decode("utf-8")
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

        tmp = Crop_SubNational.objects.filter(myFCT_id=myrow['myFCT_id'])
        if tmp.count() == 0:
            p = Crop_SubNational.objects.create(**newcrop)
        else:
            p = tmp.update(**newcrop)

    # (part 2) delete non-selected records
    tmp = Crop_SubNational.objects.filter(myLocation_id=tmp_myLocation_id)
    for rec in tmp:
        if int(rec.myFCT.food_item_id) not in tmp_newcrop_list:
            rec.selected_status = 0
            rec.save()

    myStatus.objects.filter(curr_User=request.user.id).update(myCrop='1')

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
            if tmpPerson.class_aggr == 1:
                tmpClass1 = 1
            if tmpPerson.class_aggr == 2:
                tmpClass2 = 1
            if tmpPerson.class_aggr == 3:
                tmpClass3 = 1
        tmpClass_sum = 100*tmpClass1 + 10*tmpClass2 + tmpClass3

        context['myClass_Aggr_Sum'] = tmpClass_sum
        context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
        context['myuser'] = self.request.user

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
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('person_list', kwargs={'myLocation': self.kwargs['myLocation']})

    def form_valid(self, form):
        self.object = form.save()
        form.instance.myDRI = DRI.objects.filter(
            nut_group=form.instance.nut_group).first()
        return super(Person_CreateView, self).form_valid(form)
#        return HttpResponseRedirect(self.get_success_url())


class Person_CreateView(LoginRequiredMixin, CreateView):
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
        context['myLocation'] =  self.kwargs['myLocation']
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('person_list', kwargs={'myLocation': self.kwargs['myLocation']})

    def form_valid(self, form):
        self.object = form.save()
        form.instance.created_by = self.request.user
        form.instance.myDRI = DRI.objects.filter(
            nut_group=form.instance.nut_group).first()
        form.instance.class_aggr = self.kwargs['myClass_Aggr']
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        tmp_myStatus = myStatus.objects.filter(
            curr_User=self.request.user.id).first()
        tmp_myStatus.myTarget = 1
        tmp_myStatus.save()

        return super(Person_CreateView, self).form_valid(form)
#        return HttpResponseRedirect(self.get_success_url())

class Person_DeleteView(LoginRequiredMixin, DeleteView):
    model = Person
    template_name = 'myApp/person_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myLocation'] =  self.kwargs['myLocation']
        return context

    def get_success_url(self, **kwargs):
        if kwargs != None:
            return reverse_lazy('person_list', kwargs={'myLocation': self.kwargs['myLocation']})
        else:
            return reverse_lazy('person_list', args=(self.object.id,))

class Diet_Plan1(TemplateView):
    template_name = "myApp/Diet_Plan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myLocation'] = Location.objects.get(id=self.kwargs['myLocation'])
        tmp_nut_group = Person.objects.filter(
            myLocation=self.kwargs['myLocation'])
        context['nutrient_target'] = tmp_nut_group[0].nut_group

        tmp_nut_group1 = tmp_nut_group.filter(class_aggr=1)
        tmp_e=0
        tmp_p=0
        tmp_v=0
        tmp_f=0
        for tmp in tmp_nut_group1:
            tmp_e += tmp.myDRI.energy
            tmp_p += tmp.myDRI.protein
            tmp_v += tmp.myDRI.vita
            tmp_p += tmp.myDRI.fe
        context['dri_e1'] = tmp_e
        context['dri_p1'] = tmp_p
        context['dri_v1'] = tmp_v
        context['dri_f1'] = tmp_f

        tmp_nut_group2 = tmp_nut_group.filter(class_aggr=2)
        tmp_e=0
        tmp_p=0
        tmp_v=0
        tmp_f=0
        for tmp in tmp_nut_group2:
            tmp_e += tmp.myDRI.energy
            tmp_p += tmp.myDRI.protein
            tmp_v += tmp.myDRI.vita
            tmp_p += tmp.myDRI.fe
        context['dri_e2'] = tmp_e
        context['dri_p2'] = tmp_p
        context['dri_v2'] = tmp_v
        context['dri_f2'] = tmp_f

        tmp_nut_group3 = tmp_nut_group.filter(class_aggr=3)
        tmp_e=0
        tmp_p=0
        tmp_v=0
        tmp_f=0
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
        tmp01 = Crop_SubNational.objects.filter(myLocation_id=self.kwargs['myLocation'])
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
            dd["Weight"] = "0"
            dd["food_item_id"] = tmp02.myFCT.food_item_id
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
            d.append(dd)
        context["mylist_available"] = d

        # send selected crop by community ######
        tmp01 = Crop_Individual.objects.filter(myLocation_id=self.kwargs['myLocation'])
        d = []
        for tmp02 in tmp01:
            dd = {}
            dd["class_aggr"] = tmp02.class_aggr
            dd["Food_grp"] = tmp02.myFCT.Food_grp
            dd["Food_name"] = tmp02.myFCT.Food_name
            dd["Energy"] = tmp02.myFCT.energy
            dd["Protein"] = tmp02.myFCT.Protein
            dd["VITA_RAE"] = tmp02.myFCT.VITA_RAE
            dd["FE"] = tmp02.myFCT.FE
            dd["food_item_id"] = tmp02.myFCT.food_item_id
            dd["portion_size"] = tmp02.portion_size
            dd["total_weight"] = tmp02.total_weight
            dd["m1_prod"] = tmp02.m1_prod
            dd["m2_prod"] = tmp02.m2_prod
            dd["m3_prod"] = tmp02.m3_prod
            dd["m4_prod"] = tmp02.m4_prod
            dd["m5_prod"] = tmp02.m5_prod
            dd["m6_prod"] = tmp02.m6_prod
            dd["m7_prod"] = tmp02.m7_prod
            dd["m8_prod"] = tmp02.m8_prod
            dd["m9_prod"] = tmp02.m9_prod
            dd["m10_prod"] = tmp02.m10_prod
            dd["m11_prod"] = tmp02.m11_prod
            dd["m12_prod"] = tmp02.m12_prod
            dd["m1_buy"] = tmp02.m1_buy
            dd["m2_buy"] = tmp02.m2_buy
            dd["m3_buy"] = tmp02.m3_buy
            dd["m4_buy"] = tmp02.m4_buy
            dd["m5_buy"] = tmp02.m5_buy
            dd["m6_buy"] = tmp02.m6_buy
            dd["m7_buy"] = tmp02.m7_buy
            dd["m8_buy"] = tmp02.m8_buy
            dd["m9_buy"] = tmp02.m9_buy
            dd["m10_buy"] = tmp02.m10_buy
            dd["m11_buy"] = tmp02.m11_buy
            dd["m12_buy"] = tmp02.m12_buy
            d.append(dd)
        context["mylist_selected"] = d

        context['myuser'] = self.request.user

        return context
