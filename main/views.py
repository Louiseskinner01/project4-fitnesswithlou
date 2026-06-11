from django.shortcuts import render, redirect
from .forms import NewsletterForm
from .models import NewsletterSignup
from django.contrib import messages

def join_us(request):
    print(f" JOIN US VIEW HIT - Method: {request.method}")

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

from .forms import JobApplicationForm

def join_us(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your application! We will be in touch soon.')
            return redirect('job_success')
        else:
            print(f" FORM ERRORS: {form.errors}") 
    else:
        form = JobApplicationForm()

    return render(request, 'main/joinus.html', {'form': form})