from django.db import models
from django.conf import settings


class Profile(models.Model):
    """Модель профиля пользователя"""

    class Gender(models.TextChoices):
        """Выбор пола"""
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        UNKNOWN = 'U', 'Unknown'

    headline = models.TextField(max_length=100)  # Краткое описание деятельности
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='account/profile_photo/%Y/%m/%d',
                              blank=True)
    gender = models.CharField(max_length=1,
                              choices=Gender.choices,
                              default=Gender.UNKNOWN)

    def __str__(self):
        return f'Profile of {self.user}'
