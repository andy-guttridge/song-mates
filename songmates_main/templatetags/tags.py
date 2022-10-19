from django import template
from songmates_main.models import CollabRequest

register = template.Library()

# The approach to using a custom template tag to pass data to the base
# HTML template was adapated from
# https://stackoverflow.com/questions/21062560/django-variable-in-base-html


@register.simple_tag
def number_of_collab_requests(request):
    """
    Find out how many collaboration requests there are for the current user and
    make available as a template tag.
    """
    num_collab_requests = CollabRequest.objects.filter(
        to_user=request.user).count()
    return num_collab_requests
