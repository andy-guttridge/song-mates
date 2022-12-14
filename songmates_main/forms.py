from django.forms import ModelForm, Form, BooleanField, MultipleChoiceField,\
    CharField, HiddenInput, FileInput, ImageField, Textarea
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
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            HTML('<div class = "text-start">'),
            Field('biog', css_class='bkgnd-color-1 txt-color-2'),
            Field('image', css_class='bkgnd-color-1 txt-color-2'),
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
                css_class='row profile-genres',
            ),
            Field('instru_skill1', css_class='bkgnd-color-1 txt-color-2'),
            Field('instru_skill2', css_class='bkgnd-color-1 txt-color-2'),
            Field('instru_skill3', css_class='bkgnd-color-1 txt-color-2'),
            Field('instru_skill4', css_class='bkgnd-color-1 txt-color-2'),
            Field('instru_skill5', css_class='bkgnd-color-1 txt-color-2'),
            HTML('</div>'),
            FormActions(
                Submit('profile-form-cancel', 'Revert',
                       css_class='btn btn-primary'),
                Submit('profile-form-submit', 'Submit',
                       css_class='btn btn-warning')
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
            'image': 'Profile Image',
            'biog': 'About me',
            'genre1': 'Genre 1',
            'genre2': 'Genre 2',
            'genre3': 'Genre 3',
            'genre4': 'Genre 4',
            'genre5': 'Genre 5',
            'instru_skill1': 'Instrument or skill 1',
            'instru_skill2': 'Instrument or skill 2',
            'instru_skill3': 'Instrument or skill 3',
            'instru_skill4': 'Instrument or skill 4',
            'instru_skill5': 'Instrument or skill 5',
        }

        # Specify help text for form fields
        help_texts = {
            'biog': 'Maximum 500 characters',
            'instru_skill1': 'Maximum 30 characters',
            'instru_skill2': 'Maximum 30 characters',
            'instru_skill3': 'Maximum 30 characters',
            'instru_skill4': 'Maximum 30 characters',
            'instru_skill5': 'Maximum 30 characters',
        }

        # Specify a custom widget for the image field
        widgets = {
            'image': FileInput
        }


class SearchForm(Form):
    """
    Define the form for searching profiles
    """
    def __init__(self, is_authenticated=False, *args, **kwargs):
        """
        Init form using crispy forms FormHelper to form layout
        """
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            HTML('<div class = "text-start">'),
            Field(
                'collabs_only',
                title='Show only my collaborators',
            ),
            Field('genres', css_class='bkgnd-color-1 txt-color-2'),
            HTML('<p class = "txt-explain d-none d-lg-block ">Hold down \
                 CTRL to select multiple items on PC or Command on Mac</p>'),
            Field('search_phrase', css_class='bkgnd-color-1 txt-color-2'),
            HTML('</div>'),
            FormActions(
                Submit('search-form-submit', 'Search',
                       css_class='btn btn-primary m-1'),
                Submit('search-form-show-all', 'Show all',
                       css_class='btn btn-warning m-1'),
            )
        )
        if not is_authenticated:
            self.fields['collabs_only'].widget = HiddenInput()
        self.fields['collabs_only'].label = 'Show only my collaborators'
        self.fields['genres'].label = 'Select genres you are interested in'
        self.fields['search_phrase'].label = 'Search profiles'

    collabs_only = BooleanField(required=False)
    genres = MultipleChoiceField(required=False, choices=Genres.choices)
    search_phrase = CharField(required=False, max_length=50)
