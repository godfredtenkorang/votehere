from django.shortcuts import render, get_object_or_404
from vote.models import Category, SubCategory
from payment.models import Nominees, Payment
from register.models import Register
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def admin(request):
    awards = Category.objects.all()
    context = {
        'awards': awards,
        'title': 'adminPage'
    }
    return render(request, 'dashboard/admin.html', context)

def activity_category(request, category_slug):
    category = None
    award = SubCategory.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        award = award.filter(category=category)

    context = {
        'category': category,
        'award': award,
        'title': 'adminPage'
    }
    
    return render(request, 'dashboard/activity-category.html', context)

def activity_nominee(request, nominee_slug):
    sub_category = None
    nominees = Nominees.objects.all()
    if nominee_slug:
        sub_category = get_object_or_404(SubCategory, slug=nominee_slug)
        nominees = nominees.filter(sub_category=sub_category)
        total_votes = nominees.aggregate(total=Sum('total_vote'))

        

    context = {
        'sub_category': sub_category,
        'nominees': nominees,
        'total_votes': total_votes,
        'title': 'adminPage'
    }

    return render(request, 'dashboard/activity-nominee.html', context)

def registration(request):
    awards = Category.objects.all()
    context = {
        'awards': awards,
        'title': 'adminPage'
    }

    return render(request, 'dashboard/registration.html', context)


def registration_category(request):
    
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/registration-category.html', context)



def registration_nominee(request, register_slug):
    award = None
    registers = Register.objects.all()
    if register_slug:
        award = get_object_or_404(Category, slug=register_slug)
        registers = registers.filter(award=award)
        register_count = registers.filter(award=award).count()

    context = {
        'award': award,
        'registers': registers,
        'register_count': register_count,
        'title': 'adminPage'
    }

    return render(request, 'dashboard/registration-nominee.html', context)

def transaction(request):
    awards = Nominees.objects.all()
    context = {
        'awards': awards,
        'title': 'adminPage'
    }
    return render(request, 'dashboard/transaction.html', context)

def team(request):
   
    context = {
      
        'title': 'team'
    }
    return render(request, 'dashboard/team.html', context)



def transaction_category(request, transaction_slug):
    nominee = None
    payments = Payment.objects.all()
    if transaction_slug:
        nominee = get_object_or_404(Nominees, slug=transaction_slug)
        payments = payments.filter(nominee=nominee)
        total_amount = payments.aggregate(Total=Sum('total_amount'))

    context = {
        'nominee': nominee,
        'payments': payments,
        'total_amount': total_amount,
        'title': 'adminPage'
    }
    return render(request, 'dashboard/transaction-category.html', context)