# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=False)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=10, blank=True)
    zip = models.CharField(max_length=5, blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Concert(models.Model):
    AGE_CHOICES = (
        ('21+', '21+'),
        ('18+', '18+'),
        ('All Ages', 'All Ages'),
        ('Unknown', 'Unknown'),
    )
    headliner = models.CharField(max_length=100)
    date = models.DateField()
    slug = models.SlugField(max_length=100, unique=True, blank=False)
    support = models.CharField(max_length=150, blank=True)
    venue = models.ForeignKey(Venue) #on_delete=models.Protect ???
    time = models.CharField(max_length=100, blank=True)
    price = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    age = models.CharField(max_length=100, default='Unknown', choices=AGE_CHOICES)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.headliner

    class Meta:
        ordering = ('-date',)
