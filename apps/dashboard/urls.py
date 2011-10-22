from django.conf.urls.defaults import *
from dashboard.views import DashboardView

urlpatterns = patterns('',
    url(r'', DashboardView.as_view()),
)
