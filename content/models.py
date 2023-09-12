from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from pytils.translit import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Content.Status.PUBLISHED)


class Content(models.Model):
    """Модель создания поста"""
    tags = TaggableManager()  # Теги

    objects = models.Manager()
    published = PublishedManager()

    class Status(models.TextChoices):
        """Состояние публикации (черновик или опубликован)"""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_content')
    preview = models.ImageField(upload_to='content/preview/')
    description = models.TextField()
    create_post = models.DateTimeField(auto_now_add=True)
    update_post = models.DateTimeField(auto_now=True)
    publish_post = models.DateTimeField(default=timezone.now())
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        ordering = ['-publish_post']
        indexes = [
            models.Index(fields=['-publish_post']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Создается slug"""
        if not self.slug:  # Slug определяется по названию поля title
            self.slug = slugify(self.title)  # Используется pytils.translit для транслита с рус на анг язык
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('content:show_post', args=[self.slug,
                                                  self.author.id,
                                                  self.pk])


def user_directory_path(instance, filename):
    """
    Формирование пути где
    сохраняется контент
    """
    return f'content/media_data/post_id_{instance.content.id}/{filename}'


class UploadFile(models.Model):
    """Загрузка файлов к посту"""
    file = models.FileField(upload_to=user_directory_path)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content}'
