from django.contrib import admin
from .models import FCT, DRI, Location, Person, Crop_Individual, Crop_National
from .models import Crop_SubNational, Crop_Feasibility,Countries, Country_label
from .models import Profile, Crop_Name


# Register your models here.
admin.site.register(FCT)
admin.site.register(DRI)
admin.site.register(Location)
admin.site.register(Person)
admin.site.register(Crop_Individual)
admin.site.register(Crop_National)
admin.site.register(Crop_SubNational)
admin.site.register(Crop_Feasibility)
admin.site.register(Crop_Name)
admin.site.register(Countries)
admin.site.register(Country_label)
admin.site.register(Profile)


# Register your models here.
