from django.shortcuts import render, get_object_or_404, redirect
from vote.models import Category, SubCategory
from payment.models import Nominees, Payment
from register.models import Register
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf, send_sms_to_new_nominee
from payment.forms import NomineeForm
from django.contrib import messages
from .forms import SendSmsForm
from ussd.models import PaymentTransaction

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
        total_votes = total_votes['total']

        

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
        total_votes = total_votes['total']

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
    online_payments = Payment.objects.all()
    ussd_payments = PaymentTransaction.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        award = award.filter(category=category)
        online_payments = online_payments.filter(category=category, verified=True)
        ussd_payments = ussd_payments.filter(category=category, status='PAID')
        total_online_payments = online_payments.aggregate(Total=Sum('total_amount'))
        total_online_payments = total_online_payments['Total']
        
        
        total_ussd_payments = ussd_payments.aggregate(Total=Sum('amount'))
        total_ussd_payments = total_ussd_payments['Total']
        # total_ussd_payments = total_ussd_value.quantize(Decimal('1'))

    context = {
        'category': category,
        'award': award,
        'total_online_payments': total_online_payments,
        'total_ussd_payments': total_ussd_payments,
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
        total_amount_verified = total_amount_verified['Total']
        total_amount_not_verified = total_amount_not_verified['Total']
        total_amount = total_amount['Total']

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


def ussd_transactions(request, category_id):
    category = None
    payments = PaymentTransaction.objects.all()
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        payments = payments.filter(category=category, status='PAID')
        total_amount = payments.aggregate(Total=Sum('amount'))
        total_amount = total_amount['Total']
    
    
    context = {
        'payments': payments,
        'category': category,
        'total_amount': total_amount,
        'title': 'USSD transactions'
    }
    return render(request, 'dashboard/ussd_transactions.html', context)


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


def send_sms(request):
    if request.method == 'POST':
        form = SendSmsForm(request.POST)
        if form.is_valid():
            send_sms = form.save()
            send_sms_to_new_nominee(send_sms.name, send_sms.phone_number, send_sms.category)
            return redirect('send_sms')
        
    else:
        form = SendSmsForm()
    context = {
        'form': form,
        'title': 'SMS'
    }
    
    return render(request, 'dashboard/nominee/send_sms.html', context)


def award_revenue_insight(request):
    return render(request, 'dashboard/award_revenue_insight.html')