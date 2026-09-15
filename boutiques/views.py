from django.core.checks import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import BoutiqueForm

@login_required
def boutique_create(request):
    if request.method == 'POST':
        form = BoutiqueForm(request.POST)
        if form.is_valid():
            boutique = form.save(commit=False)
            boutique.client = request.user.client_profile
            boutique.save()
            messages.success(request, "Boutique ajoutée avec succès.")
            return redirect('boutique_list')
    else:
        form = BoutiqueForm()

    return render(request, 'boutiques/boutique_form.html', {'form': form})