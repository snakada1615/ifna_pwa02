from django.contrib import admin
from .models import FCT, DRI, DRI_women, Family, Person, Crop, Countries


# Register your models here.
admin.site.register(FCT)
admin.site.register(DRI)
admin.site.register(DRI_women)
admin.site.register(Family)
admin.site.register(Person)
admin.site.register(Crop)
admin.site.register(Countries)
