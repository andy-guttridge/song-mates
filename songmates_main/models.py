from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from .genres import Genres


class Profile(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                             unique=True, related_name="profile")
    slug = models.SlugField(max_length=200, unique=True)
    friends = models.ManyToManyField("self", blank=True,
                                     )
    image = CloudinaryField('image', default='blank-profile-pic.png')
    biog = models.TextField(max_length=500, null=True, blank=True)
    genre1 = models.CharField(choices=Genres.choices, max_length=3, null=True,
                              blank=True)
    genre2 = models.CharField(choices=Genres.choices, max_length=3, null=True,
                              blank=True)
    genre3 = models.CharField(choices=Genres.choices, max_length=3, null=True,
                              blank=True)
    genre4 = models.CharField(choices=Genres.choices, max_length=3, null=True,
                              blank=True)
    genre5 = models.CharField(choices=Genres.choices, max_length=3, null=True,
                              blank=True)
    instru_skill1 = models.CharField(max_length=30, null=True, blank=True)
    instru_skill2 = models.CharField(max_length=30, null=True, blank=True)
    instru_skill3 = models.CharField(max_length=30, null=True, blank=True)
    instru_skill4 = models.CharField(max_length=30, null=True, blank=True)
    instru_skill5 = models.CharField(max_length=30, null=True, blank=True)
