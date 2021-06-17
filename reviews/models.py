from django.db import models


class Search(models.Model):
    text = models.TextField()


class Places(models.Model):
    search = models.ForeignKey(Search)
    # we have id as primay, place_id as unque
    # place_id - from Google Places
    place_id = models.TextField(unique=True)
    name = models.TextField()

class Review(models.Model):
    place_id = models.ForeignKey(Places)
    datetime = models.DateTimeField()