from django.forms import ModelForm, Form, BooleanField, MultipleChoiceField, CharField
from django.contrib.auth.models import User
from django.conf.urls.static import static
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Button, Submit, HTML
from crispy_forms.bootstrap import FormActions
from .genres import Genres


class ProfileForm(ModelForm):
    """
    Create form class based on Profile model
    """
    def __init__(self, *args, **kwargs):
        """
        Init form using crispy forms FormHelper for form layout
        """
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-6'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            Field('biog'),
            Field('image'),
            # Approach to using a HTML helper class to display an image from
            # the data base in the form from
            # https://stackoverflow.com/questions/21076248/imagefield-preview-in-crispy-forms-layout
            HTML("""<img src="{{ profile.image.url }}" class="profile-img"
                 alt="profile image">""", ),
            # Approach to using a Div helper class to display
            # form elements next to each other from
            # https://stackoverflow.com/questions/23021746/get-two-fields-inline-in-django-crispy-forms-but-not-others-horizontal
            Div(
                Div('genre1', css_class='col-md-4'),
                Div('genre2', css_class='col-md-4'),
                Div('genre3', css_class='col-md-4'),
                Div('genre4', css_class='col-md-4'),
                Div('genre5', css_class='col-md-4'),
                css_class='row'
            ),
            Field('instru_skill1'),
            Field('instru_skill2'),
            Field('instru_skill3'),
            Field('instru_skill4'),
            Field('instru_skill5'),
            FormActions(
                Submit('profile-form-cancel', 'Revert',
                       css_class='btn btn-secondary'),
                Submit('profile-form-submit', 'Submit',
                       css_class='btn btn-primary')
            )
        )

    class Meta:
        # Associate the form with Profile model and specify which fields to
        # display
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


class SearchForm(Form):
    """
    Define the form for searching profiles
    """
    def __init__(self, *args, **kwargs):
        """
        Init form using crispy forms FormHelper to form layout
        """
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            Field('collabs_only', title='Show only my collaborators'),
            Field('genres'),
            Field('instru_skills_biog'),
            FormActions(
                Submit('search-form-submit', 'Search',
                       css_class='btn btn-primary'),
            )
        )
        self.fields['collabs_only'].label = 'Show only my collaborators'
        self.fields['genres'].label = 'Select genres you are interested in'
        self.fields['instru_skills_biog'].label = 'Search biographies, instruments and skills'

    collabs_only = BooleanField(required=False)
    genres = MultipleChoiceField(required=False, choices=Genres.choices)
    instru_skills_biog = CharField(required=False, max_length=50)

