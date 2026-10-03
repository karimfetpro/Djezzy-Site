from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from boutiques.models import Boutique
from boutiques.forms import BoutiqueForm
from comptes.models import Commercials

@login_required
def boutique_create(request):
    if request.method == 'POST':
        form = BoutiqueForm(request.POST)
        if form.is_valid():
            boutique = form.save(commit=False)
            boutique.client = request.user.client_profile
            boutique.statut = 'en_attente'
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
def boutique_pending_list(request):
    commercial = Commercials.objects.filter(user=request.user).first()
    if not commercial:
        messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('home')
    boutiques = Boutique.objects.filter(statut='en_attente')
    return render(request, 'boutiques/boutique_pending_list.html', {'boutiques': boutiques})

@login_required
def accept_boutique(request, pk):
    commercial = Commercials.objects.filter(user=request.user).first()
    if commercial:
        boutique = get_object_or_404(Boutique, pk=pk)
        boutique.statut = 'acceptee'
        boutique.save()
        messages.success(request, f"Boutique « {boutique.name} » acceptée.")
    else:
        messages.error(request, "Vous n'avez pas la permission de réaliser cette action.")
    return redirect('boutique_pending_list')

@login_required
def refuse_boutique(request, pk):
    commercial = Commercials.objects.filter(user=request.user).first()
    if commercial:
        boutique = get_object_or_404(Boutique, pk=pk)
        boutique.statut = 'refusee'
        boutique.save()
        messages.success(request, f"Boutique « {boutique.name} » refusée.")
    else:
        messages.error(request, "Vous n'avez pas la permission de réaliser cette action.")
    return redirect('boutique_pending_list')