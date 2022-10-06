from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserDeleteForm


# Create your views here.
class Home(View):
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "index.html"
            )


class UserDelete(View):
    
    #Approach to making a user account inactive adapated from
    #https://stackoverflow.com/questions/38047408/how-to-allow-user-to-delete-account-in-django-allauth
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request.user.is_active = False
        request.user.save()
        return HttpResponseRedirect(reverse_lazy('account_logout'))
