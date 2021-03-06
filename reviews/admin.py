from django.contrib import admin

from django.contrib.auth.models import Group, User
#from django_admin_listfilter_dropdown.filters import DropdownFilter
from baton.admin import InputFilter, RelatedDropdownFilter, DropdownFilter
from django.utils.html import format_html

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
    list_display = ('id', 'name', 'lat', 'lng', 'rating', 'search')
    list_filters = (
         (NameFilter),
    )

    def search(self, obj):
        return obj.search.text 
 
@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'status', 'report' )

    @admin.display(empty_value='???')
    def report(self, obj):
         return format_html(
            f'<a href="/admin/reviews/search/{obj.id}/change/">Show</a> '
        )
  
    baton_form_includes = [
        ('dash.html', 'text', 'above', ),
    ]
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        some_dict = {'url_slug': {'children': object_id}}
        extra_context['some_dict'] = some_dict
        return super(SearchAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

     
 
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'sentiment_overall', 'place_name', 'search')

    class IdFilter(InputFilter):
        parameter_name = 'id'
        title = 'id'

        def queryset(self, request, queryset):
            if self.value() is not None:
                search_term = self.value()
                return queryset.filter(
                    id=search_term
                )

    class ClassificationFilter(InputFilter):
        parameter_name = 'classification'
        title = 'classification'

        def queryset(self, request, queryset):
            if self.value() is not None:
                search_term = self.value()
                return queryset.filter(
                    id=search_term
                )
    
    #list_filters = (
    #    IdFilter,
    #)

    list_filter = (
        # for ordinary fields
        (IdFilter),
        (ClassificationFilter),
         ('place', RelatedDropdownFilter),
    )

    def place_name(self, obj):
        return obj.place.name

    def search(self, obj):
        return obj.place.search.text 