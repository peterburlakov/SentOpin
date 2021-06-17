from django.contrib import admin

from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)


# Register your models here.
from .models import Search, Places, Review

admin.site.register(Search)
admin.site.register(Places)
admin.site.register(Review)