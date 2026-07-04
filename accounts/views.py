from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    """
    Handle user registration via the custom signup page.
    GET request: renders an empty UserCreationForm.
    POST request: validates the submitted form and creates
    a new user account, then redirects to the login page.
    Note: This view is largely superseded by django-allauth's
    built in registration flow which handles email verification.
    """
    if request.method == "POST":  # Fixed typo: 'mehod' -> 'method'
        # Bind the form with POST data
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user to the database
            form.save()
            # Redirect to login page after successful registration
            return redirect('login')
    else:
        # GET request — render empty registration form
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
