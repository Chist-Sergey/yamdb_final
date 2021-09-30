from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from users.models import User

from .validators import year_validator


class CategoryAbstract(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(CategoryAbstract):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryAbstract):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 on_delete=models.PROTECT,
                                 related_name='titles')
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', blank=True, null=True)
    year = models.PositiveSmallIntegerField(null=True,
                                            blank=True,
                                            validators=[year_validator],
                                            verbose_name='Год')
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')

    class Meta:
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименование'

    def __str__(self):
        return f'{self.name} - {self.category.name}'


class Review(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)])

    pub_date = models.DateTimeField("Дата добавления",
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )]


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()

    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
