from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import User
from .encriptacion import cryptPassword, validatePassword 
from django.http import HttpResponse 
from django.contrib.auth import logout

def login_view(request):
    form = LoginForm()  
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            
            try:
                user = User.objects.get(email=email)
                if validatePassword(password, user.password):
                   request.session['user_id'] = user.id
                   request.session['username'] = user.email
                   request.session.set_expiry(3600)
                   return redirect('dashboard')
                else:
                    error_message = "Contraseña incorrecta."
                    return render(request, 'error.html', {'error': error_message})  # Pasar el error aquí
            except User.DoesNotExist:
                error_message = "Usuario no encontrado."
                return render(request, 'error.html', {'error': error_message})  # Pasar el error aquí  
    return render(request, "login.html", {'form': form})

def register_view(request):
    form = RegisterForm() 
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data.get("role", "user")

            encrypted_password = cryptPassword(password)
            User.objects.create(email=email, password=encrypted_password, role=role)
            return redirect('login') 

    return render(request, "register.html", {'form': form}) 


def dashboard_view(request):
    #if 'user_id' in request.session:
    user_id = request.user_id
    usuario = request.usuario

    return HttpResponse(f'Bienvenido {usuario} su ID es {user_id}')

    #if request.user.is_authenticated:
     #   return render(request, 'dashboard.html')
    #else:
     #   return redirect('login')  

def error_view(request):
    error_message = "Ocurrió un error al intentar iniciar sesión."
    return render(request, 'error.html', {'error': error_message})


def logout_view(request):
    logout(request)
    return redirect('login')