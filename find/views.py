from django.shortcuts import render
from .models import Posting
from django.views import generic
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.contrib.postgres.search import SearchVector


class findView(generic.ListView):
	template_name = 'find/find_ride.html'
	context_object_name = 'postings_list'
	def get_queryset(self):
		print("method called")
		return Posting.objects.all()


class dateView(generic.ListView):
    template_name = 'find/find_ride_date.html'
    context_object_name = 'postings_list'

    def get_queryset(self):
    	# print("find ride")
    	return Posting.objects.all().order_by('-riding_date')

class priceView(generic.ListView):
    template_name = 'find/find_ride_price.html'
    context_object_name = 'postings_list'

    def get_queryset(self):
    	return Posting.objects.all().order_by('price')


class searchView(generic.ListView):
	model = Posting
	template_name = 'find/find_ride_search.html'
	context_object_name = 'postings_list'
	# queryset = Posting.objects.filter(location_to='Virginia Beach, VA')

	def get_queryset(self):
		location_to = self.request.GET.get('location_to')
		print(self.request.GET.get('location_to')+"location_to")
		location_from = self.request.GET.get('location_from')
		year = self.request.GET.get('date_year')
		month = self.request.GET.get('date_month')
		day = self.request.GET.get('date_day')
		hour = self.request.GET.get('date_hour')
		time = self.request.GET.get('date_time_of_day')
		minute = self.request.GET.get('date_min')
		s = year+ '-' +month+ '-' +day
		if location_to=="" and location_from != "" and s!="--":
			return Posting.objects.filter(location_from=location_from, riding_date__date=s)
		elif location_to!="" and location_from == "" and s!="--":
			return Posting.objects.filter(location_to=location_to, riding_date__date=s)
		elif location_to!="" and location_from != "" and s=="--":
			return Posting.objects.filter(location_to=location_to, location_from=location_from)
		elif location_to=="" and location_from == "" and s!="--":
			return Posting.objects.filter(riding_date__date=s)		
		elif location_to !="" and location_from == "" and s=="--":
			print("method goes here")
			return Posting.objects.filter(location_to=location_to)
		elif location_to =="" and location_from != "" and s=="--":	
			return Posting.objects.filter(location_from=location_from)
		elif location_to =="" and location_from == "" and s=="--":
			return Posting.objects.filter(location_from=location_from)	
		else:
			return Posting.objects.filter(location_to=location_to, location_from=location_from, riding_date__date=s)
