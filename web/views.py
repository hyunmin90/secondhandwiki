from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def landing(request):
    if request.user.is_authenticated():
        return render(request, 'main.html')
    else:
        return render(request, 'sign_up.html')
