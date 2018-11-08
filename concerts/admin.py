# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Venue, Concert


class ConcertAdmin(admin.ModelAdmin):
    list_display = ('headliner', 'support', 'venue', 'date', 'time', 'price')
    search_fields = ('headliner', 'date')

class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'website')


admin.site.register(Venue, VenueAdmin)
admin.site.register(Concert, ConcertAdmin)
