from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        # Associate the form with Profile model and specify which fields to display
        model = Profile
        fields = ['image', 'biog', 'genre1', 'genre2', 'genre3',
                  'genre4', 'genre5', 'instru_skill1', 'instru_skill2',
                  'instru_skill3', 'instru_skill4', 'instru_skill5']
        # Specify labels for form fields
        labels = {
            'image': ('Profile Image'),
            'biog': ('Biography'),
            'genre1': ('Genre 1'),
            'genre2': ('Genre 2'),
            'genre3': ('Genre 3'),
            'genre4': ('Genre 4'),
            'genre5': ('Genre 5'),
            'instru_skill1': ('Instrument or skill 1'),
            'instru_skill2': ('Instrument or skill 2'),
            'instru_skill3': ('Instrument or skill 3'),
            'instru_skill4': ('Instrument or skill 4'),
            'instru_skill5': ('Instrument or skill 5'),
        }
