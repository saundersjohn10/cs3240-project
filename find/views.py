from django.shortcuts import render
from .models import Posting
from django.views import generic
from datetime import datetime
from django.http import HttpResponseRedirect
from user_profile.models import Rider
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from django.contrib import messages
from django.core.paginator import Paginator

from datetime import datetime, timezone, timedelta

flagPrice = False
flagDate = False
flagSearch = False
flagPost = False
l=[]
flagp=True
flagr=True
flagd=True

def find(request):
	global flagPrice
	global flagDate
	global flagSearch
	global flagPost
	global l
	l=[]
	flagPrice=False
	flagDate=False
	flagSearch=False
	flagPost=False
	# print("flagSearch", flagSearch)
	posts = getRelevantRides().order_by('-date')
	paginator = Paginator(posts, 10)
	page = request.GET.get('page')
	posts = paginator.get_page(page)

	return render(request, 'find/find_ride.html', {'title': 'Profile', 'postings_list' : posts})


def sortByPostingDate(request):
	global flagd
	global flagSearch
	global flagPost
	global l
	flagPost=True
	if flagd:
		flagd=False
		if flagSearch:
			# printpostings_list(l[0])
			l.sort(key=lambda x: x[3], reverse=True)
			ans=[]
			for post in l:
				ans.append(post[0])
			# flagSearch = False
			paginator = Paginator(ans, 10)
			page = request.GET.get('page')
			ans = paginator.get_page(page)
			return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': ans})
		posts = getRelevantRides().order_by('-date')
		paginator = Paginator(posts, 10)
		page = request.GET.get('page')
		posts = paginator.get_page(page)	
		return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': posts, 'flagDate': flagd})
	else:
		flagd=True
		if flagSearch:
			# print(l[0])
			l.sort(key=lambda x: x[3])
			ans=[]
			for post in l:
				ans.append(post[0])
			# flagSearch = False
			paginator = Paginator(ans, 10)
			page = request.GET.get('page')
			ans = paginator.get_page(page)
			return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': ans})
		posts = getRelevantRides().order_by('date')
		paginator = Paginator(posts, 10)
		page = request.GET.get('page')
		posts = paginator.get_page(page)	
		return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': posts, 'flagDate': flagd})


def sortByRidingDate(request):
	global flagr
	global flagDate
	flagDate=True
	global l
	global flagSearch
	if flagr:
		flagr = False
		if flagSearch:
			# print(l)
			# print(l[0][1])
			l.sort(key=lambda x: x[1], reverse=True)
			ans=[]
			for post in l:
				ans.append(post[0])
			# flagSearch = False
			paginator = Paginator(ans, 10)
			page = request.GET.get('page')
			ans = paginator.get_page(page)
			return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': ans})
		posts = getRelevantRides().order_by('-riding_date')
		paginator = Paginator(posts, 10)
		page = request.GET.get('page')
		posts = paginator.get_page(page)
		return render(request, 'find/find_ride.html', {'title': 'Profile', 'postings_list': posts, 'flagRide': flagr})
	else:
		flagr = True
		if flagSearch:
			l.sort(key=lambda x: x[1])
			ans=[]
			for post in l:
				ans.append(post[0])
			# flagSearch = False
			paginator = Paginator(ans, 10)
			page = request.GET.get('page')
			ans = paginator.get_page(page)
			return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': ans})
		posts = getRelevantRides().order_by('riding_date')
		paginator = Paginator(posts, 10)
		page = request.GET.get('page')
		posts = paginator.get_page(page)
		return render(request, 'find/find_ride.html',
				  {'title': 'Profile', 'postings_list': posts, 'flagRide': flagr})

def sortByPrice(request):
	global flagp
	global flagPrice
	global flagSearch
	flagPrice = True
	global l
	print("flagSearch", flagSearch)
	if flagp:
		flagp=False
		print("flagp", flagp)
		if flagSearch:
			l.sort(key=lambda x: x[2])
			ans=[]
			for post in l:
				ans.append(post[0])
			# flagSearch = False
			paginator = Paginator(ans, 10)
			page = request.GET.get('page')
			ans = paginator.get_page(page)
			return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': ans})
			
		posts = getRelevantRides().order_by('price')
		paginator = Paginator(posts, 10)
		page = request.GET.get('page')
		posts = paginator.get_page(page)
		return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': posts, 'flagPrice': flagp})
	else:
		print("flagp", flagp)
		flagp=True
		if flagSearch:
			l.sort(key=lambda x: x[2], reverse=True)
			ans=[]
			for post in l:
				ans.append(post[0])
			# flagSearch = False
			paginator = Paginator(ans, 10)
			page = request.GET.get('page')
			ans = paginator.get_page(page)
			return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': ans})
			
		posts = getRelevantRides().order_by('-price')
		paginator = Paginator(posts, 10)
		page = request.GET.get('page')
		posts = paginator.get_page(page)
		return render(request, 'find/find_ride.html',
					  {'title': 'Profile', 'postings_list': posts, 'flagPrice': flagp})


def search(request):

	global flagSearch
	flagSearch = True
	global flagPrice
	global flagDate
	global l

	if flagPrice:
		all = getRelevantRides().order_by('price')
		# flagPrice = False
	elif flagDate:
		all = getRelevantRides().order_by('-riding_date')
		# flagDate = False
	else:
		all = getRelevantRides().order_by('-date')
	location_to = request.POST['searchTo']
	if location_to != None and location_to != '':
		if (len(location_to) > 5 and location_to[-5:] == ", USA"):
			location_to = location_to[:-5]
		temp=[]	
		filtered = []
		for posting in all:
			if posting.location_to == location_to and isValid(posting):
				a=[posting, posting.riding_date,posting.price,posting.date]
				temp.append(a)
				filtered.append(posting)
		all = filtered
		l=temp
	location_from = request.POST['searchFrom']
	if location_from != None and location_from != '':
		if (len(location_from) > 5 and location_from[-5:] == ", USA"):
			location_from = location_from[:-5]

		filtered = []
		temp =[]
		for posting in all:
			if posting.location_from == location_from and isValid(posting):
				a=[posting, posting.riding_date,posting.price,posting.date]
				temp.append(a)
				filtered.append(posting)
		all = filtered
		l=temp
	riding_date = request.POST['riding_date']
	if riding_date != None and riding_date != '':

		riding_date = formatDate(riding_date)
		filtered = []
		temp=[]
		for posting in all:
			if str(str(posting.riding_date).split(" ")[0]) == str(riding_date) and isValid(posting):
				filtered.append(posting)
				a=[posting, posting.riding_date,posting.price]
				temp.append(a)
		all = filtered
		l = temp
	paginator = Paginator(all, 10)
	page = request.GET.get('page')
	all = paginator.get_page(page)
	return render(request, 'find/find_ride.html',
				  {'title': 'Profile', 'postings_list': all})
		

#called when rider requesting to join posting
def requestToJoinRide(request):

    query = Posting.objects.filter(posting_id=request.GET['id'])
    if query.count() > 0 :
        posting = Posting.objects.filter(posting_id=request.GET['id'])[0]
        posting.riders_requested = str(posting.riders_requested) + "," + str(request.user)
        posting.save()

        user = Rider.objects.filter(username=str(request.user))[0]
        user.rides_pending += request.GET['id'] + ","
        user.save()
        messages.success(request, 'Your Request Was Sent!')

    return HttpResponseRedirect('/')

#takes in date in format: November 1, 2019, returns format: 2019-11-1
def formatDate(date):
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
			  "November", "December"]
	date = date.split(" ")
	return date[2] + '-' + str(months.index(date[0]) + 1) + '-' + (date[1])[:-1]

def isValid(posting):
	if posting.location_to!=None and posting.location_from!=None and posting.riding_date!=None and posting.driver_name!=None:
		return True
	return False

class findView(generic.ListView):
	template_name = 'find/find_ride.html'
	context_object_name = 'postings_list'
	def get_queryset(self):
		return getRelevantRides()

class dateView(generic.ListView):
    template_name = 'find/find_ride_date.html'
    context_object_name = 'postings_list'

    def get_queryset(self):
    	# print("find ride")
    	return getRelevantRides().order_by('-riding_date')

class priceView(generic.ListView):
    template_name = 'find/find_ride_price.html'
    context_object_name = 'postings_list'

    def get_queryset(self):
    	return getRelevantRides().order_by('price')


class searchView(generic.ListView):
	model = Posting
	template_name = 'find/find_ride_search.html'
	context_object_name = 'postings_list'
	# queryset = Posting.objects.filter(location_to='Virginia Beach, VA')

	def get_queryset(self):
		location_to = self.request.GET.get('location_to')
		# print(self.request.GET.get('location_to')+"location_to")
		location_from = self.request.GET.get('location_from')
		year = self.request.GET.get('date_year')
		month = self.request.GET.get('date_month')
		day = self.request.GET.get('date_day')

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
			# print("method goes here")
			return Posting.objects.filter(location_to=location_to)
		elif location_to =="" and location_from != "" and s=="--":
			return Posting.objects.filter(location_from=location_from)
		elif location_to =="" and location_from == "" and s=="--":
			return Posting.objects.filter(location_from=location_from)
		else:
			return Posting.objects.filter(location_to=location_to, location_from=location_from, riding_date__date=s)
#return the rides that still have spots left and date still hasn't happended
def getRelevantRides():

	return Posting.objects.filter(num_passengers__gte=1, riding_date__gte=(datetime.now(timezone.utc) - timedelta(hours=5)))


