from django.conf.urls import url
from . import views
from .views import venue_events as v_events
from .views import past_venue_events as pv_events

app_name = 'concerts'

urlpatterns = [
    url(r'^$', views.calendar, name="calendar"),
    url(r'^past/$', views.past_events, name="past_events"),
    url(r'^venues/$', views.venues, name="venues"),
    url(r'^venues/(?P<slug>[\w-]+)/$', v_events, name="venue_events"),
    url(r'^venues/(?P<slug>[\w-]+)/past/$', pv_events, name="past_venue_events"),
    url(r'^date_filter/$', views.filter_by_date, name="date_filter"),
]
