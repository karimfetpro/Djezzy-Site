from django.shortcuts import render , redirect
from django.contrib.auth import  login
from .forms import ClientRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home (request):
        return render(request, 'comptes/home.html')

    
def register_views(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = ClientRegisterForm()
    return render(request, 'comptes/register.html', {'form': form})

def login_views(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        next_url = request.POST.get('next') or next_url
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(next_url or 'home')
    else:
        form = AuthenticationForm()

    return render(request, 'comptes/login.html', {'form': form, 'next': next_url})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
