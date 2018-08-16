from django.contrib import admin
from . import models
from . models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display  = ['title','updated','timestamp']
	list_display_links = ['updated']
	list_filter = ["updated","timestamp"]
	search_fields = ["title","content"]
	list_editable = ["title"]
	class  Meta:
		model = Post
# Register your models here.
admin.site.register(models.Post,PostModelAdmin)