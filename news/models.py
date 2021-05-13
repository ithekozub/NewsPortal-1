from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #read about those methods
    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    theme = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    NEWS = 'NW'
    ARTICLES = 'AR'

    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLES, 'Статья')
    )

    time = models.DateTimeField(auto_now_add=True)
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLES)
    title = models.CharField(max_length=255)
    text = models.TextField(default='Текс статьи')
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) <= 124:
            return self.text + '...'
        elif len(self.text) > 124:
            short_text = len(self.text)[0:124]
            return short_text + '...'


class Comment(models.Model):
    text = models.TextField(default='Коментарий')
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
