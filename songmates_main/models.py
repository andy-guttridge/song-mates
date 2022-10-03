from django.db import models
from django.contrib.auth.models import User
from .genres import Genres


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="profile")
    slug = models.SlugField(max_length=200, unique=True)
    friends = models.ManyToManyField("self", null=True, blank=True,
                                     default=None)
    biog = models.TextField(max_length=500, null=True, blank=True)
    genre1 = models.CharField(choices=Genres.choices, max_length=3, null=True,
                              blank=True)
    instru_skill1 = models.CharField(max_length=30, null=True, blank=True)
