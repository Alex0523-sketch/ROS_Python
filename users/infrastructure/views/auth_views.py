from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('username')   # el input del form se llama 'username'
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('/')
        return render(request, 'auth/login.html', {'form_errors': True})
    return render(request, 'auth/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/login/')
