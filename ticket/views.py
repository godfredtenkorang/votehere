from django.shortcuts import render

# Create your views here.
def ticketing(request):
    return render(request, 'ticket/ticketting.html')