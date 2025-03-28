from django.shortcuts import render, get_object_or_404, redirect
from vote.models import Category, SubCategory
from payment.models import Nominees, Payment
from register.models import Register
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from payment.forms import NomineeForm
from django.contrib import messages

# Create your views here.

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

def transaction(request, nominee_slug):
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

    return render(request, 'dashboard/transaction.html', context)

def team(request):
   
    context = {
      
        'title': 'team'
    }
    return render(request, 'dashboard/team.html', context)

@login_required(login_url='login')
def adminHome(request):
    awards = Category.objects.all()
    award_count = Category.objects.all().count()
    category_count = SubCategory.objects.all().count()
    nominee_count = Nominees.objects.all().count()
    current_time = timezone.now()
    context = {
        'awards': awards,
        'current_time': current_time,
        'award_count': award_count,
        'category_count': category_count,
        'nominee_count': nominee_count,
        'title': 'adminHome'
    }
    return render(request, 'dashboard/adminHome.html', context)


def TransactionMain(request):
    awards = Category.objects.all()
    context = {
        'awards': awards,
        'title': 'TransactionMain'
    }
    return render(request, 'dashboard/transactionMain.html', context)


def TransactionCat(request, category_slug):
    category = None
    award = SubCategory.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        award = award.filter(category=category)

    context = {
        'category': category,
        'award': award,
        'title': 'TransactionCat'
    }

    return render(request, 'dashboard/transactionCat.html', context)



def transaction_category(request, transaction_slug):
    nominee = None
    payments = Payment.objects.all()
    if transaction_slug:
        nominee = get_object_or_404(Nominees, slug=transaction_slug)
        all_payments = payments.filter(nominee=nominee)
        verified_payments = payments.filter(nominee=nominee, verified=True)
        not_verified_payments = payments.filter(nominee=nominee, verified=False)
        total_amount_verified = verified_payments.aggregate(Total=Sum('total_amount'))
        total_amount_not_verified = not_verified_payments.aggregate(Total=Sum('total_amount'))
        total_amount = all_payments.aggregate(Total=Sum('total_amount'))

    context = {
        'nominee': nominee,
        'all_payments': all_payments,
        'verified_payments': verified_payments,
        'not_verified_payments': not_verified_payments,
        'total_amount_verified': total_amount_verified,
        'total_amount_not_verified': total_amount_not_verified,
        'total_amount': total_amount,
        'title': 'adminPage'
    }
    return render(request, 'dashboard/transaction-category.html', context)


class GeneratePdf(View):
    def get(self, request, form, *args, **kwargs):
        nominee = None
        forms = Payment.objects.all()
        if form:
            nominee = get_object_or_404(Nominees, pk=form)
            forms = forms.filter(nominee=nominee, verified=True)

        context = {
            'forms':forms,
            'nominee': nominee
        }
        pdf = render_to_pdf('dashboard/generate.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


def generate(request, pdf):
    nominee = None
    forms = Payment.objects.all()
    if pdf:
        nominee = get_object_or_404(Nominees, pk=pdf)
        forms = forms.filter(nominee=nominee)
        total_amount = forms.aggregate(Total=Sum('total_amount'))

    context = {
        'nominee': nominee,
        'forms': forms,
        'total_amount': total_amount,
        'title': 'adminPage'
    }

    return render(request, 'dashboard/generate.html', context)

@login_required
def add_nominee(request):
    if request.method == 'POST':
        form = NomineeForm(request.POST, request.FILES)
        if form.is_valid():
            nominee = form.save(commit=False)
            nominee.save()
            messages.success(request, f'Nominee {nominee.name} added successfully.')
            return redirect('add_nominee')
    else:
        form = NomineeForm(request.FILES)
    context = {
        'form': form,
        'title': 'Add Nominee'
    }
    return render(request, 'dashboard/nominee/add_nominee.html', context)