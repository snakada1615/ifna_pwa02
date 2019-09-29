from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FCT, FamilyMember, DRI, DRI_women, Family, Crop
from .forms import Order_Key_Form


# Create your views here.
class TestView(TemplateView):
    template_name = "myApp/index.html"

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

class FamilyMember_List(LoginRequiredMixin, ListView):
    template_name = 'myApp/familymember_list.html'  # この行でテンプレート指定
    context_object_name = 'families'
    model = FamilyMember

    def get_queryset(self):
        queryset = super().get_queryset().filter(familyid = self.kwargs['familyid']).order_by('age')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = FamilyMember.objects.get(id = self.kwargs['familyid'])
        context['myid'] = FamilyMember.objects.get(id = self.kwargs['familyid']).id
        context['dri_p'] = FamilyMember.objects.get(id = self.kwargs['familyid']).protein
        context['dri_v'] = FamilyMember.objects.get(id = self.kwargs['familyid']).vita
        context['dri_f'] = FamilyMember.objects.get(id = self.kwargs['familyid']).fe
        context['sum_p'] = FamilyMember.objects.get(id = self.kwargs['familyid']).protein_s
        context['sum_v'] = FamilyMember.objects.get(id = self.kwargs['familyid']).vita_s
        context['sum_f'] = FamilyMember.objects.get(id = self.kwargs['familyid']).fe_s
        return context

'''
# 登録画面
class FamilyCreateView(LoginRequiredMixin, CreateView):
    model = Family
    form_class = Family_Create_Form

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(FamilyCreateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['familyid']
        return kwargs

    def get_context_data(self, **kwargs):
        myid = self.kwargs['familyid']
        mydata = FamilyList.objects.get(id = myid)
        context = super().get_context_data(**kwargs)
        context['myid'] = myid
        context['name'] = mydata
        context["families"] = Family.objects.filter(familyid = self.kwargs['familyid']).order_by('age')
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('family_list', kwargs = {'familyid': self.kwargs['familyid']})

    def form_valid(self, form):
        self.object = form.save()
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        myid = self.kwargs['familyid']
        aggregates = Family.objects.aggregate(
            protein1 = Sum('protein', filter = Q(familyid = myid)),
            vita1 = Sum('vita', filter = Q(familyid = myid)),
            fe1 = Sum('fe', filter = Q(familyid = myid)),
        )
        if aggregates:
            rec = FamilyList.objects.filter(id = myid).first()
            rec.protein = aggregates['protein1']
            rec.vita = aggregates['vita1']
            rec.fe = aggregates['fe1']
            rec.save()

        mySize = Family.objects.filter(familyid = myid).count()
        if mySize > 0:
            rec = FamilyList.objects.filter(id = myid).first()
            rec.size = mySize
            rec.save()

        return HttpResponseRedirect(self.get_success_url())

# 更新画面
class FamilyUpdateView(LoginRequiredMixin, UpdateView):
    model = Family
    form_class = Family_Create_Form

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(FamilyUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['myid'] = self.kwargs['familyid']
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        myid = self.kwargs['familyid']
        aggregates = Family.objects.aggregate(
            protein1 = Sum('protein', filter = Q(familyid = myid)),
            vita1 = Sum('vita', filter = Q(familyid = myid)),
            fe1 = Sum('fe', filter = Q(familyid = myid)),
        )
        if aggregates:
            rec = FamilyList.objects.filter(id = myid).first()
            rec.protein = aggregates['protein1']
            rec.vita = aggregates['vita1']
            rec.fe = aggregates['fe1']
            rec.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        myid = self.kwargs['familyid']
        mydata = FamilyList.objects.get(id = myid)
        context = super().get_context_data(**kwargs)
        context['name'] = mydata
        context['myid'] = myid
        context["families"] = Family.objects.filter(familyid = self.kwargs['familyid']).order_by('age')
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('family_list', kwargs = {'familyid': self.kwargs['familyid']})


# 削除画面
class FamilyDeleteView(LoginRequiredMixin, DeleteView):
    model = Family

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['familyid'] = self.kwargs['familyid']
        return context

    def get_success_url(self, **kwargs):
        if  kwargs != None:
            return reverse_lazy('family_list', kwargs = {'familyid': self.kwargs['familyid']})
        else:
            return reverse_lazy('family_list', args = (self.object.id,))

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        success_url = self.get_success_url()

        myid = self.kwargs['familyid']
        aggregates = Family.objects.aggregate(
            protein1 = Sum('protein', filter = Q(familyid = myid)),
            vita1 = Sum('vita', filter = Q(familyid = myid)),
            fe1 = Sum('fe', filter = Q(familyid = myid)),
        )
        if aggregates:
            rec = FamilyList.objects.filter(id = myid).first()
            rec.protein = aggregates['protein1']
            rec.vita = aggregates['vita1']
            rec.fe = aggregates['fe1']
            rec.save()

        mySize = Family.objects.filter(familyid = myid).count()
        if mySize > 0:
            rec = FamilyList.objects.filter(id = myid).first()
            rec.size = mySize
            rec.save()

        return HttpResponseRedirect(success_url)

'''
