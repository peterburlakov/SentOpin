from django.db import models


class Search(models.Model):
    class Status(models.IntegerChoices):
        FINISHED = 1
        PENDING = 2
        IN_PROGRESS = 3
        FAILED = 4
    
    text = models.TextField()
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

    def __str__(self) -> str:
        return self.text


class Places(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    # we have id as primay, place_id as unque
    # place_id - from Google Places
    place_id = models.TextField(unique=True)
    name = models.TextField()

class Review(models.Model):
    place_id = models.ForeignKey(Places, on_delete=models.CASCADE)
    datetime = models.DateTimeField()