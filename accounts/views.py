from django.shortcuts import render

def login(request):
    render(request, 'login.html', {})
