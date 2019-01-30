# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger #, Paginator
from .digg_paginator import DiggPaginator as Paginator
from .models import Concert, Venue
from django.db.models import Q


def calendar(request):
    now = datetime.datetime.now()
    concerts = Concert.objects.filter(date__gte=now).order_by('date')
    page = request.GET.get('page', 1)
    paginator = Paginator(concerts, 24, body=3, tail=1, margin=2)
    try:
        concerts = paginator.page(page)
    except PageNotAnInteger:
        concerts = paginator.page(1)
    except EmptyPage:
        concerts = paginator.page(paginator.num_pages)
    return render(request, 'concerts/calendar.html', {'concerts': concerts})


def past_events(request):
    now = datetime.datetime.now()
    concerts = Concert.objects.filter(date__lt=now).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(concerts, 24, body=3, tail=1, margin=2)
    try:
        concerts = paginator.page(page)
    except PageNotAnInteger:
        concerts = paginator.page(1)
    except EmptyPage:
        concerts = paginator.page(paginator.num_pages)
    return render(request, 'concerts/calendar.html', {'concerts': concerts})


def venues(request):
    venues = Venue.objects.all().order_by('name')
    return render(request, 'concerts/venues.html', {'venues': venues})


def venue_events(request, slug):
    now = datetime.datetime.now()
    concerts = Concert.objects.filter(venue__slug=slug)\
                              .filter(date__gte=now)\
                              .order_by('date')
    page = request.GET.get('page', 1)
    paginator = Paginator(concerts, 24, body=3, tail=1, margin=2)
    try:
        concerts = paginator.page(page)
    except PageNotAnInteger:
        concerts = paginator.page(1)
    except EmptyPage:
        concerts = paginator.page(paginator.num_pages)
    if concerts:
        return render(request, 'concerts/calendar.html', {'concerts': concerts})
    else:
        return render(request, 'concerts/no_concerts.html', {'slug': slug})


def past_venue_events(request, slug):
    now = datetime.datetime.now()
    concerts = Concert.objects.filter(venue__slug=slug)\
                              .filter(date__lt=now).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(concerts, 24, body=3, tail=1, margin=2)
    try:
        concerts = paginator.page(page)
    except PageNotAnInteger:
        concerts = paginator.page(1)
    except EmptyPage:
        concerts = paginator.page(paginator.num_pages)
    if concerts:
        return render(request, 'concerts/calendar.html', {'concerts': concerts})
    else:
        return render(request, 'concerts/no_concerts.html')


def about(request):
    return render(request, "concerts/about.html")


def search(request):
    if request.method == 'GET':
        search_term = request.GET.get('search')
        try:
            headliners = Concert.objects.filter(headliner__search=search_term)
            notes = Concert.objects.filter(notes__search=search_term)
            support = Concert.objects.filter(support__search=search_term)
            venues = Concert.objects.filter(venue__name__search=search_term)
            prices = Concert.objects.filter(price__search=search_term)
            ages = Concert.objects.filter(age__search=search_term)
            results = headliners | notes | support | venues | prices | ages
        except Concert.DoesNotExist:
            results = None
        template = "concerts/search.html"
        context = {"results" : results, "search_term" : search_term}
        return render(request, template, context)
    else:
        return render(request, "concerts/search.html", {})


def filter_by_date(request):
    if request.method == "GET":
        # get start and end dates from the template
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        # try to find things on or between those dates
        try:
            concerts = Concert.objects.filter(
                Q(date__gte=start_date) & Q(date__lte=end_date)
            )
        except Concert.DoesNotExist:
            results = None
        # convert our date strings to datetime objects for better rendering
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        # let's render it, yo
        template = "concerts/calendar.html"
        context = {
            "concerts" : concerts,
            "start_date" : start_date,
            "end_date" : end_date
        }
        return render(request, template, context)
    else:
        return render(request, "concerts/calendar.html", {})
