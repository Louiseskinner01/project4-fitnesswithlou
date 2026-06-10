from django.shortcuts import render, redirect
from .forms import NewsletterForm
from .models import NewsletterSignup
from django.contrib import messages

def landing_page(request):
    return render (request, "landing.html")


def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if already signed up
            if NewsletterSignup.objects.filter(email=email).exists():
                messages.warning(request, 'You are already signed up to our newsletter!')
            else:
                form.save()
                messages.success(request, 'Thank you for signing up to our newsletter!')
            return redirect('main:landing')
    else:
        form = NewsletterForm()

    return render(request, 'main/news.html', {'form': form})