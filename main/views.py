from django.shortcuts import render, redirect
from .forms import NewsletterForm
from .models import NewsletterSignup
from django.contrib import messages
from .forms import JobApplicationForm


def landing_page(request):
    """
    Render the FWL landing page.
    The home page of the site featuring the hero image,
    call to action button and introduction to FWL services.
    Accessible to all users including unauthenticated visitors.
    """
    return render(request, "landing.html")


def newsletter_signup(request):
    """
    Handle newsletter signup form submissions.
    GET request: renders the empty newsletter signup form.
    POST request: validates the submitted email address,
    checks for duplicate signups to prevent the same email
    being registered twice, saves the signup to the database
    and redirects to the landing page with a success message.
    Accessible to all users including unauthenticated visitors.
    """
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if this email is already registered for the newsletter
            # to prevent duplicate entries in the database
            if NewsletterSignup.objects.filter(email=email).exists():
                messages.warning(
                    request,
                    'You are already signed up to our newsletter!'
                )
            else:
                # Save the new newsletter signup to the database
                form.save()
                messages.success(
                    request,
                    'Thank you for signing up to our newsletter!'
                )

            # Redirect back to the landing page after form submission
            return redirect('main:landing')
    else:
        # GET request — render empty newsletter signup form
        form = NewsletterForm()

    return render(request, 'main/news.html', {'form': form})


def join_us(request):
    """
    Handle job application form submissions including CV upload.
    GET request: renders the empty job application form.
    POST request: validates the submitted form including any
    uploaded CV file, saves the application to the database
    and redirects to the job success page with a confirmation message.
    If the form is invalid, errors are printed to the console
    for debugging and the form is re-rendered with error messages.
    Accessible to all users including unauthenticated visitors.
    """
    if request.method == 'POST':
        # Bind the form with POST data and any uploaded files (CV)
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the job application to the database
            form.save()
            messages.success(
                request,
                'Thank you for your application! We will be in touch soon.'
            )
            # Redirect to the success page after successful submission
            return redirect('job_success')
        else:
            # Log form errors to the console for debugging
            print(f"FORM ERRORS: {form.errors}")
    else:
        # GET request — render empty job application form
        form = JobApplicationForm()

    return render(request, 'main/joinus.html', {'form': form})
