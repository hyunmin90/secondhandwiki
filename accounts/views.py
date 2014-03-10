from django.shortcuts import render

def login(request):
    return render(request, 'login.html', {})

def sign_up(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'sign_up.html', {})
