from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from .genres import Genres


class Profile(models.Model):
    """
    Model for user profiles
    """
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                             unique=True, related_name="profile")
    slug = models.SlugField(max_length=200, unique=True)
    friends = models.ManyToManyField("self", blank=True,
                                     )
    image = CloudinaryField('image', default='placeholder')
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


class CollabRequest(models.Model):
    """
    Model for collaboration requests
    """
    from_user = models.ForeignKey(User, null=False, on_delete=models.CASCADE,
                                  unique=False, related_name="from_user")
    to_user = models.ForeignKey(User, null=False, on_delete=models.CASCADE,
                                unique=False, related_name="to_user")
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200, blank=True, null=True)

