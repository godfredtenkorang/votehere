from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm



def login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                
                return redirect("access_award_by_code")
        
    context = {
        'form': form
    }
    
    return render(request, 'user/login.html', context)


def logout(request):
    auth.logout(request)
    
    return redirect('login')