import re
from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers
from django.http.response import JsonResponse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import LocationForm

from .models import myStatus,Location

# for user registration
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

# python component
import json


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

    def form_valid(self, form):
        self.object = form.save()
# --------------------update myProgress-------------------------
        keys = {}
        keys['Location_id'] = form.instance.pk
        tmp = myProgress.objects.filter(user_id=self.request.user.id)
        if tmp.count() == 0:
            keys['user_id'] = self.request.user.id
            p = myProgress.objects.create(**keys)
        else:
            p = tmp.update(**keys)

#        keys_all.update(**keys)
# ---------------------
# --------------------update myCrop-------------------------
        tmp_aez = Countries.objects.filter(
            GID_2=form.instance.province).first().AEZ_id
        tmp = Crop_AEZ.objects.filter(AEZ_id=tmp_aez)
        if tmp.count() != 0:
            for tmp01 in tmp:
                keys = {}
                keys['myLocation'] =Location.objects.get(id=form.instance.pk)
                keys['myFCT'] = FCT.objects.get(
                    food_item_id=tmp01.myFCT.food_item_id)
                keys['selected_status'] = 0
                p = myCrop.objects.create(**keys)
# ---------------------
        form.instance.created_by = self.request.user
        form.instance.country_test = Countries.objects.filter(
            GID_2=form.instance.province).first()
        return super(Location_CreateView, self).form_valid(form)

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Location_CreateView, self).get_form_kwargs()
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
        context['myuser'] = self.request.user
        return context


class Location_UpdateView(LoginRequiredMixin, UpdateView):
    model =Location
    form_class =LocationForm
    template_name = 'myApp/Location_form.html'
    success_url = reverse_lazy('Location_list')

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Location_UpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['pk']
        return kwargs

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

#    def get_success_url(self, **kwargs):
#        return reverse_lazy('Location_list', kwargs = "")

    def form_valid(self, form):
        form.instance.country_test = Countries.objects.filter(
            GID_2=form.instance.province).first()
#        return super(Location_UpdateView, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
