from django.db import models


class Status(models.IntegerChoices):
    PENDING = 1
    IN_PROGRESS = 2
    FINISHED = 3
    FAILED = 4


class Search(models.Model):
    text = models.CharField(max_length=255)
    status = models.IntegerField(choices=Status.choices,
                                 default=Status.PENDING)

    def __str__(self) -> str:
        return self.text


class Places(models.Model):
    
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices,
                                 default=Status.PENDING)
    # we have id as primay, place_id as unque
    # place_id - from Google Places
    place_id = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    business_status = models.CharField(max_length=255)
    formatted_address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    user_ratings_total = models.PositiveIntegerField()
    state = models.CharField(max_length=255)
    types = models.JSONField()
    is_agent = models.BooleanField(default=False)


class Review(models.Model):
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    url = models.TextField()
    reviewer = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    reply = models.JSONField(null=True, blank=True)
    language = models.CharField(max_length=10)
    # review_id = id in original data
    review_id = models.CharField(unique=True, max_length=255)
    likes = models.PositiveIntegerField()

    # from expert.ai
    sentiment_overall = models.DecimalField(max_digits=4, decimal_places=1,null=True, blank=True)
    expertai_classification = models.JSONField(null=True, blank=True)
    expertai_entities= models.JSONField(null=True, blank=True)
    expertai_mainLemmas = models.JSONField(null=True, blank=True)
    expertai_mainPhrases=models.JSONField(null=True, blank=True)
    expertai_mainSyncons=models.JSONField(null=True, blank=True)
    expertai_sentiment_items =models.JSONField(null=True, blank=True)
    expertai_topics=models.JSONField(null=True, blank=True)


# "place_id";"datetime";"id";"language";"rating";"likes";"reviewer";
# "url"
# "sentiment.overall";
# "text";"reply";"place_name";"place_rating";"place_user_ratings_total";
# "place_formatted_address";"place_state";"place_types";"place_location";
# "latitude";"longitude";
# "expertai_classification";"expertai_entities";"expertai_mainLemmas";
# "expertai_mainPhrases";"expertai_mainSyncons";"expertai_sentiment.items";
# "expertai_topics";

