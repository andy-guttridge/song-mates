from django.db import models
from django.utils.translation import gettext_lazy as _


class Genres(models.TextChoices):
    '''
    Defines genres for use in user profile database model
    '''
    POP = 'POP', _('Pop')
    ROCK = 'ROC', _('Rock')
    HIPHOP = 'HIP', _('Hip Hop')
    FUSION = 'FUS', _('Fusion')
    CLASSICAL = 'CLA', _('Classical')
