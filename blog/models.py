from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=40)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)
    categories = models.ForeignKey('Category', default=1)
    senti = models.SmallIntegerField(choices=((1, 'positive'),
                                              (0, 'neutral'),
                                              (-1, 'negative')),
                                     default=0)


    def __str__(self):
        return '{}님의 글: {}'.format(self.pk, self.title)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}의 덧글'.format(self.post)

class Tag(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Sentiword(models.Model):
    word = models.CharField(max_length=40)
    post = models.ForeignKey(Post)

