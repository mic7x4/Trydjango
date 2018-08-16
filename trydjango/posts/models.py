from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save

from django.conf import settings
from django.utils.text import slugify

from django.utils import timezone
# Create your models here.


class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1,on_delete=models.CASCADE)
	#The format of the post 
	title = models.CharField(max_length = 120)
	slug = models.SlugField(unique = True)
	image = models.ImageField(upload_to = upload_location ,null= True, blank= True, width_field="width_field", height_field= "height_field")
	height_field = models.IntegerField(default= 0)
	width_field = models.IntegerField(default= 0)
	content  = models.TextField()
	draft = models.BooleanField(default= False)
	publish = models.DateField(auto_now = False, auto_now_add = False)
	updated= models.DateTimeField(auto_now = True , auto_now_add = False)#Everytime it saved into database this will be set
	timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)#Set when it added to the database

	objects = PostManager()
	#This is used for Python2
	def __unicode__(self):
		return self.title
		

	#This is used for Python3
	def __str__(self):
		return self.title
		
	#this function is used to return the cannonical URL for an Object 
	def get_absolute_url(self):
		return reverse("posts:detail",kwargs={'id':self.id})

	#Used to get The post by id or The timestamp it been created
	class Meta:
		ordering = ["-timestamp","-updated"] #"-id"

#Recursive Function
def create_slug(instance, new_slug =None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug= new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
	# slug = slugify(instance.title)
	# #slugg change the title like Tessla item 1 -> tesla-item-1
	# exists = Post.objects.filter(slug=slug).exists()
	# if exists:
	# 	slug = "%s-%s" %(slugify(instance.title), instance.id)
	# instance.slug = slug

pre_save.connect(pre_save_post_receiver, sender=Post)
