from django.db import models


class Search(models.Model):
    title = models.CharField(max_length=50)
    search_terms = models.JSONField(default=list)

    def __str__(self):
        return f'ID:{self.id}, TITLE:{self.title}, SEARCH_TERMS:{self.search_terms}'


class Post(models.Model):
    reddit_id = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField()
    title = models.CharField(max_length=300)
    url = models.TextField(blank=False, null=False)
    img_url = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    searches = models.ManyToManyField(Search, related_name='posts', blank=True)

    def __str__(self):
        return f'ID:{self.id}, REDDIT_ID:{self.reddit_id}, TITLE:{self.title}'
