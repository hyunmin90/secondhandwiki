from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse



def landing(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/main') 
    else:
        return render(request, 'landing.html')

def test_page(request):
    return render(request, 'test_page.html', {})

