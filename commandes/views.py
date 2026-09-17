from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from commandes.models import Order, OrderItem
from boutiques.models import Boutique
from catalogue.models import SubOffers

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
    boutiques = request.user.client_profile.boutique_set.all()

    if not boutiques.exists():
        messages.error(request, "Tu dois d'abord ajouter une boutique avant de commander.")
        return redirect('boutique_list')

    if request.method == 'POST':
        boutique_id = request.POST.get('boutique')
        quantity = int(request.POST.get('quantity', 1))
        boutique = get_object_or_404(Boutique, pk=boutique_id, client=request.user.client_profile)

        order = Order.objects.create(
            client=request.user.client_profile,
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