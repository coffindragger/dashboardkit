from django.views.generic import DetailView
from dashboard.models import *
from django import http


class DashboardView(DetailView):
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'dashboard'
    model = Dashboard

    def get_object(self):
        try:
            return Dashboard.objects.get(url=self.request.path, status__in=(STATUS_LIVE,STATUS_WIP))
        except Dashboard.DoesNotExist:
            raise http.Http404

