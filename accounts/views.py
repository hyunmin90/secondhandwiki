from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout


def login(request):
    return render(request, 'login.html', {})

@login_required
def logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_protect
def sign_up(request):
    if request.method == 'POST':
        email_exists = User.objects.filter(email=request.POST['email'].strip()).count()
        if not email_exists:
            try:
                new_user = User.objects.create_user(
                    username = request.POST['email'].strip(),
                    email = request.POST['email'].strip(),
                    password = request.POST['password']
                )
                new_user.first_name = request.POST['first_name'].strip()
                new_user.save()

                new_user.is_active = True
                new_user.save() 

                new_profile = Profile(user=new_user)
                new_profile.save()
            except:
                # should not get here
                return HttpResponseRedirect('/')

            username = request.POST['email'].strip()
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/main')
            else:
                # should not get here
                return HttpResponseRedirect('/')

        else:
            #email exists
            return render(request,'sign_up.html', {'email_exists':True})
    
    else:
        return render(request, 'login.html', {})
