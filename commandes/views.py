from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.test import client
from django.views.decorators.http import require_POST

from commandes.models import Order, OrderItem
from boutiques.models import Boutique
from catalogue.models import SubOffers, SubOfferQuota
from comptes.models import Commercials

CART_SESSION_KEY = 'cart'

@login_required
def order_list(request):
    orders = request.user.client_profile.orders.prefetch_related('items__sub_offer')
    return render(request, 'commandes/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404( Order.objects.prefetch_related('items__sub_offer'), pk=pk, client=request.user.client_profile, )
    return render(request, 'commandes/order_detail.html', {'order': order})

@login_required
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk, client=request.user.client_profile)

    if request.method == 'POST':
        if order.cancel():
            messages.success(request, "Commande annulée.")
        else:
            messages.error(request, "Cette commande ne peut plus être annulée.")
        return redirect('order_detail', pk=order.pk)

    return render(request, 'commandes/order_confirm_cancel.html', {'order': order})

def _get_cart(request):
    return request.session.setdefault(CART_SESSION_KEY, {})

@login_required
def cart_add(request, sub_offer_id):
    sub_offer = get_object_or_404(SubOffers, id=sub_offer_id)
    cart = _get_cart(request)
    key = str(sub_offer_id)
    if key in cart:
        cart[key] += 1
    else:
        cart[key] = 1
    request.session.modified = True
    messages.success(request, f"{sub_offer.name} ajoutée au panier.")
    return redirect("cart_detail")

@login_required
def cart_remove(request, sub_offer_id):
    cart = _get_cart(request)
    key = str(sub_offer_id)
    if key in cart:
        del cart[key]
    request.session.modified = True
    return redirect("cart_detail")

@login_required
def cart_detail(request):
    cart = _get_cart(request)
    items = []
    total = 0
    for key in cart:
        sub_offer = get_object_or_404(SubOffers, id=key)
        quantity = cart[key]
        subtotal = sub_offer.price * quantity
        total += subtotal
        items.append({"sub_offer": sub_offer, "quantity": quantity, "subtotal": subtotal})

    client = request.user.client_profile
    boutiques = client.boutiques.filter(statut=Boutique.Statut.ACCEPTEE)
    return render(request, "commandes/cart_detail.html", {"items": items, "total": total, "boutiques": boutiques})

@login_required
def cart_confirm(request):
    if request.method != "POST":
        return redirect("cart_detail")
    cart = _get_cart(request)
    if not cart:
        messages.error(request, "Votre panier est vide.")
        return redirect("cart_detail")

    client = request.user.client_profile
    boutique_id = request.POST.get("boutique_id")
    boutique = get_object_or_404( Boutique, id=boutique_id, client=client, statut=Boutique.Statut.ACCEPTEE )
    quota_depasse = False
    with transaction.atomic():
        order = Order.objects.create(client=client, boutique=boutique)
        for key in cart:
            sub_offer = get_object_or_404(SubOffers, id=key)
            quantity = cart[key]
            OrderItem.objects.create(order=order, sub_offer=sub_offer, quantity=quantity, unit_price=sub_offer.price)
            if sub_offer.quota_restant(boutique.commune) < quantity:
                quota_depasse = True
    if quota_depasse:
        order.status = Order.Status.CANCELLED
        order.save(update_fields=['status', 'updated_at'])
        messages.error(
            request,
            f"Commande #{order.pk} refusée automatiquement : quota dépassé pour une ou plusieurs sous-offres à {boutique.commune}."
        )
    else:
        messages.success(request, "Commande passée avec succès.")
 
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True
 
    return redirect("order_detail", pk=order.id)

@login_required
def cart_update(request, sub_offer_id, action):
    cart = _get_cart(request)
    key = str(sub_offer_id)

    if action == 'add':
        cart[key] = cart.get(key, 0) + 1
    elif action == 'remove' and key in cart:
        cart[key] -= 1
        if cart[key] == 0:
            del cart[key]

    request.session.modified = True
    return redirect("cart_detail")

@login_required
def cart_pending_list(request):
    commercial = Commercials.objects.filter(user=request.user).first()
    if not commercial:
        messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
        return redirect('home')
    orders = Order.objects.filter(status=Order.Status.PENDING).prefetch_related('items__sub_offer')
    return render(request, 'commandes/cart_pending_list.html', {'orders': orders})

@login_required
def cart_set_quantity(request, sub_offer_id):
    if request.method == 'POST':
        cart = _get_cart(request)
        key = str(sub_offer_id)
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            if key in cart:
                del cart[key]
        else:
            cart[key] = quantity

        request.session.modified = True
    return redirect("cart_detail")

@login_required
@require_POST
def accept_cart(request, pk):
    commercial = Commercials.objects.filter(user=request.user).first()
    if not commercial:
        messages.error(request, "Vous n'avez pas la permission de réaliser cette action.")
        return redirect('cart_pending_list')

    order = get_object_or_404(Order.objects.prefetch_related('items__sub_offer'), pk=pk)

    if order.status != Order.Status.PENDING:
        messages.error(request, f"Commande #{order.pk} déjà traitée.")
        return redirect('cart_pending_list')

    commune = order.boutique.commune

    for item in order.items.all():
        if item.sub_offer.quota_restant(commune) < item.quantity:
            messages.error(
                request,
                f"Quota insuffisant pour « {item.sub_offer.name} » à {commune}, commande #{order.pk} non acceptée."
            )
            return redirect('cart_pending_list')

    with transaction.atomic():
        for item in order.items.all():
            SubOfferQuota.objects.filter(sub_offer=item.sub_offer, commune=commune).update(
                quantity_sold=F('quantity_sold') + item.quantity
            )
        order.status = Order.Status.CONFIRMED
        order.save(update_fields=['status', 'updated_at'])

    messages.success(request, f"Commande #{order.pk} acceptée.")
    return redirect('cart_pending_list')

@login_required
@require_POST
def refuse_cart(request, pk):
    commercial = Commercials.objects.filter(user=request.user).first()
    if commercial:
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.Status.CANCELLED
        order.save()
        messages.success(request, f"Commande #{order.pk} refusée.")
    else:
        messages.error(request, "Vous n'avez pas la permission de réaliser cette action.")
    return redirect('cart_pending_list')