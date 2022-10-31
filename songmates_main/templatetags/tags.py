from django import template
from django.db.models import Q
from songmates_main.models import CollabRequest, Message

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
            Q(from_user=request.user) | Q(to_user=request.user)
            ).count()
    return num_collab_requests


@register.simple_tag
def number_of_incoming_messages(request):
    """
    Find out how many incoming messages there are for the current user and
    make available as a template tag.
    """
    num_incoming_messages = Message.objects.filter(
            to_user=request.user).filter(to_deleted=False).count()
    return num_incoming_messages