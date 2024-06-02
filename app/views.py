import re
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import textwrap
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import TestConfig, TestResult, Vulnerability
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import logout
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Nome de usuário ou senha inválidos.",
    }

def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        if username:
            user_exists = User.objects.filter(username=username).exists()
            return JsonResponse({'exists': user_exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
                return redirect('login')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def is_valid_password(password):
    try:
        validate_password(password)
    except ValidationError as e:
        return False, e.messages
    return True, None

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
@csrf_protect
def index(request):
    return render(request, 'index.html')

@require_http_methods(["POST"])
def run_scan(request):
    url = request.POST.get('url')
    
    try:
        test_config = TestConfig.objects.create(url=url)
        
        test_result = TestResult.objects.create(test_config=test_config, status='Em andamento')
        
        vulnerabilities = []
        
        session = requests.Session()

        
        response = session.get(f"{url}/?name=<script>alert('XSS')</script>")
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find_all('script'):
            vulnerability = Vulnerability.objects.create(
                test_result=test_result,
                tipo='XSS',
                descrição='Potencial vulnerabilidade de XSS detectada',
                impacto='Alto'
            )
            vulnerabilities.append(vulnerability)
        
        response = session.get(f"{url}/?cmd=;echo%20$USER")
        if '$USER' in response.text:
            vulnerability = Vulnerability.objects.create(
                test_result=test_result,
                tipo='Command Injection',
                descrição='Potencial vulnerabilidade de Injeção de Comandos detectada',
                impacto='Alto'
            )
            vulnerabilities.append(vulnerability)
        
    
        if re.search(r'\b(?:referer|x-forwarded-for|user-agent|host)\b', str(request.headers), re.IGNORECASE):
            vulnerability = Vulnerability.objects.create(
                test_result=test_result,
                tipo='Injeção de Header HTTP',
                descrição='Potencial vulnerabilidade de Injeção de Header HTTP detectada',
                impacto='Médio'
            )
            vulnerabilities.append(vulnerability)
        
        
        response = session.get(url)
        if 'Access-Control-Allow-Origin' not in response.headers:
            vulnerability = Vulnerability.objects.create(
                test_result=test_result,
                tipo='Configuração CORS Mal Configurada',
                descrição='A página pode estar vulnerável a ataques de origem cruzada devido à falta de configuração do CORS.',
                impacto='Médio'
            )
            vulnerabilities.append(vulnerability)

        pdf_bytes = generate_pdf(vulnerabilities)
        
      
        test_result.status = 'Concluído'
        test_result.save()
        
      
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=report.pdf'
        return response

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=400)


def generate_pdf(vulnerabilities):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    data = [["Tipo", "Descrição", "Impacto"]]
    
    max_length = {
        'Tipo': 15,
        'Descrição': 50,
        'Impacto': 15
    }
    
    for vulnerability in vulnerabilities:
        tipo_lines = textwrap.wrap(vulnerability.tipo, max_length['Tipo'])
        descricao_lines = textwrap.wrap(vulnerability.descrição, max_length['Descrição'])
        impacto_lines = textwrap.wrap(vulnerability.impacto, max_length['Impacto'])
        
        tipo_text = '\n'.join(tipo_lines)
        descricao_text = '\n'.join(descricao_lines)
        impacto_text = '\n'.join(impacto_lines)
        
        data.append([tipo_text, descricao_text, impacto_text])
    
    table = Table(data, colWidths=[100, 300, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    pdf.build(elements)
    
    buffer.seek(0)
    return buffer.getvalue()