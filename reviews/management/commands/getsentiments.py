import requests
import googlemaps
import time
import pprint
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Review, Search, Places, Status
from tenacity import retry, wait_random, stop_after_attempt
from django.db import IntegrityError
from expertai.nlapi.cloud.client import ExpertAiClient
import os


class Command(BaseCommand):
    help = 'Collect sentiments'

    def handle(self, *args, **options):
        process_sentiments_all()
        self.stdout.write(self.style.SUCCESS(
            'Successfully finished process_reviews'))


client = ExpertAiClient()
taxonomy = 'iptc'
language = 'en'

# text = "I don't have Liberty Mutual Insurance but I get to see that totally unrealistic commercial 20 times a day....Really, too busy with two kids to handle her own business...Liberty stands with her!!! but the really bad part of that commercial is the woman with a bunch of kids running around a car repair shop...Kids are running rampant at the garage....This will never happen at any reputable garage!!! (unless of course Liberty Mutual is insuring the car repair shop owner) He better have some really great coverage when a car falls off the lift and falls on those unruly kids running around the shop!!!!!!!! Good luck with that!!!!"


@retry(wait=wait_random(min=5, max=10), stop=stop_after_attempt(5))
def expertise(text):
    result = {}
    output = client.full_analysis(
        body={"document": {"text": text}}, params={'language': language})
    output2 = client.classification(body={"document": {"text": text}}, params={
                                    'taxonomy': taxonomy, 'language': language})

    result['classification'] = [(f.label, f.hierarchy, f.frequency)
                                for f in output2.categories if f.winner == True]
    result['mainPhrases'] = [(f.value, f.score) for f in output.main_phrases]
    result['mainLemmas'] = [(f.value, f.score) for f in output.main_lemmas]
    result['mainSyncons'] = [(f.syncon, f.lemma, f.score)
                             for f in output.main_syncons]
    result['topics'] = [(f.label, f.score)
                        for f in output.topics if f.winner == True]
    result['entities'] = [(f.type_, f.lemma) for f in output.entities]
    result['sentiment.overall'] = output.sentiment.overall
    result['sentiment.negativity'] = output.sentiment.negativity
    result['sentiment.positivity'] = output.sentiment.positivity
    result['sentiment.items'] = [(f.lemma, f.sentiment)
                                 for f in output.sentiment.items]

    return result


def save_sentiments(review, sentiment):
    # print(sentiment['sentiment'])
    review.sentiment_overall = sentiment['sentiment.overall']
    review.expertai_classification = sentiment['classification']
    review.expertai_entities = sentiment['entities']
    review.expertai_mainLemmas = sentiment['mainLemmas']
    review.expertai_mainPhrases = sentiment['mainPhrases']
    review.expertai_mainSyncons = sentiment['mainSyncons']
    review.expertai_sentiment_items = sentiment['sentiment.items']
    review.expertai_topics = sentiment['topics']
    review.save()


def process_sentiments():
    cnt = 0
    reviews = Review.objects.filter(
        sentiment_overall=None).exclude(text='')[:500]
    for r in reviews:
        cnt += 1
        sentiment = expertise(r.text)
        save_sentiments(r, sentiment)
        if cnt % 50 == 0:
            time.sleep(1)
    return cnt


def process_sentiments_all():
    total = 0
    cnt = process_sentiments()
    while cnt > 0:
        total += cnt
        print('process_sentiments', total)
        cnt = process_sentiments()
    print('process_sentiments', total)
