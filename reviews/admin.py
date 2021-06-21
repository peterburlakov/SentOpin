from django.contrib import admin

from django.contrib.auth.models import Group, User
#from django_admin_listfilter_dropdown.filters import DropdownFilter
from baton.admin import InputFilter

admin.site.unregister(Group)
admin.site.unregister(User)


# Register your models here.
from .models import Search, Places, Review

from baton.admin import InputFilter

class NameFilter(InputFilter):
    parameter_name = 'name'
    title = 'name'

    def queryset(self, request, queryset):
        if self.value() is not None:
            search_term = self.value()
            return queryset.filter(
                name__icontains=search_term
            )

@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lat', 'lng', 'rating', )
    list_filters = (
         (NameFilter),
    )
 
@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'status' )
 
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'sentiment_overall', )
