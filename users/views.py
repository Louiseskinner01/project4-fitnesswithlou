from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
from .forms import ProfileForm

from checkout.models import Order

@login_required
def profile(request):
    """ Display and update the user's profile """

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    orders = request.user.orders.all().order_by('-date')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Profile updated successfully!'
            )

    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'orders': orders,
    }

    return render(request, 'users/profile.html', context)


@login_required
def create_profile(request):

    if request.method == 'POST':

        form = ProfileForm(request.POST)

        if form.is_valid():

            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            messages.success(
                request,
                'Profile created successfully!'
            )

            return redirect('users:profile')

    else:

        form = ProfileForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'users/profile_form.html',
        context
    )


@login_required
def order_history(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )

    return render(request, 'users/order_detail.html', {'order': order})