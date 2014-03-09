from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse


def landing(request):
    if request.user.is_authenticated():
        return render(request, 'main.html')
    else:
        return HttpResponseRedirect('/login')
