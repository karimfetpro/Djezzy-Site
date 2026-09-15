from django.shortcuts import render , redirect
from django.contrib.auth import  login
from .forms import ClientRegisterForm

def home (request):
        return render(request, 'comptes/home.html')

    
def register(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = ClientRegisterForm()

    return render(request, 'comptes/register.html', {'form': form})
