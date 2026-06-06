from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from dashboard.forms import CategorySMSForm, PaymentTransactionForm, SendSmsForm
from dashboard.utils import send_access_code_to_new_nominee, send_mnotify_sms, send_sms_to_new_nominee
from payment.models import Nominees, Payment, RequestForPayment
from ussd.models import PaymentTransaction
from vote.models import Blog, Category, SubCategory
from django.utils import timezone
from django.db.models import Sum, Q, Count, Case, When, IntegerField
from django.db import transaction
from .forms import NomineeForm, BlogForm

from register.models import EventOrganizer
from django.views.decorators.http import require_POST
import json
from django.utils.text import slugify
import random
import string
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from ticket.models import Event




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
        total_votes = award.aggregate(total=Sum('total_vote'))['total'] or 0
        
        


    context = {
        'category': category,
        'award': award,
        'total_votes': total_votes,
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


def get_bulk_voting_transactions_by_category(request, category_slug):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view transactions.")
        return redirect('adminHome')
    
    category = get_object_or_404(Category, slug=category_slug)
    transactions = Payment.objects.filter(category=category, is_bulk=True, verified=True).order_by('-date_created')
    
    total_amount = transactions.aggregate(total=Sum('total_amount'))['total'] or 0
    transaction_count = transactions.count()
    
    context = {
        'category': category,
        'transactions': transactions,
        'total_amount': total_amount,
        'transaction_count': transaction_count,
        'title': f'Bulk Voting Transactions - {category.title}'
    }
    return render(request, 'maindashboard/bulk_voting_transactions.html', context)

# USSD
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

# Online
# Filter online transactions by phone number
def filter_online_transactions(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view transactions.")
        return redirect('adminHome')
    
    # Ger filter parameters
    phone_number = request.GET.get('phone_number', '').strip()
    reference = request.GET.get('reference', '').strip()
    category_filter = request.GET.get('category', '').strip()
    
    # Base queryset
    transactions = Payment.objects.select_related('category', 'content', 'nominee').all().order_by('-date_created')
    
    if phone_number:
        transactions = transactions.filter(phone__icontains=phone_number)
    
    if reference:
        transactions = transactions.filter(ref__icontains=reference)
        
    if category_filter:
        transactions = transactions.filter(category__award__icontains=category_filter)
        
    # Calculate statictics
    total_count = transactions.count()
    verified_count = transactions.filter(verified=True).count()
    not_verified_count = transactions.filter(verified=False).count()
    bulk_count = transactions.filter(is_bulk=True).count()
    total_amount = transactions.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Get unique categories for filter dropdown
    categories = Category.objects.filter(payment__isnull=False).distinct()
    
    context = {
        'transactions': transactions,
        'total_amount': total_amount,
        'total_count': total_count,
        'verified_count': verified_count,
        'not_verified_count': not_verified_count,
        'bulk_count': bulk_count,
        'categories': categories,
        'filter_params': {
            'phone_number': phone_number,
            'reference': reference,
            'category': category_filter,
        },
        'title': 'Online Transactions'
    }
    return render(request, 'maindashboard/online_transactions.html', context)

@transaction.atomic
def verify_payment(request, payment_id):
    """Verify a specific transaction and update votes"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to verify transactions.")
        return redirect('adminHome')
    
    try:
        payment = Payment.objects.select_for_update().get(id=payment_id)
        
        if payment.verified:
            messages.warning(request, f'Transaction {payment.ref} is already verified.')
            return redirect('filter_online_transactions')
        
        # Mark as verified and save to update the status before adding votes
        payment.verified = True
        payment.save()
        
        # Add votes to nominee if payment is verified
        nominee = payment.nominee
        if nominee:
            nominee.total_vote += payment.vote
            nominee.save()
            
            # Update category vote count if needed
            category = payment.category
            if category:
                category.total_vote = Nominees.objects.filter(category=category).aggregate(total=Sum('total_vote'))['total'] or 0
                category.save()
            messages.success(request, f'Transaction {payment.ref} verified successfully! Added {payment.vote} votes to {nominee.name}.')
        else:
            messages.warning(request, f'Transaction {payment.ref} verified but no nominee found to add votes.')
        
    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found.')
        
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')
        
    return redirect('filter_online_transactions')

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


def blog_list(request):
    blogs = Blog.objects.all().order_by('-date_added')
    context = {
        'blogs': blogs,
        'title': 'Blog List'
    }
    return render(request, 'maindashboard/blog_list.html', context)

def add_blog(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to add blog.")
        return redirect('adminHome')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, f'Blog {blog.title} added successfully.')
            return redirect('blog_list')
    else:
        form = BlogForm()
    
    context = {
        'form': form,
        'title': 'Add Blog'
    }
    
    return render(request, 'maindashboard/add_blog.html', context)

def update_blog(request, blog_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to update blog.")
        return redirect('adminHome')
    
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, f'Blog {blog.title} updated successfully.')
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
    
    context = {
        'form': form,
        'title': 'Update Blog'
    }
    
    return render(request, 'maindashboard/update_blog.html', context)

def delete_blog(request, blog_id):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to delete blog.")
        return redirect('adminHome')
    
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, f'Blog {blog.title} deleted successfully.')
    return redirect('blog_list')


def receipt(request):
    
    return render(request, 'maindashboard/receipt.html') 

def send_all_sms(request):
    
    return render(request, 'maindashboard/send_all_sms.html') 

def transactions(request):
    
    return render(request, 'maindashboard/transactions.html') 

def addAward(request):
    if request.method == 'POST':
        award = request.POST.get('award', '').strip()
        title = request.POST.get('title', '').strip()
        image = request.FILES.get('image')
        slug = request.POST.get('slug', '').strip()
        date_added = request.POST.get('date_added') or None
        end_date = request.POST.get('end_date') or None
        access_code = request.POST.get('access_code', '').strip() or None
        link = request.POST.get('link', '').strip() or None
        nomination_end_date = request.POST.get('nomination_end_date') or None
        bulk_raw = request.POST.get('bulk_voting_options', '').strip()
        close_result = request.POST.get('close_result') == 'on'
        percentage_earned = request.POST.get('percentage_earned', '80').strip() or '80'
        
        # --- validate required fields ---
        errors = []
        if not award:
            errors.append("Award name is required.")
        if not slug:
            errors.append("Slug is required.")
        if not image:
            errors.append("Award image is required.")
        if not date_added:
            errors.append("Date added is required.")
        if not end_date:
            errors.append("End date is required.")
            
        # --- validate JSON ---
        bulk_voting_options = []
        if bulk_raw:
            try:
                bulk_voting_options = json.loads(bulk_raw)
                if not isinstance(bulk_voting_options, list):
                    errors.append("Bulk voting options must be a JSON array.")
            except json.JSONDecodeError as e:
                errors.append(f"Bulk voting options - invalid JSON: {e}")
                
        # --- check slug uniqueness ---
        if slug and Category.objects.filter(slug=slug).exists():
            errors.append(f'The slug "{slug}" is already in use. Please choose a different slug.')
            
        if errors:
            for err in errors:
                messages.error(request, err)
                
            # Return to form with existing data
            return render(request, 'maindashboard/addAward.html', {
                'request': request
            })
        else:
            try:
                category = Category(
                    award=award,
                    title=title or None,
                    slug=slug,
                    image=image,
                    date_added=date_added,
                    end_date=end_date,
                    access_code=access_code,
                    link=link,
                    nomination_end_date=nomination_end_date or None,
                    percentage_earned=percentage_earned,
                    bulk_voting_options=bulk_voting_options,
                    close_result=close_result,
                )
                category.save()
                messages.success(request, f'Award "{category.award}" created successfully.')
                return redirect('addAward')
                
            except Exception as e:
                
                messages.error(request, f'An error occurred while creating the award: {str(e)}')
                
                return render(request, 'maindashboard/addAward.html', {
                    'request': request
                })
    return render(request, 'maindashboard/addAward.html') 

def sendMessage(request):
    
    return render(request, 'maindashboard/sendMessage.html') 

def bookings(request):
    events = EventOrganizer.objects.all()
    context = {
        'events': events,
        'title': 'Bookings'
    }
    return render(request, 'maindashboard/bookings.html', context)

@require_POST
def approve_booking(request, event_id):
    event = get_object_or_404(EventOrganizer, id=event_id)
    event.is_approved = True
    event.save()
    messages.success(request, f'Event "{event.event_name}" approved successfully.')
    return redirect('bookings')

@require_POST
def delete_booking(request, event_id):
    event = get_object_or_404(EventOrganizer, id=event_id)
    event.delete()
    messages.success(request, f'Event "{event.event_name}" deleted successfully.')
    return redirect('bookings')

def requested_payment(request):
    payment_requests = RequestForPayment.objects.all()
    return render(request, 'maindashboard/requestedPayement.html', {'payment_requests': payment_requests})

@csrf_exempt
@staff_member_required
def approve_payment(request, payment_id):
    """Approve a payment request via AJAX"""
    if request.method == 'POST':
        try:
            payment = get_object_or_404(RequestForPayment, id=payment_id)
            payment.is_approved = True
            payment.save()
            return JsonResponse({
                'success': True,
                'message': f'Payment request "{payment.name}" approved successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=400)
            
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)
    

@csrf_exempt
@staff_member_required
def delete_payment(request, payment_id):
    """Delete a payment request via AJAX"""
    if request.method == 'POST':
        try:
            payment = get_object_or_404(RequestForPayment, id=payment_id)
            payment_name = payment.name  # Store name before deletion
            payment.delete()
            return JsonResponse({
                'success': True,
                'message': f'Payment request "{payment_name}" deleted successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=400)
            
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)


def election(request):
    
    return render(request, 'maindashboard/election.html') 

import json

def addAwards(request):
            
    return render(request, 'maindashboard/addAwards.html') 

import datetime

def AddSubCategory(request):
    if request.method == 'POST':
        # Get form data
        category_name = request.POST.get('category')
        content = request.POST.get('content')
        slug = request.POST.get('slug')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
        # Handle the checkbox - it will be 'on' if checked, None if not
        can_view_result = request.POST.get('can_view_result') == 'on'
        
        # Validate required fields
        if not category_name or not content or not slug:
            messages.error(request, 'Category, Content, and Slug are required fields!')
            return redirect('AddCategory')
        
        # Check if slug already exists
        if SubCategory.objects.filter(slug=slug).exists():
            messages.error(request, 'A subcategory with this slug already exists!')
            return redirect('AddCategory')
        
        # Get category instance
        try:
            category = Category.objects.get(award=category_name)
        except Category.DoesNotExist:
            messages.error(request, 'Selected category does not exist!')
            return redirect('AddCategory')
        
        # Combine date and time if both are provided
        if date_str and time_str:
            try:
                combine_datetime = datetime.datetime.strptime(
                    f"{date_str} {time_str}",
                    "%Y-%m-%d %H:%M"
                )
                date = timezone.make_aware(combine_datetime)
            except ValueError:
                date = timezone.now()
                
        elif date_str:
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                date = timezone.make_aware(date)
            except ValueError:
                date = timezone.now()
        else:
            date = timezone.now()
            
        # Create the subcategory
        subcategory = SubCategory.objects.create(
            category=category,
            content=content,
            slug=slug,
            date=date,
            can_check_result=can_view_result
        )
        
        messages.success(request, f'Subcategory "{content}" has been added successfully!')
        return redirect('AddCategory')
    
    # Get all categories for the dropdown
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
        
    return render(request, 'maindashboard/AddCategory.html', context) 

# Election
def manageElection(request):
    
    return render(request, 'maindashboard/manageElection.html') 
def AddElectionCategory(request):
    
    return render(request, 'maindashboard/AddElectionCategory.html') 

def AddCandidate(request):
    return render(request, 'maindashboard/AddCandidate.html') 

def LiveVoting(request):
    
    return render(request, 'maindashboard/LiveVoting.html') 


def create_ussd_transactions(request):
    if request.method == 'POST':
        try:
            # Get from data
            order_id = request.POST.get('order_id')
            amount = Decimal(request.POST.get('amount', '0'))
            status = request.POST.get('status')
            payment_type = request.POST.get('payment_type')
            invoice_no = request.POST.get('invoice_no')
            transaction_id = request.POST.get('transaction_id', '')
            trans_hash = request.POST.get('trans_hash', '')
            account_number = request.POST.get('account_number', '')
            account_name = request.POST.get('account_name', '')
            nominee_code = request.POST.get('nominee_code', '')
            votes = request.POST.get('votes', '0')
            category_id = request.POST.get('category')
            event_code = request.POST.get('event_code', '')
            tickets = request.POST.get('tickets', '0')
            ticket_type = request.POST.get('ticket_type', '')
            event_category_id = request.POST.get('event_category')
            donation_code = request.POST.get('donation_code', '')
            
            # Handle timestamp if provided
            date_str = request.POST.get('date', '')
            time_str = request.POST.get('time', '')
            timestamp = None
            if date_str and time_str:
                try:
                    timestamp = datetime.strptime(
                        f"{date_str} {time_str}",
                        "%Y-%m-%d %H:%M"
                    )
                    
                except:
                    timestamp = timezone.now()
            else:
                timestamp = timezone.now()
                
            # Validate required fields
            if not order_id:
                messages.error(request, 'Order ID is required!')
                return redirect('create_ussd_transactions')
            
            # Check if transaction with the same order_id already exists
            if PaymentTransaction.objects.filter(order_id=order_id).exists():
                messages.error(request, f'Transaction with Order ID "{order_id}" already exists!')
                return redirect('create_ussd_transactions')
            
            # Process vote transaction
            nominee = None
            if payment_type == 'VOTE' and nominee_code:
                try:
                    nominee = Nominees.objects.get(code=nominee_code)
                    
                    # Validate votes count
                    if votes and int(votes) > 0:
                        # Calculate expected amount matches expected (can be disabled if not needed)
                        expected_amount = int(votes) * nominee.price_per_vote
                        
                        # Optional: Verify amount matches expected (can be disabled if not needed)
                        # if amount != expected_amount:
                        #     messages.warning(request, f'Amount does not match votes count. Expected: {expected_amount}, Received: {amount}')
                        
                    # Add votes to nominee's total_vote
                    nominee.total_vote += int(votes) if votes else 0
                    nominee.save()
                except Nominees.DoesNotExist:
                    messages.warning(request, f'No nominee found with code "{nominee_code}". Transaction will be created without linking to a nominee.')
                    
            # Get category object if provided
            category = None
            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    messages.warning(request, f'No category found with ID "{category_id}". Transaction will be created without linking to a category.')
                    
            # Get event category object if provided
            event_category = None
            if event_category_id:
                try:
                    
                    event_category = Event.objects.get(id=event_category_id)
                except Event.DoesNotExist:
                    messages.warning(request, f'No event found with ID "{event_category_id}". Transaction will be created without linking to an event.')
                    
            # Create the transaction
            transaction = PaymentTransaction.objects.create(
                order_id=order_id,
                amount=amount,
                status=status,
                payment_type=payment_type,
                invoice_no=invoice_no,
                transaction_id=transaction_id,
                trans_hash=trans_hash,
                account_number=account_number,
                account_name=account_name,
                nominee_code=nominee_code,
                votes=int(votes) if votes else None,
                category=category,
                event_code=event_code,
                tickets=int(tickets) if tickets else None,
                ticket_type=ticket_type,
                event_category=event_category,
                donation_code=donation_code,
                timestamp=timestamp,
            )
            
            # Success message
            if payment_type == 'VOTE' and nominee:
                messages.success(request, f'Vote transaction created successfully! Added {votes} votes to nominee "{nominee.name}".')
            elif payment_type == 'VOTE':
                messages.success(request, f'Vote transaction created successfully! No nominee linked.')
            else:
                messages.success(request, f'Transaction created successfully!')
                
            return redirect('payment_transactions')
        
        except Exception as e:
            messages.error(request, f'An error occurred while creating the transaction: {str(e)}')
            return redirect('create_ussd_transactions')
        
    context = {
        'title': 'Create USSD Transaction',
        'categories': Category.objects.all(),
        'events': Event.objects.all(),
    }
    return render(request, 'maindashboard/create_ussd_transactions.html', context) 