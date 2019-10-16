from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers

from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FCT, Person, DRI, DRI_women, Family, Crop
from .forms import Order_Key_Form, FamilyForm, Person_Create_Form, CropForm
from django.db.models import Q, Sum


# Create your views here.
class FCTdatable_View(TemplateView):
    template_name = "myApp/FCT_datable.html"

class Trial_View(TemplateView):
    template_name = "myApp/trial.html"

class TestOfflineView(TemplateView):
    template_name = "myApp/offline/index.html"

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

class Family_DeleteView(LoginRequiredMixin, DeleteView):
    model = Family
    template_name = 'myApp/family_confirm_delete.html'
    success_url = reverse_lazy('Family_index')

class Family_CreateView(LoginRequiredMixin, CreateView):
    model = Family
    form_class = FamilyForm
    template_name = 'myApp/family_form.html'
    success_url = reverse_lazy('Family_index')

class Family_UpdateView(LoginRequiredMixin, UpdateView):
    model = Family
    form_class = FamilyForm
    template_name = 'myApp/family_form.html'
    success_url = reverse_lazy('Family_index')

class Person_ListView(LoginRequiredMixin, ListView):
    template_name = 'myApp/person_list.html'  # この行でテンプレート指定
    context_object_name = 'families'
    model = Person

    def get_queryset(self):
        queryset = super().get_queryset().filter(familyid = self.kwargs['familyid']).order_by('age')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Family.objects.get(id = self.kwargs['familyid'])
        context['myid'] = Family.objects.get(id = self.kwargs['familyid']).id
        context['dri_p'] = Family.objects.get(id = self.kwargs['familyid']).protein
        context['dri_v'] = Family.objects.get(id = self.kwargs['familyid']).vita
        context['dri_f'] = Family.objects.get(id = self.kwargs['familyid']).fe
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
        myid = self.kwargs['familyid']
        aggregates = Person.objects.aggregate(
            protein1 = Sum('protein', filter = Q(familyid = myid)),
            vita1 = Sum('vita', filter = Q(familyid = myid)),
            fe1 = Sum('fe', filter = Q(familyid = myid)),
        )
        if aggregates:
            rec = Family.objects.filter(id = myid).first()
            rec.protein = aggregates['protein1']
            rec.vita = aggregates['vita1']
            rec.fe = aggregates['fe1']
            rec.save()

        mySize = Person.objects.filter(familyid = myid).count()
        if mySize > 0:
            rec = Family.objects.filter(id = myid).first()
            rec.size = mySize
            rec.save()

        return HttpResponseRedirect(self.get_success_url())

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
        aggregates = Person.objects.aggregate(
            protein1 = Sum('protein', filter = Q(familyid = myid)),
            vita1 = Sum('vita', filter = Q(familyid = myid)),
            fe1 = Sum('fe', filter = Q(familyid = myid)),
        )
        if aggregates:
            rec = Family.objects.filter(id = myid).first()
            rec.protein = aggregates['protein1']
            rec.vita = aggregates['vita1']
            rec.fe = aggregates['fe1']
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
        aggregates = Person.objects.aggregate(
            protein1 = Sum('protein', filter = Q(familyid = myid)),
            vita1 = Sum('vita', filter = Q(familyid = myid)),
            fe1 = Sum('fe', filter = Q(familyid = myid)),
        )
        if aggregates:
            rec = Family.objects.filter(id = myid).first()
            rec.protein = aggregates['protein1']
            rec.vita = aggregates['vita1']
            rec.fe = aggregates['fe1']
            rec.save()

        mySize = Person.objects.filter(familyid = myid).count()
        if mySize > 0:
            rec = Family.objects.filter(id = myid).first()
            rec.size = mySize
            rec.save()

        return HttpResponseRedirect(success_url)

class Crop_ListView(LoginRequiredMixin, ListView):
    model = Crop
    context_object_name = "mylist"
    template_name = 'myApp/crop_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(familyid = self.kwargs['familyid'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Family.objects.get(id = self.kwargs['familyid'])
        context['myid'] = Family.objects.get(id = self.kwargs['familyid']).id
        context['dri_p'] = Family.objects.get(id = self.kwargs['familyid']).protein
        context['dri_v'] = Family.objects.get(id = self.kwargs['familyid']).vita
        context['dri_f'] = Family.objects.get(id = self.kwargs['familyid']).fe
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

    def get_success_url(self, **kwargs):
        return reverse_lazy('crop_list', kwargs = {'familyid': self.kwargs['familyid']})


class Crop_UpdateView(LoginRequiredMixin, UpdateView):
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
        kwargs = super(Crop_UpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['familyid']
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse_lazy('crop_list', kwargs = {'familyid': self.kwargs['familyid']})

def getNFA(request, store_id):
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
        results = Crop.objects.all()
    if store_id == 6:
        results = Family.objects.all()

    jsondata = serializers.serialize('json',results)
    return HttpResponse(jsondata)
