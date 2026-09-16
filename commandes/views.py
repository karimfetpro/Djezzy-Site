from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from commandes.models import Order

@login_required
def order_list(request):
    orders = request.user.client_profile.orders.prefetch_related('items__sub_offer')
    return render(request, 'client/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__sub_offer'),
        pk=pk,
        client=request.user.client_profile,
    )
    return render(request, 'client/order_detail.html', {'order': order})

@login_required
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk, client=request.user.client_profile)

    if request.method == 'POST':
        if order.cancel():
            messages.success(request, "Commande annulée.")
        else:
            messages.error(request, "Cette commande ne peut plus être annulée.")
        return redirect('order_detail', pk=order.pk)

    return render(request, 'client/order_confirm_cancel.html', {'order': order})
