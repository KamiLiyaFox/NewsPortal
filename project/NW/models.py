from django.core.validators import MinValueValidator
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

# Категория, к которой будет привязываться новость
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # названия категорий тоже не должны повторяться

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'



class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.title)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return '{} . . . {}'.format(self.text[0:123], str(self.rating))



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

# Новости для нашей страницы
class News(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True, # заголовки новостей не должны повторяться
    )
    description = models.TextField(db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news', # все новости в категории будут доступны через поле news
    )


    def __str__(self):
        return f'{self.name.title()}: {self.description[:128]}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


# # Категория, к которой будет привязываться новость
# class Category(models.Model):
#     # названия категорий тоже не должны повторяться
#     name = models.CharField(max_length=100, unique=True)
#
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categorys'
