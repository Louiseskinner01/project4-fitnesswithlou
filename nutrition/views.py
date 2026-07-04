from django.shortcuts import render


def nutritional_advice(request):
    """
    Display the nutritional advice page.
    Renders a static informational page providing nutritional
    guidance and advice to FWL users.
    Accessible to all users including unauthenticated visitors.
    No database queries are required as the content is
    hardcoded in the template.
    """
    return render(request, "nutrition/nutritional_advice.html")
