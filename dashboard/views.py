from django.shortcuts import render
from vote.models import Category, SubCategory
from payment.models import Nominees, Payment
from register.models import Register

# Create your views here.

def admin(request):
    
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/admin.html', context)

def activity_category(request):
    
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/activity-category.html', context)

def activity_nominee(request):
    
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/activity-nominee.html', context)

def registration(request):
    
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/registration.html', context)


def registration_category(request):
    
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/registration-category.html', context)



def registration_nominee(request):
    
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/registration-nominee.html', context)

def transaction(request):
    
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/transaction.html', context)


def transaction_category(request):
    
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/transaction-category.html', context)