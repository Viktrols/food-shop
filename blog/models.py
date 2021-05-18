from django.db import models
from django.db.models.fields.files import ImageField


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:20]


class Whyme(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    photo =  models.ImageField(upload_to='blog/', blank=True, null=True)
