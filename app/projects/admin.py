from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Project,Category,Tag,Image,Comment

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Comment)
