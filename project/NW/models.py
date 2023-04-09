from django.db import models


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

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'




# Категория, к которой будет привязываться новость
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'
