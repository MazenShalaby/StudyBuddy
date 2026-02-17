from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import pycountry

# Create your models here.


class CustomUser(AbstractUser):
    
    @staticmethod
    def get_country():
        countries = list(pycountry.countries)
        country_choices = list((country.alpha_2, country.name) for country in countries)
        return country_choices
    
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], blank=True, null=False)
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{11}$')],
        blank=True,
        null=True,
    )

    country = models.CharField(max_length=2, default='US', choices=get_country())
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/avatar.svg', blank=True, null=False)
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['date_joined']
    
    def __str__(self):
        return self.email