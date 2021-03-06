from urllib.parse import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator ,EmptyPage, PageNotAnInteger #for page list Pagination


# Create your views here.
def post_home(request):
	return HttpResponse("<h1>The home Page</h1>")

def post_create(request): 
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		#mesages Success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {"form":form}
	return render(request, "post_form.html" , context)

	
def post_detail(request, id=None):
	instance = get_object_or_404(Post, id=id)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	share_string = quote_plus(instance.content)
	context = {
			"title":instance.title,
			"instance":instance,
			"share_string":share_string,
		}
		#mesages Success
	return render(request,'post_detail.html',context)

def post_list(request):

	today = timezone.now().date()
	##Getting or post from database 
	queryset_list = Post.objects.active()#.order_by('-timestamp')
	if request.user.is_staff or request.user.is_superuser:#When is the user and the super user logged in can see all post including draft
		queryset_list = Post.objects.all()

	query = request.GET.get("q")#For the searching Item 
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__username__icontains= query)
			).distinct()

	paginator = Paginator(queryset_list, 4)#Show 25 post per page
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not integer , deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of range(e.g. 9999),deliver last page of result
		queryset = paginator.page(paginator.num_pages)
	context = {
			"object_list":queryset,
			"title":"List",
			"page_request_var":page_request_var,
			"today":today,
		}
	return render(request,'post_list.html',context)
	

def post_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None , request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully Saved")
		return HttpResponseRedirect(instance.get_absolute_url())#Redirect the user to the updated Url

	context = {
			"title":instance.title,
			"instance":instance,
			"form":form
		}
	return render(request,'post_form.html',context)
 

def post_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Successfully Deleted")
	return redirect("posts:list")#Redirect the user to the updated Url