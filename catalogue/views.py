from django.shortcuts import render, redirect, get_object_or_404
from catalogue.forms import CategorieForm, OfferForm, SubOfferForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from catalogue.models import Categories, Offers, SubOffers
from catalogue.forms import CategorieForm, OfferForm, SubOfferForm
from comptes.models import Commercials


def _commercial_or_404(request):
    return get_object_or_404(Commercials, user=request.user)

@login_required
def catalog_manage(request):
    _commercial_or_404(request)
    categories = Categories.objects.prefetch_related('offers__sub_offers').all()
    return render(request, 'commercial/catalog_manage.html', {'categories': categories})

@login_required
def categorie_create(request):
    _commercial_or_404(request)
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie ajoutée.")
            return redirect('catalog_manage')
    else:
        form = CategorieForm()
    return render(request, 'commercial/categorie_form.html', {'form': form})

@login_required
def categorie_update(request, pk):
    _commercial_or_404(request)
    categorie = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie modifiée.")
            return redirect('catalog_manage')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'commercial/categorie_form.html', {'form': form, 'categorie': categorie})

@login_required
def categorie_delete(request, pk):
    _commercial_or_404(request)
    categorie = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, "Catégorie supprimée.")
        return redirect('catalog_manage')
    return render(request, 'commercial/catalog_confirm_delete.html', {
        'object_name': categorie.type,
        'warning': "Toutes les offres et sous-offres de cette catégorie seront également supprimées.",
    })

@login_required
def offer_create(request):
    _commercial_or_404(request)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Offre ajoutée.")
            return redirect('catalog_manage')
    else:
        form = OfferForm()
    return render(request, 'commercial/offer_form.html', {'form': form})

@login_required
def offer_update(request, pk):
    _commercial_or_404(request)
    offer = get_object_or_404(Offers, pk=pk)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, "Offre modifiée.")
            return redirect('catalog_manage')
    else:
        form = OfferForm(instance=offer)
    return render(request, 'commercial/offer_form.html', {'form': form, 'offer': offer})

@login_required
def offer_delete(request, pk):
    _commercial_or_404(request)
    offer = get_object_or_404(Offers, pk=pk)
    if request.method == 'POST':
        offer.delete()
        messages.success(request, "Offre supprimée.")
        return redirect('catalog_manage')
    return render(request, 'commercial/catalog_confirm_delete.html', {
        'object_name': offer.name,
        'warning': "Toutes les sous-offres de cette offre seront également supprimées.",
    })

@login_required
def suboffer_create(request):
    _commercial_or_404(request)
    if request.method == 'POST':
        form = SubOfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sous-offre ajoutée.")
            return redirect('catalog_manage')
    else:
        form = SubOfferForm()
    return render(request, 'commercial/suboffer_form.html', {'form': form})

@login_required
def suboffer_update(request, pk):
    _commercial_or_404(request)
    sub_offer = get_object_or_404(SubOffers, pk=pk)
    if request.method == 'POST':
        form = SubOfferForm(request.POST, request.FILES, instance=sub_offer)
        if form.is_valid():
            form.save()
            messages.success(request, "Sous-offre modifiée.")
            return redirect('catalog_manage')
    else:
        form = SubOfferForm(instance=sub_offer)
    return render(request, 'commercial/suboffer_form.html', {'form': form, 'sub_offer': sub_offer})

@login_required
def suboffer_delete(request, pk):
    _commercial_or_404(request)
    sub_offer = get_object_or_404(SubOffers, pk=pk)
    if request.method == 'POST':
        sub_offer.delete()
        messages.success(request, "Sous-offre supprimée.")
        return redirect('catalog_manage')
    return render(request, 'commercial/catalog_confirm_delete.html', {
        'object_name': sub_offer.name,
    })
