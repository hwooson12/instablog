from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)
    categories = models.ForeignKey('Category')


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