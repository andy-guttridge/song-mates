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
    profile_complete = models.BooleanField(default=False)
    friends = models.ManyToManyField("self", blank=True,
                                     )
    image = CloudinaryField('image', default='placeholder')
    biog = models.TextField(
                            max_length=500, null=True, blank=True
                            )
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

    def save(self, *args, **kwargs):
        """
        Overrides the save method and sets profile_complete value
        depending on if user has entered at least some profile data
        """
        # Technique for overriding save method to set fields conditionally
        # on values of other fields adapted from
        # https://stackoverflow.com/questions/22157437/model-field-based-on-other-fields
        if all(o is None or o == "" for o in [self.genre1,
                                              self.genre2,
                                              self.genre3,
                                              self.genre4,
                                              self.genre5,
                                              self.instru_skill1,
                                              self.instru_skill2,
                                              self.instru_skill3,
                                              self.instru_skill4,
                                              self.instru_skill5,
                                              self.biog]):
            self.profile_complete = False
        else: 
            self.profile_complete = True
        super(Profile, self).save(*args, **kwargs)


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

