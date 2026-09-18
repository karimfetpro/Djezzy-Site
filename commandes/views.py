from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from commandes.models import Order, OrderItem
from boutiques.models import Boutique
from catalogue.models import SubOffers


CART_SESSION_KEY = 'cart'


@login_required
def order_list(request):
    orders = request.user.client_profile.orders.prefetch_related('items__sub_offer')
    return render(request, 'commandes/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__sub_offer'),
        pk=pk,
        client=request.user.client_profile,
    )
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


@login_required
def order_create(request, sub_offer_pk):
    sub_offer = get_object_or_404(SubOffers, pk=sub_offer_pk)

    client = request.user.client_profile
    boutiques = client.boutique_set.all()

    if not boutiques.exists():
        messages.error(request, "Tu dois d'abord ajouter une boutique avant de commander.")
        return redirect('boutique_list')

    if request.method == 'POST':
        boutique_id = request.POST.get('boutique')
        quantity = int(request.POST.get('quantity', 1))
        boutique = get_object_or_404(Boutique, pk=boutique_id, client=client)

        order = Order.objects.create(
            client=client,
            boutique=boutique,
        )
        OrderItem.objects.create(
            order=order,
            sub_offer=sub_offer,
            quantity=quantity,
        )
        messages.success(request, "Commande créée avec succès.")
        return redirect('order_detail', pk=order.pk)

    return render(request, 'commandes/order_create.html', {
        'sub_offer': sub_offer,
        'boutiques': boutiques,
    })


def try_confirm_order(order):
    if order.status != Order.Status.PENDING:
        return order.status == Order.Status.CONFIRMED

    items = order.items.all()

    if all(item.sub_offer.quota_restant() >= item.quantity for item in items):
        for item in items:
            item.sub_offer.commandes_effectuees += item.quantity
            item.sub_offer.save()
        order.status = Order.Status.CONFIRMED
        order.save()
        return True
    return False


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
    boutiques = client.boutique_set.all()
    return render(
        request, "commandes/cart_detail.html",
        {"items": items, "total": total, "boutiques": boutiques}
    )


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
    boutique = get_object_or_404(Boutique, id=boutique_id, client=client)

    order = Order.objects.create(
        client=client,
        boutique=boutique,
    )

    for key in cart:
        sub_offer = get_object_or_404(SubOffers, id=key)
        OrderItem.objects.create(order=order, sub_offer=sub_offer, quantity=cart[key], unit_price=sub_offer.price)

    confirmed = try_confirm_order(order)

    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True

    if confirmed:
        messages.success(request, "Votre commande a été confirmée.")
    else:
        messages.warning(request, "Commande enregistrée, mais le stock est insuffisant.")
    return redirect("order_detail", pk=order.id)