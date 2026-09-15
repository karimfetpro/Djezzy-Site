from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect

from boutiques.models import Boutique
from boutiques.forms import BoutiqueForm

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

    return render(request, 'boutiques/boutique.html', {'form': form})

@login_required
def boutique_list(request):
    boutiques = request.user.client_profile.boutique_set.all()
    return render(request, 'boutiques/boutique_list.html', {'boutiques': boutiques})

@login_required
def boutique_delete(request):
    if request.method == 'POST':
        boutique_id = request.POST.get('boutique_id')
        try:
            boutique = request.user.client_profile.boutique_set.get(id=boutique_id)
            boutique.delete()
            messages.success(request, "Boutique supprimée avec succès.")
        except Boutique.DoesNotExist:
            messages.error(request, "Boutique introuvable.")
    return redirect('boutique_list')