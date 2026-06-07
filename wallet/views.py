from django.shortcuts import render

# Create your views here.
def top_up_guide(request):

    return render(request, "top_up_guide.html")

def top_up(request):

    return render(request, "top_up.html")

def main_wallet(request):

    return render(request, "main_wallet.html")

def wallet_login(request):

    return render(request, "wallet_login.html")

