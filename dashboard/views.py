from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from vote.models import Category, SubCategory
from payment.models import Nominees, Payment
from register.models import Register
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf, send_sms_to_new_nominee, send_mnotify_sms, send_access_code_to_new_nominee
from payment.forms import NomineeForm
from django.contrib import messages
from .forms import SendSmsForm, NomineeForm, CategorySMSForm, PaymentTransactionForm, AccessCodeSMSForm
from ussd.models import PaymentTransaction

from ticket.models import Event, TicketPayment

from django.http import JsonResponse
from django.views import View

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

# @login_required
# def add_nominee(request):
#     if not request.user.is_staff:
#         messages.error(request, "You don't have permission to add nominee.")
#         return redirect('adminHome')
#     if request.method == 'POST':
#         form = NomineeForm(request.POST, request.FILES)
#         if form.is_valid():
#             nominee = form.save(commit=False)
#             nominee.save()
#             messages.success(request, f'Nominee {nominee.name} added successfully.')
#             return redirect('add_nominee')
#     else:
#         form = NomineeForm(request.FILES)
#     context = {
#         'form': form,
#         'title': 'Add Nominee'
#     }
#     return render(request, 'dashboard/nominee/add_nominee.html', context)




# class GetSubCategoriesView(View):
#     def get(self, request, *args, **kwargs):
#         category_id = request.GET.get('category_id')
#         if category_id:
#             subcategories = SubCategory.objects.filter(category_id=category_id)
#             options = '<option value="">---------</option>'
#             for subcategory in subcategories:
#                 options += f'<option value="{subcategory.id}">{subcategory.content}</option>'
#             return JsonResponse(options, safe=False)
#         return JsonResponse('<option value="">---------</option>', safe=False)


# def send_sms(request):
#     if not request.user.is_staff:
#         messages.error(request, "You don't have permission to send SMS.")
#         return redirect('adminHome')
#     if request.method == 'POST':
#         form = SendSmsForm(request.POST)
#         if form.is_valid():
#             send_sms = form.save()
#             send_sms_to_new_nominee(send_sms.name, send_sms.phone_number, send_sms.category)
#             messages.success(request, 'Message sent successfully!')
#             return redirect('send_sms')
        
#     else:
#         form = SendSmsForm()
#     context = {
#         'form': form,
#         'title': 'SMS'
#     }
    
#     return render(request, 'dashboard/nominee/send_sms.html', context)


# def send_sms_to_nominees(request):
#     if not request.user.is_staff:
#         messages.error(request, "You don't have permission to send SMS.")
#         return redirect('adminHome')
    
#     if request.method == 'POST':
#         form = CategorySMSForm(request.POST)
#         if form.is_valid():
#             category = form.cleaned_data['category']
#             sms_message = form.cleaned_data['message']
            
            
            
#             nominees = Nominees.objects.filter(
#                 category=category,
#                 phone_number__isnull=False
#             ).exclude(phone_number='')
            
#             if not nominees.exists():
#                 messages.warning(request, f"No nominees with phone numbers found in {category.award} category.")
#                 return redirect('send_category_sms')
            
#             phone_numbers = [n.phone_number for n in nominees if n.phone_number]
            
#             # Send SMS via MNotify
#             send_mnotify_sms(phone_numbers, sms_message)
#             messages.success(request, 'Message sent successfully!')
            
            
#             return redirect('send_category_sms')
#     else:
#         form = CategorySMSForm()
        
#     context = {
#         'form': form,
#         'title': 'Send SMS by Category'
#     }
        
#     return render(request, 'dashboard/nominee/send_sms_to_nominees.html', context)


# def get_subcategory_votes(subcategory_id):
#     try:
#         subcategory = SubCategory.objects.get(id=subcategory_id)
#         total_votes = Nominees.objects.filter(sub_category=subcategory).aggregate(total=Sum('total_vote'))['total'] or 0
#         return subcategory, total_votes
#     except SubCategory.DoesNotExist:
#         return None, 0

# def award_revenue_insight(request, subcategory_id):
#     subcategory, total_votes = get_subcategory_votes(subcategory_id)
#     context = {
#         'subcategory': subcategory,
#         'total_votes': total_votes
#     }
#     return render(request, 'dashboard/award_revenue_insight.html', context)


# def get_all_categories(request):
#     if not request.user.is_staff:
#         messages.error(request, "You don't have permission to send SMS.")
#         return redirect('adminHome')
#     awards = Category.objects.all()
#     context = {
#         'awards': awards,
#         'title': 'Categories'
#     }
#     return render(request, 'dashboard/get_nominees/awards.html', context)

# def get_nominee_by_category(request, category_slug):
#     if not request.user.is_staff:
#         messages.error(request, "You don't have permission to send SMS.")
#         return redirect('adminHome')
#     category = None
#     award = Nominees.objects.all()
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         award = award.filter(category=category)
        


#     context = {
#         'category': category,
#         'award': award,
#         'title': 'Nominees'
#     }
#     return render(request, 'dashboard/get_nominees/nominees.html', context)



# def update_nominee_by_category(request, nominee_slug):
#     if not request.user.is_staff:
#         messages.error(request, "You don't have permission to update nominee.")
#         return redirect('adminHome')
#     nominee = get_object_or_404(Nominees, slug=nominee_slug)
    
        
#     if request.method == 'POST':
#         form = NomineeForm(request.POST, request.FILES, instance=nominee)
#         if form.is_valid():
#             form.save()
#             return redirect('get_all_categories')
#     else:
#         form = NomineeForm(instance=nominee)
        


#     context = {
#         'title': 'Nominees',
#         'form': form
#     }
#     return render(request, 'dashboard/get_nominees/update.html', context)


# def payment_transactions(request):
#     if not request.user.is_staff:
#         messages.error(request, "You don't have permission to view transactions.")
#         return redirect('adminHome')
#     payments = PaymentTransaction.objects.all()
    
#     payment_count = payments.count()
#     total_payments = PaymentTransaction.objects.all().aggregate(total=Sum('amount'))['total'] or 0
    
#     context = {
#         'payment_count': payment_count,
#         'total_payments': total_payments,
#         'payments': payments
#     }
#     return render(request, 'dashboard/payment_transactions.html', context)


# def payment_transactions_detail(request, invoice_id):
#     if not request.user.is_staff:
#         messages.error(request, "You don't have permission to view transaction details.")
#         return redirect('adminHome')
    
#     payment = get_object_or_404(PaymentTransaction, invoice_no=invoice_id)
    
    
#     if request.method == 'POST':
#         form = PaymentTransactionForm(request.POST, instance=payment)
#         if form.is_valid():
#             form.save()
            
#             messages.success(request, 'Payment updated successfully!')
#             return redirect('payment_transactions')
#     else:
#         form = PaymentTransactionForm(instance=payment)
        
#     context = {
#         'payment': payment,
#         'form': form
#     }
#     return render(request, 'dashboard/payment_transactions_form.html', context)

# def send_access_code_to_nominee(request):
#     if not request.user.is_staff:
#         messages.error(request, "You don't have permission to send access code SMS.")
#         return redirect('adminHome')
    
#     if request.method == 'POST':
        
#             name = request.POST.get('name')
#             phone_number = request.POST.get('phone_number')
#             access_code = request.POST.get('access_code')
#             category = request.POST.get('category')
            
#             # Send SMS via MNotify
#             send_access_code_to_new_nominee(name, phone_number, access_code, category)
#             messages.success(request, 'Message sent successfully!')
            
            
#             return redirect('send_access_code')
 
#     context = {
     
#         'title': 'Send Access Code'
#     }
        
#     return render(request, 'dashboard/nominee/send_access_code.html', context)


def accessTicket(request):
    if request.method == 'POST':
        code = request.POST.get('access_code')
        try:
            event = Event.objects.get(access_code=code)
            return redirect('ticketActivity', event.slug)
        except Event.DoesNotExist:
            messages.error(request, "Invalid access code. Please try again.")
            return redirect('accessTicket')  # or wherever your admin view is named
        
    return render(request, 'dashboard/tickiting/accessTicket.html')

def ticketActivity(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    tickets_sold = event.total_tickets - event.available_tickets
    
    ticket_types_data = []
    for ticket_type in event.ticket_types.all():
        ticket_types_data.append({
            'name': ticket_type.name,
            'total': ticket_type.total_tickets,
            'sold': ticket_type.total_tickets - ticket_type.available_tickets,
            'available': ticket_type.available_tickets
        })
        
     # Calculate total revenue from TicketPayment
    ticket_payment_revenue = TicketPayment.objects.filter(
        event=event,
        verified=True
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Calculate total revenue from PaymentTransaction
    payment_transaction_revenue = PaymentTransaction.objects.filter(
        payment_type='TICKET',
        event_category=event,
        status='successful'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Combine revenues
    total_revenue = ticket_payment_revenue + payment_transaction_revenue
    # Get recent ticket payments (max 5)
    ticket_payments = TicketPayment.objects.filter(
        event=event,
        verified=True
    ).order_by('-date_created')[:5]
    
    # Get recent payment transactions (max 5)
    payment_transactions = PaymentTransaction.objects.filter(
        payment_type='TICKET',
        event_category=event,
        status='PAID'
    ).order_by('-created_at')[:5]
    
    # Combine and sort transactions (newest first)
    recent_transactions = sorted(
        list(ticket_payments) + list(payment_transactions),
        key=lambda x: x.date_created if hasattr(x, 'date_created') else x.created_at,
        reverse=True
    )[:10]  # Ensure we only show 10 most recent
    
    context = {
        'event': event,
        'tickets_sold': tickets_sold,
        'ticket_types_data': ticket_types_data,
        'recent_transactions': recent_transactions,
        'total_revenue': total_revenue
    }

    return render(request, 'dashboard/tickiting/ticketActivity.html', context)

def onlineTransaction(request, event_id):
    event = None
    payments = TicketPayment.objects.all()
    
    
    if event_id:
        event = get_object_or_404(Event, id=event_id)
        payments = payments.filter(event=event, verified=True)
        
   
        total_amount = payments.aggregate(Total=Sum('amount')).get('Total', 0)
        
    
    
    context = {
        'payments': payments,
        'event': event,
        'total_amount': total_amount,
        
        'title': 'Online transactions'
    }
    return render(request, 'dashboard/tickiting/onlineTransaction.html', context)

def ussdTransaction(request, event_id):
    event = None
    payments = PaymentTransaction.objects.all()
    
  
    if event_id:
        event = get_object_or_404(Event, id=event_id)
        payments = payments.filter(event_category=event, status='PAID')
    
    
        total_amount = payments.aggregate(Total=Sum('amount')).get('Total', 0)

    
    
    context = {
        'payments': payments,
        'event': event,
        'total_amount': total_amount,
        'title': 'USSD transactions',
        
    }
    return render(request, 'dashboard/tickiting/ussdTransaction.html', context)