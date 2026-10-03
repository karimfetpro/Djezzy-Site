from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from catalogue.models import Categories, Offers, SubOffers, SubOfferQuota
from catalogue.forms import CategorieForm, OfferForm, SubOfferForm, QuotaForm
from comptes.models import Commercials

def catalog_view(request):
    categories = Categories.objects.prefetch_related('offers__sub_offers').all()
    return render(request, 'catalogue/catalog_view.html', {'categories': categories})

def offer_detail(request, pk):
    offer = get_object_or_404(Offers, pk=pk)
    return render(request, 'catalogue/offer_detail.html', {'offer': offer})

def _commercial_or_404(request):
    return get_object_or_404(Commercials, user=request.user)

@login_required
def catalog_manage(request):
    _commercial_or_404(request)
    categories = Categories.objects.prefetch_related('offers__sub_offers').all()
    return render(request, 'catalogue/catalog_manage.html', {'categories': categories})

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
    return render(request, 'catalogue/categorie_form.html', {'form': form})

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
    return render(request, 'catalogue/categorie_form.html', {'form': form, 'categorie': categorie})

@login_required
def categorie_delete(request, pk):
    _commercial_or_404(request)
    categorie = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, "Catégorie supprimée.")
        return redirect('catalog_manage')
    return render(request, 'catalogue/catalog_confirm_delete.html', {
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
    return render(request, 'catalogue/offer_form.html', {'form': form})

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
    return render(request, 'catalogue/offer_form.html', {'form': form, 'offer': offer})

@login_required
def offer_delete(request, pk):
    _commercial_or_404(request)
    offer = get_object_or_404(Offers, pk=pk)
    if request.method == 'POST':
        offer.delete()
        messages.success(request, "Offre supprimée.")
        return redirect('catalog_manage')
    return render(request, 'catalogue/catalog_confirm_delete.html', {
        'object_name': offer.name,
        'warning': "Toutes les sous-offres de cette offre seront également supprimées.",
    })

@login_required
def suboffer_create(request):
    _commercial_or_404(request)
    if request.method == 'POST':
        form = SubOfferForm(request.POST, request.FILES)
        if form.is_valid():
            sub_offer = form.save()
            messages.success(request, "Sous-offre ajoutée. Pensez à définir ses quotas par commune.")
            return redirect('quota_list', sub_offer_pk=sub_offer.pk)
    else:
        form = SubOfferForm()
    return render(request, 'catalogue/suboffer_form.html', {'form': form})

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
    return render(request, 'catalogue/suboffer_form.html', {'form': form, 'sub_offer': sub_offer})

@login_required
def suboffer_delete(request, pk):
    _commercial_or_404(request)
    sub_offer = get_object_or_404(SubOffers, pk=pk)
    if request.method == 'POST':
        sub_offer.delete()
        messages.success(request, "Sous-offre supprimée.")
        return redirect('catalog_manage')
    return render(request, 'catalogue/catalog_confirm_delete.html', {
        'object_name': sub_offer.name,
    })

@login_required
def quota_list(request, sub_offer_pk):
    _commercial_or_404(request)
    sub_offer = get_object_or_404(SubOffers, pk=sub_offer_pk)
    quotas = sub_offer.quotas.all()
    return render(request, 'catalogue/quota_list.html', {
        'sub_offer': sub_offer,
        'quotas': quotas,
    })

@login_required
def quota_create(request, sub_offer_pk):
    _commercial_or_404(request)
    sub_offer = get_object_or_404(SubOffers, pk=sub_offer_pk)
    if request.method == 'POST':
        form = QuotaForm(request.POST, sub_offer=sub_offer)
        if form.is_valid():
            form.save()
            messages.success(request, "Quota ajouté.")
            return redirect('quota_list', sub_offer_pk=sub_offer.pk)
    else:
        form = QuotaForm(sub_offer=sub_offer)
    return render(request, 'catalogue/quota_form.html', {'form': form, 'sub_offer': sub_offer})

@login_required
def quota_update(request, pk):
    _commercial_or_404(request)
    quota = get_object_or_404(SubOfferQuota, pk=pk)
    sub_offer = quota.sub_offer
    if request.method == 'POST':
        form = QuotaForm(request.POST, instance=quota, sub_offer=sub_offer)
        if form.is_valid():
            form.save()
            messages.success(request, "Quota modifié.")
            return redirect('quota_list', sub_offer_pk=sub_offer.pk)
    else:
        form = QuotaForm(instance=quota, sub_offer=sub_offer)
    return render(request, 'catalogue/quota_form.html', {'form': form, 'sub_offer': sub_offer, 'quota': quota})

@login_required
def quota_delete(request, pk):
    _commercial_or_404(request)
    quota = get_object_or_404(SubOfferQuota, pk=pk)
    sub_offer = quota.sub_offer
    if request.method == 'POST':
        quota.delete()
        messages.success(request, "Quota supprimé.")
    return redirect('quota_list', sub_offer_pk=sub_offer.pk)