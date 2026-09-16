from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
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
def boutique_update(request, pk):
    boutique = get_object_or_404(Boutique, pk=pk, client=request.user.client_profile)
    if request.method == 'POST':
        form = BoutiqueForm(request.POST, instance=boutique)
        if form.is_valid():
            form.save()
            messages.success(request, "Boutique modifiée avec succès.")
            return redirect('boutique_list')
    else:
        form = BoutiqueForm(instance=boutique)

    return render(request, 'boutiques/boutique.html', {'form': form, 'boutique': boutique})

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

@login_required
def accept_boutique(request , pk):
    if request.user.role == 'commercial':
        boutique = get_object_or_404(Boutique, pk=pk)
        boutique.statut = 'Acceptée'
        boutique.save()
    else:
        messages.error(request, "Vous n'avez pas la permission de réaliser cette action.")
    return redirect('boutique_list')

@login_required
def refuse_boutique(request , pk):
    if request.user.role == 'commercial':
        boutique = get_object_or_404(Boutique, pk=pk)
        boutique.statut = 'Refusée'
        boutique.save()
    else:
        messages.error(request, "Vous n'avez pas la permission de réaliser cette action.")
    return redirect('boutique_list')