
from django.urls import path
from . import views

urlpatterns = [
    path('show/<int:search_id>', views.show, name='show'),
]