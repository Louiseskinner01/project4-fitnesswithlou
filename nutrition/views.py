from django.shortcuts import render

# Create your views here.
def nutritional_advice(request):
    return render(request, "nutrition/nutritional_advice.html")