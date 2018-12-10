import json
import dateparser
import re
import webbrowser as wb
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from concerts.models import Concert, Venue
from django.utils.text import slugify
from django.db.utils import DataError

# To run this code use:
# python manage.py load_concerts name_of_file.json

class Command(BaseCommand):
    help = "Load JSON concert data"

    def add_arguments(self, parser):
        parser.add_argument('concert_file', type=str)

    def handle(self, *args, **options):
        with open("json/" + options['concert_file']) as f:
            data = json.load(f)

        venues_successfully_created = []
        venues_failed_to_be_created = []
        concerts_without_venues = []
        concerts_successfully_created = []
        duplicate_concerts_not_created = []
        concerts_not_created_data_error = []

        for concert in data:

            # TODO in filter_and_combine.py -- add this there, remove here
            # encode to utf-8 to avoid encoding errors later
            # remove the awful right and left apostrophes that ruin so much
            for key, value in concert.iteritems():
                try:
                    concert[key] = value.encode("utf-8")
                    concert[key] = re.sub(u"(\u2018|\u2019)", "'", value)
                except AttributeError:
                    pass

            # TODO in moonbot scraper -- add this there, remove it here
            if 'ticket_link' in concert:
                del concert['ticket_link']

            # Now that we've prepped our data, start with the venue
            try:
                venue = Venue.objects.get(name=concert['venue'])
            except Venue.DoesNotExist:
                if 'venue_address' not in concert:
                    google = "https://www.google.com/search?q="
                    wb.open_new_tab(google + concert['venue'])
                    prompt = (
                        "Enter a street address for %s. " % concert['venue']
                    )
                    concert['venue_address'] = raw_input(prompt)
                if 'venue_website' not in concert:
                    concert['venue_website'] = ""
                if 'venue_slug' not in concert:
                    concert['venue_slug'] = slugify(concert['venue'])
                try:
                    venue = Venue.objects.create(
                        name=concert['venue'],
                        slug=concert['venue_slug'],
                        address=concert['venue_address'],
                        city="",
                        state="",
                        zip="",
                        website=concert['venue_website']
                    )
                    venues_successfully_created.append(concert['venue'])
                except:
                    venues_failed_to_be_created.append(concert['venue'])
                    continue # skip the concert if we fail to create a venue
            except KeyError:
                concerts_without_venues.append(concert)
                continue # skip the concert if there is no associated venue

            # Delete all the venue stuff from the dictionary since we now have
            # venues associated in our database.
            if 'venue' in concert:
                del concert['venue']
            if 'venue_address' in concert:
                del concert['venue_address']
            if 'venue_website' in concert:
                del concert['venue_website']
            if 'venue_slug' in concert:
                del concert['venue_slug']

            # Now creating the concert is just a matter of...
            try:
                Concert.objects.create(venue=venue, **concert)
                concerts_successfully_created.append(concert['slug'])
            except IntegrityError: # if slug already exists
                duplicate_concerts_not_created.append(concert['slug'])
                pass # if slug exists, just pass this concert
            except DataError:
                concerts_not_created_data_error.append(concert['slug'])

        print "Concerts created:", len(concerts_successfully_created)
        print "Duplicates not created:", len(duplicate_concerts_not_created)
        print "Concerts with data errors:", len(concerts_not_created_data_error)
        print "Venues created: ", len(venues_successfully_created)
        print "Venues failed to be created:", len(venues_failed_to_be_created)
        print "Concerts without venues (WTF?):", len(concerts_without_venues)
