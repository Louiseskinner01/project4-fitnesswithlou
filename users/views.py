from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
from .forms import ProfileForm
from checkout.models import Order
from subscriptions.models import UserSubscription


@login_required
def profile(request):
    """
    Display and update the authenticated user's profile.
    Retrieves or creates a UserProfile for the current user,
    fetches their order history and active subscription,
    and handles profile form submission.
    GET request: renders the profile page with the current
    profile data pre-filled in the form.
    POST request: validates and saves the updated profile
    information and displays a success message.
    Requires the user to be logged in.
    """
    # Get or create a profile for the current user
    # created is True if a new profile was just created
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    # Retrieve all orders for the current user ordered by most recent first
    orders = request.user.orders.all().order_by('-date')

    # Retrieve the user's active subscription if one exists
    # Returns None if the user has no active subscription
    active_subscription = UserSubscription.objects.filter(
        user=request.user,
        status='active'
    ).first()

    if request.method == 'POST':
        # Bind the form with POST data and the existing profile instance
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            # Save the updated profile to the database
            form.save()
            messages.success(
                request,
                'Profile updated successfully!'
            )
    else:
        # GET request — pre-fill the form with existing profile data
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'orders': orders,
        'active_subscription': active_subscription,
    }

    return render(request, 'users/profile.html', context)


@login_required
def create_profile(request):
    """
    Handle creation of a new user profile.
    GET request: renders an empty profile creation form.
    POST request: validates the submitted form, links the
    new profile to the current user and saves it to the
    database, then redirects to the profile page.
    Note: In most cases profiles are created automatically
    via get_or_create in the profile view — this view
    provides an explicit profile creation route if needed.
    Requires the user to be logged in.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            # Save the profile without committing to database yet
            # so we can attach the current user first
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            messages.success(
                request,
                'Profile created successfully!'
            )

            # Redirect to the profile page after successful creation
            return redirect('users:profile')
    else:
        # GET request — render empty profile creation form
        form = ProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'users/profile_form.html', context)


@login_required
def order_history(request, order_number):
    """
    Display the details of a specific historical order.
    Retrieves the order by its unique order number and
    verifies it belongs to the current user to prevent
    users from viewing other users' orders.
    Returns 404 if the order doesn't exist or doesn't
    belong to the current user.
    Requires the user to be logged in.
    """
    # Retrieve the order ensuring it belongs to the current user
    # Returns 404 if the order number doesn't exist or belongs
    # to a different user
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )

    return render(request, 'users/order_detail.html', {'order': order})
