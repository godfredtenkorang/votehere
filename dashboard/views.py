from django.shortcuts import render, get_object_or_404, redirect
from vote.models import Category, SubCategory
from payment.models import Nominees, Payment
from register.models import Register
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf, send_sms_to_new_nominee, send_mnotify_sms
from payment.forms import NomineeForm
from django.contrib import messages
from .forms import SendSmsForm, NomineeForm, CategorySMSForm
from ussd.models import PaymentTransaction

# Create your views here.

def access_award_by_code(request):
    if request.method == 'POST':
        code = request.POST.get('access_code')
        try:
            award = Category.objects.get(access_code=code)
            return redirect('activity_category', award.slug)
        except Category.DoesNotExist:
            messages.error(request, "Invalid access code. Please try again.")
            return redirect('access_award_by_code')  # or wherever your admin view is named
    
    return render(request, 'dashboard/access_code_form.html')

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


def access_transaction_by_code(request):
    if request.method == 'POST':
        code = request.POST.get('access_code')
        try:
            award = Category.objects.get(access_code=code)
            return redirect('TransactionCat', award.slug)
        except Category.DoesNotExist:
            messages.error(request, "Invalid access code. Please try again.")
            return redirect('access_transaction_by_code')  # or wherever your admin view is named
    
    return render(request, 'dashboard/access_transaction_code_form.html')

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
    
    # Get filter parameters from request GET
    invoice_no = request.GET.get('invoice_no')
    payment_type = request.GET.get('payment_type')
    nominee_code = request.GET.get('nominee_code')
    event_code = request.GET.get('event_code')
    timestamp = request.GET.get('timestamp')
    created_at = request.GET.get('created_at')
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        payments = payments.filter(category=category, status='PAID')
    
    # Apply additional filters if they exist in the request
    if invoice_no:
        payments = payments.filter(invoice_no__icontains=invoice_no)
    if payment_type:
        payments = payments.filter(payment_type=payment_type)
    if nominee_code:
        payments = payments.filter(nominee_code__icontains=nominee_code)
    if event_code:
        payments = payments.filter(event_code__icontains=event_code)
    if timestamp:
        payments = payments.filter(timestamp__date=timestamp)
    if created_at:
        payments = payments.filter(created_at__date=created_at)
        
    total_amount = payments.aggregate(Total=Sum('amount')).get('Total', 0)

    
    
    context = {
        'payments': payments,
        'category': category,
        'total_amount': total_amount,
        'title': 'USSD transactions',
        'filter_params': {  # Pass filter values back to template to maintain filter state
            'invoice_no': invoice_no,
            'payment_type': payment_type,
            'nominee_code': nominee_code,
            'event_code': event_code,
            'timestamp': timestamp,
            'created_at': created_at,
        }
    }
    return render(request, 'dashboard/ussd_transactions.html', context)

def online_transactions(request, category_id):
    category = None
    payments = Payment.objects.all()
    
    # Get filter parameters from request GET
    nominee_id = request.GET.get('nominee')
    content_id = request.GET.get('content')
    phone = request.GET.get('phone')
    ref = request.GET.get('ref')
    verified = request.GET.get('verified')
    date_created = request.GET.get('date_created')
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        payments = payments.filter(category=category, verified=True)
        
    # Apply additional filters if they exist in the request
    if nominee_id:
        payments = payments.filter(nominee_id=nominee_id)
    if content_id:
        payments = payments.filter(content_id=content_id)
    if phone:
        payments = payments.filter(phone__icontains=phone)
    if ref:
        payments = payments.filter(ref__icontains=ref)
    if verified:
        # Convert string 'true'/'false' to boolean
        verified_bool = verified.lower() == 'true'
        payments = payments.filter(verified=verified_bool)
    if date_created:
        payments = payments.filter(date_created__date=date_created)
        
    total_amount = payments.aggregate(Total=Sum('total_amount')).get('Total', 0)
        
    
    
    context = {
        'payments': payments,
        'category': category,
        'total_amount': total_amount,
        'filter_params': {  # Pass filter values back to template
            'nominee': nominee_id,
            'content': content_id,
            'phone': phone,
            'ref': ref,
            'verified': verified,
            'date_created': date_created,
        },
        'nominees': Nominees.objects.all(),  # For nominee dropdown
        'contents': SubCategory.objects.all(),  # For content dropdown
        'title': 'Online transactions'
    }
    return render(request, 'dashboard/online_transactions.html', context)


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
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminPage')
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
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminPage')
    if request.method == 'POST':
        form = SendSmsForm(request.POST)
        if form.is_valid():
            send_sms = form.save()
            send_sms_to_new_nominee(send_sms.name, send_sms.phone_number, send_sms.category)
            messages.success(request, 'Message sent successfully!')
            return redirect('send_sms')
        
    else:
        form = SendSmsForm()
    context = {
        'form': form,
        'title': 'SMS'
    }
    
    return render(request, 'dashboard/nominee/send_sms.html', context)


def send_sms_to_nominees(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminPage')
    
    if request.method == 'POST':
        form = CategorySMSForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            sms_message = form.cleaned_data['message']
            
            
            
            nominees = Nominees.objects.filter(
                category=category,
                phone_number__isnull=False
            ).exclude(phone_number='')
            
            if not nominees.exists():
                messages.warning(request, f"No nominees with phone numbers found in {category.award} category.")
                return redirect('send_category_sms')
            
            phone_numbers = [n.phone_number for n in nominees if n.phone_number]
            
            # Send SMS via MNotify
            send_mnotify_sms(phone_numbers, sms_message)
            messages.success(request, 'Message sent successfully!')
            
            
            return redirect('send_category_sms')
    else:
        form = CategorySMSForm()
        
    context = {
        'form': form,
        'title': 'Send SMS by Category'
    }
        
    return render(request, 'dashboard/nominee/send_sms_to_nominees.html', context)


def get_subcategory_votes(subcategory_id):
    try:
        subcategory = SubCategory.objects.get(id=subcategory_id)
        total_votes = Nominees.objects.filter(sub_category=subcategory).aggregate(total=Sum('total_vote'))['total'] or 0
        return subcategory, total_votes
    except SubCategory.DoesNotExist:
        return None, 0

def award_revenue_insight(request, subcategory_id):
    subcategory, total_votes = get_subcategory_votes(subcategory_id)
    context = {
        'subcategory': subcategory,
        'total_votes': total_votes
    }
    return render(request, 'dashboard/award_revenue_insight.html', context)


def get_all_categories(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminPage')
    awards = Category.objects.all()
    context = {
        'awards': awards,
        'title': 'Categories'
    }
    return render(request, 'dashboard/get_nominees/awards.html', context)

def get_nominee_by_category(request, category_slug):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminPage')
    category = None
    award = Nominees.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        award = award.filter(category=category)
        


    context = {
        'category': category,
        'award': award,
        'title': 'Nominees'
    }
    return render(request, 'dashboard/get_nominees/nominees.html', context)



def update_nominee_by_category(request, nominee_slug):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminPage')
    nominee = get_object_or_404(Nominees, slug=nominee_slug)
    
        
    if request.method == 'POST':
        form = NomineeForm(request.POST, request.FILES, instance=nominee)
        if form.is_valid():
            form.save()
            return redirect('get_all_categories')
    else:
        form = NomineeForm(instance=nominee)
        


    context = {
        'title': 'Nominees',
        'form': form
    }
    return render(request, 'dashboard/get_nominees/update.html', context)