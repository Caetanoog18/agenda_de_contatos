from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato

def login(request):
    if request.method != 'POST':
        return render(request, 'contas/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'contas/login.html')

    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('index')

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'contas/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha \
            or not senha2:
        messages.error(request, 'Nenhum campo deve ficar vazio')
        return render(request, 'contas/cadastro.html')

    try:
        validate_email(email)

    except:
        messages.error(request, 'Email inválido')
        return render(request, 'contas/cadastro.html')

    if len(senha)< 8:
        messages.error(request, 'A senha precisa conter pelo menos 8 caracteres')
        return render(request, 'contas/cadastro.html')

    if senha != senha2:
        messages.error(request, 'As senhas precisam ser idênticas!')
        return render(request, 'contas/cadastro.html')

    if User.objects.filter(username = usuario).exists():
        messages.error(request, 'Nome de usuário já existente')
        return render(request, 'contas/cadastro.html')

    if User.objects.filter(email = email).exists():
        messages.error(request, 'Email já existente')
        return render(request, 'contas/cadastro.html')

    messages.success(request, 'Cadastro realizado com sucesso')

    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'contas/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar o formulário!')
        form = FormContato(request.POST)
        return render(request, 'contas/dashboard.html', {'form': form})

    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'Olá')
        form = FormContato(request.POST)
        return render(request, 'contas/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso!')
    return redirect('dashboard')



