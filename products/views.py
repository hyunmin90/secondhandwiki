from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from accounts.models import *

# Create your views here.
@login_required
@csrf_protect
def show_categories(request):
    return render(request, 'main.html', {})    
    

