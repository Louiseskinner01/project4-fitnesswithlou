from django.shortcuts import render


def handler404(request, exception):
    """
    Custom 404 error handler.
    Renders a styled FWL 404 page when a user visits a URL
    that doesn't exist or a resource cannot be found.
    The exception parameter is required by Django's 404 handler
    but is not used directly in this view.
    Note: This template is standalone and does not extend base.html
    as the cart context processor cannot run on unmatched URLs.
    Registered in fwl/urls.py as handler404.
    """
    return render(request, '404.html', status=404)


def handler500(request):
    """
    Custom 500 error handler.
    Renders a styled FWL 500 page when an unexpected server
    error occurs. Extends base.html unlike the 404 template
    as the request context is still available at this point.
    Registered in fwl/urls.py as handler500.
    """
    return render(request, '500.html', status=500)
