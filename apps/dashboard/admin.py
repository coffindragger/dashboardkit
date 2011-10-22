from django.contrib import admin 
from dashboard.models import *

class OwnerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, *args, **kwargs):
        if not obj.owner:
            obj.owner = request.user
        super(OwnerAdmin, self).save_model(request, obj, *args, **kwargs)


class DashboardAdmin(OwnerAdmin):
    class DashboardGadgetInline(admin.TabularInline):
        model = DashboardGadget
        extra = 0
    list_display = ('__unicode__','owner')
    inlines = (DashboardGadgetInline,)
admin.site.register(Dashboard, DashboardAdmin)


class GadgetAdmin(OwnerAdmin):
    list_display = ('__unicode__','magic_cookie','owner')
admin.site.register(Gadget, GadgetAdmin)
