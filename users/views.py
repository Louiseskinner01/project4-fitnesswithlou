from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import ProfileForm


@login_required
def display_profile(request):
        # All bookings for the logged-in user
    profile = UserProfile.objects.get_or_create(user=request.user)


    # Context dictionary to send to the template
    context = {
        'profile': profile,
    }

    # Render the template with context (load the HTML template)
    return render(request, 'users/profile.html', context)



# Create your views here.
@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user= request.user
            profile.save()

            messages.success(request, "Your user profile has successfully been created!")

            return redirect('home')

    else:
        form = ProfileForm()

    context = {
        'form' : form,
            }

    return render(request, 'users/profile_form.html', context)

   