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
    class DashboardTeamInline(admin.TabularInline):
        model = DashboardTeam
        extra = 0
    list_display = ('__unicode__','owner')
    inlines = (DashboardGadgetInline,DashboardTeamInline)
admin.site.register(Dashboard, DashboardAdmin)


class GadgetAdmin(OwnerAdmin):
    class GadgetTeamInline(admin.TabularInline):
        model = GadgetTeam
        extra = 0
    list_display = ('__unicode__','magic_cookie','owner')
    inlines = (GadgetTeamInline,)
admin.site.register(Gadget, GadgetAdmin)
