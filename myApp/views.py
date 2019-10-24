from django.shortcuts import render, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core import serializers

from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import FCT, Person, DRI, DRI_women, Family, Crop
from .forms import Order_Key_Form, FamilyForm, Person_Create_Form, CropForm
from django.db.models import Q, Sum

# for user registration
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login


# Create your views here.
class FCTdatable_View(TemplateView):
    template_name = "myApp/FCT_datable.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Family.objects.get(id = self.kwargs['familyid'])
        context['myid'] = Family.objects.get(id = self.kwargs['familyid']).id
        context['country'] = Family.objects.get(id = self.kwargs['familyid']).country
        context['region'] = Family.objects.get(id = self.kwargs['familyid']).region
        context['nutrition_target'] = Family.objects.get(id = self.kwargs['familyid']).nutrition_target
        context['dri_p'] = Family.objects.get(id = self.kwargs['familyid']).protein
        context['dri_v'] = Family.objects.get(id = self.kwargs['familyid']).vita
        context['dri_f'] = Family.objects.get(id = self.kwargs['familyid']).fe
        context['sex'] = Person.objects.filter(familyid = self.kwargs['familyid'])[0].sex
        context['age'] = Person.objects.filter(familyid = self.kwargs['familyid'])[0].age
        tmp = Family.objects.get(id = self.kwargs['familyid']).crop_list
        crops = []
        if ('-' in tmp):
            for crop in tmp.split('-'):
                crops.append(FCT.objects.get(food_item_id = crop).Food_name)
        context['crop_list'] = crops
        return context


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

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(Family_CreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = '0'
        return kwargs


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
    context_object_name = 'families'
    model = Person

    def get_queryset(self):
        queryset = super().get_queryset().filter(familyid = self.kwargs['familyid']).order_by('age')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Family.objects.get(id = self.kwargs['familyid'])
        context['myid'] = Family.objects.get(id = self.kwargs['familyid']).id
        context['country'] = Family.objects.get(id = self.kwargs['familyid']).country
        context['region'] = Family.objects.get(id = self.kwargs['familyid']).region
        context['nutrition_target'] = Family.objects.get(id = self.kwargs['familyid']).nutrition_target
        context['dri_p'] = Family.objects.get(id = self.kwargs['familyid']).protein
        context['dri_v'] = Family.objects.get(id = self.kwargs['familyid']).vita
        context['dri_f'] = Family.objects.get(id = self.kwargs['familyid']).fe
        context['crop_list'] = Family.objects.get(id = self.kwargs['familyid']).crop_list
        context['sex'] = Person.objects.filter(familyid = self.kwargs['familyid'])[0].sex
        context['age'] = Person.objects.filter(familyid = self.kwargs['familyid'])[0].age
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
        context['country'] = Family.objects.get(id = self.kwargs['familyid']).country
        context['region'] = Family.objects.get(id = self.kwargs['familyid']).region
        context['nutrition_target'] = Family.objects.get(id = self.kwargs['familyid']).nutrition_target
        context['dri_p'] = Family.objects.get(id = self.kwargs['familyid']).protein
        context['dri_v'] = Family.objects.get(id = self.kwargs['familyid']).vita
        context['dri_f'] = Family.objects.get(id = self.kwargs['familyid']).fe
        context['sex'] = Person.objects.filter(familyid = self.kwargs['familyid'])[0].sex
        context['age'] = Person.objects.filter(familyid = self.kwargs['familyid'])[0].age

        tmp = Family.objects.get(id = self.kwargs['familyid']).crop_list
        context['crop_list2'] = tmp

        crops = []
        if ('-' in tmp):
            for crop in tmp.split('-'):
                crops.append(FCT.objects.get(food_item_id = crop).Food_name)
        context['crop_list'] = crops
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

def registCrops(request, familyid, items):
    tmp = Family.objects.get(id = familyid).crop_list
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

    for item in selectedItem:
        if item in crops:
            a += 1 #  do nothing"
        else:
#            register new crop here"
            newcrop = {}
            myfood = FCT.objects.get(food_item_id = item)
            if myfood.Protein == '':
                myfood.Protein = 0
            if myfood.VITA_RAE == '':
                myfood.VITA_RAE = 0
            if myfood.FE == '':
                myfood.FE = 0

            mytarget = Family.objects.get(pk = familyid)
            newcrop['food_item_id'] = item
            newcrop['Food_name'] = myfood.Food_name
            newcrop['food_grp'] = myfood.Food_grp
            newcrop['protein'] = myfood.Protein
            newcrop['vita'] = myfood.VITA_RAE
            newcrop['fe'] = myfood.FE
            newcrop['familyid'] = familyid

            if myfood.Protein >0:
                newcrop['food_wt_p'] = round(mytarget.protein *100 / myfood.Protein, 1)
            else:
                newcrop['food_wt_p'] = 0

            if myfood.VITA_RAE > 0:
                newcrop['food_wt_va'] = round(mytarget.vita *100 / myfood.VITA_RAE, 1)
            else:
                newcrop['food_wt_va'] = 0

            if myfood.FE > 0:
                newcrop['food_wt_fe'] = round(mytarget.fe *100 / myfood.FE, 1)
            else:
                newcrop['food_wt_fe'] = 0

            p = Crop.objects.create(**newcrop)

    for crop in crops:
        if crop in selectedItem:
            a += 1 #  do nothing"
        else:
#            delete crop here"
            p = Crop.objects.filter(food_item_id=crop).delete()

#   update crop_list to match with DCT_datatable selection
    Family.objects.filter(id = familyid).update(crop_list = items)

#    move to crop list page
    myURL = reverse_lazy('crop_list', kwargs = {'familyid': familyid})
    return HttpResponseRedirect(myURL)

def funcTest(request, familyid):
#    move to crop list page
    myURL = reverse_lazy('crop_list', kwargs = {'familyid': familyid})
    return HttpResponseRedirect(myURL)

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
