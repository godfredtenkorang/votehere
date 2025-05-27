from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from dashboard.forms import CategorySMSForm, PaymentTransactionForm, SendSmsForm
from dashboard.utils import send_access_code_to_new_nominee, send_mnotify_sms, send_sms_to_new_nominee
from payment.models import Nominees
from ussd.models import PaymentTransaction
from vote.models import Category, SubCategory
from django.utils import timezone
from django.db.models import Sum
from .forms import NomineeForm

# Create your views here.
def dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to see more.")
        return redirect('adminHome')
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
    return render(request, 'maindashboard/dashboard.html', context)

@login_required
def add_nominee(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to add nominee.")
        return redirect('adminHome')
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
    return render(request, 'maindashboard/nominee/add_nominee.html', context)


class GetSubCategoriesView(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        if category_id:
            subcategories = SubCategory.objects.filter(category_id=category_id)
            options = '<option value="">---------</option>'
            for subcategory in subcategories:
                options += f'<option value="{subcategory.id}">{subcategory.content}</option>'
            return JsonResponse(options, safe=False)
        return JsonResponse('<option value="">---------</option>', safe=False)


def send_sms(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminHome')
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
    
    return render(request, 'maindashboard/nominee/send_sms.html', context)


def send_sms_to_nominees(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminHome')
    
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
        
    return render(request, 'maindashboard/nominee/send_sms_to_nominees.html', context)


def get_subcategory_votes(subcategory_id):
    try:
        subcategory = SubCategory.objects.get(id=subcategory_id)
        total_votes = Nominees.objects.filter(sub_category=subcategory).aggregate(total=Sum('total_vote'))['total'] or 0
        return subcategory, total_votes
    except SubCategory.DoesNotExist:
        return None, 0



def get_all_categories(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminHome')
    awards = Category.objects.all()
    context = {
        'awards': awards,
        'title': 'Categories'
    }
    return render(request, 'maindashboard/get_nominees/awards.html', context)

def get_nominee_by_category(request, category_slug):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send SMS.")
        return redirect('adminHome')
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
    return render(request, 'maindashboard/get_nominees/nominees.html', context)



def update_nominee_by_category(request, nominee_slug):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to update nominee.")
        return redirect('adminHome')
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
    return render(request, 'maindashboard/get_nominees/update.html', context)


def payment_transactions(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view transactions.")
        return redirect('adminHome')
    payments = PaymentTransaction.objects.all()
    
    payment_count = payments.count()
    total_payments = PaymentTransaction.objects.all().aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'payment_count': payment_count,
        'total_payments': total_payments,
        'payments': payments
    }
    return render(request, 'maindashboard/payment_transactions.html', context)


def payment_transactions_detail(request, invoice_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view transaction details.")
        return redirect('adminHome')
    
    payment = get_object_or_404(PaymentTransaction, invoice_no=invoice_id)
    
    
    if request.method == 'POST':
        form = PaymentTransactionForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Payment updated successfully!')
            return redirect('payment_transactions')
    else:
        form = PaymentTransactionForm(instance=payment)
        
    context = {
        'payment': payment,
        'form': form
    }
    return render(request, 'maindashboard/payment_transactions_form.html', context)

def send_access_code_to_nominee(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to send access code SMS.")
        return redirect('adminHome')
    
    if request.method == 'POST':
        
            name = request.POST.get('name')
            phone_number = request.POST.get('phone_number')
            access_code = request.POST.get('access_code')
            category = request.POST.get('category')
            
            # Send SMS via MNotify
            send_access_code_to_new_nominee(name, phone_number, access_code, category)
            messages.success(request, 'Message sent successfully!')
            
            
            return redirect('send_access_code')
 
    context = {
     
        'title': 'Send Access Code'
    }
        
    return render(request, 'maindashboard/nominee/send_access_code.html', context)
