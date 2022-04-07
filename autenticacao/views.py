from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
# Create your views here.

def cadastro(request):
    if request.method == "GET":
        if request.user.id_althenticated:
            return redirect('/home/')
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("password")
        confirmar_senha = request.POST.get("confirm-password")
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/cadastrar/cadastro/')
        
        if len(username.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/cadastrar/cadastro/')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existente!')
            return redirect('/cadastrar/cadastro/')
        
        
        try:
            user = User.objects.create_user(username= username, password=senha)
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso')
            return redirect('/cadastrar/login/')
            
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/cadastrar/cadastro/')
        


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/home/')
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')
        usuario = auth.authenticate(username=username, password=senha)
    if not usuario:
        messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
        return redirect('/auth/logar')
    else:
        auth.login(request, usuario)
        return redirect('/home/')


def sair(request):
    auth.logout(request)
    return redirect('/cadastrar/login/')