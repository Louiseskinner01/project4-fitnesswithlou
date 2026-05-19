from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
from .forms import ProfileForm


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