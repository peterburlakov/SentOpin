from django.contrib import admin

from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)


# Register your models here.
from .models import Search, Places, Review

@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Search)
admin.site.register(Review)