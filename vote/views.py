from django.shortcuts import render, get_object_or_404, redirect

from payment.models import Nominees
from register.forms import EventOrganizerForm
from register.models import EventOrganizer
from ussd.models import CustomSession, PaymentTransaction
from .models import *
from django.db.models import Q  # New
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from .utils import receive_sms_from_event_organizer


def index(request):
    search_item = request.GET.get('search')
    
    if search_item:
        all_categories = Category.objects.filter(Q(award__icontains=search_item))
    else:
        all_categories = Category.objects.all()[:6]

    context = {
        'all_categories': all_categories,
    }
    return render(request, 'vote/index.html', context)


def about(request):
    context = {
        'title': 'About us'
    }
    return render(request, 'vote/about.html', context)

def blog(request):
    blogs = Blog.objects.all()
    context = {
        'blogs': blogs,
        'title': 'Blog',
    }
    return render(request, 'vote/blog.html', context)

def blog_detail(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    context = {
        'blog': blog,
        'title': 'Blog Detail'
    }
    return render(request, 'vote/blog-detail.html', context)


def policy(request):
    context = {
        'title': 'About us'
    }
    return render(request, 'vote/policy.html', context)


def termsCondition(request):
    context = {
        'title': 'About us'
    }
    return render(request, 'vote/termsCondition.html', context)


def contact(request):
    context = {
        'title': 'About us'
    }
    return render(request, 'vote/contact.html', context)



def category(request, category_slug=None):
    search_item = request.GET.get('search')
    
    
    category = None
    award = SubCategory.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        award = award.filter(category=category)
        
    # Add search functionality
    if search_item:
        award = award.filter(
            Q(category__title__icontains=search_item) | 
            Q(content__icontains=search_item)
        )
    
    now = timezone.now().date()

    context = {
        'category': category,
        'award': award,
        'title': 'Category Detail',
        'search_item': search_item,  # Pass the search term back to template
        'now': now
    }
    return render(request, 'vote/category.html', context)


def category_search_view(request, category_slug=None):
    
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.filter(category=category)
        
    context = {
        "category": category,
        "categories": categories,
    }
    
    return render(request, "vote/search.html", context)


def custom_404_view(request, exception):
    return render(request, 'vote/404.html', status=404)

from django.views.decorators.http import require_POST

# @csrf_exempt
# def webhook_callback(request):
#     if request.method == 'POST':
#         try:
#             # Parse the incoming JSON data
#             data = json.loads(request.body.decode('utf-8'))
#             print(f'Received webhook data: {data}')

#             # Extract relevant fields
#             event_type = data.get('event')  # e.g., 'transaction.completed', 'transaction.failed'
#             transaction_id = data.get('transaction_id')
#             status = data.get('status')  # e.g., 'completed', 'failed'
#             amount = data.get('amount')
#             customer_number = data.get('customer_number')
#             nominee_code = data.get('nominee_code')  # Assumed to be provided
#             network = data.get('network')  # Network used for the transaction
#             raw_response = json.dumps(data)  # Store the entire response as a string

#             # Handle different event types
#             if event_type == 'transaction.completed':
#                 return handle_transaction_completed(transaction_id, status, amount, customer_number, nominee_code, network, raw_response)

#             elif event_type == 'transaction.failed':
#                 return handle_transaction_failed(transaction_id)

#             return JsonResponse({'status': 'error', 'message': 'Unknown event type.'}, status=400)

#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
#         except Exception as e:
#             print(f'Error: {str(e)}')
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


# def handle_transaction_completed(request, transaction_id, status, amount, customer_number, nominee_code, network, raw_response):
#     # Find or create the transaction record
#     data = json.loads(request.body.decode('utf-8'))
#     transaction, created = PaymentTransaction.objects.get_or_create(
#         transaction_id=transaction_id,
        
#         defaults={
#             'order_id': data.get('order_id', ''),
#             'status': status,
#             'amount': amount,
#             'customer_number': customer_number,
#             'network': network,
#             'raw_response': raw_response
#         }
#     )

#     if not created:
#         # If the transaction already exists, update its status
#         transaction.status = status
#         transaction.amount = amount
#         transaction.customer_number = customer_number
#         transaction.network = network
#         transaction.raw_response = raw_response
#         transaction.save()

#     if status == 'completed':
#         # Handle successful transaction
#         nominee = Nominees.objects.filter(code=nominee_code).first()
#         if nominee:
#             nominee.total_vote += 1  # Increment vote count
#             nominee.save()
#             return JsonResponse({'status': 'success', 'message': 'Vote added to nominee.'}, status=200)
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Nominee not found.'}, status=404)

#     return JsonResponse({'status': 'error', 'message': 'Transaction not successful.'}, status=400)

# def handle_transaction_failed(transaction_id):
#     # Handle failed transaction logic here
#     print(f'Transaction {transaction_id} failed.')
#     return JsonResponse({'status': 'error', 'message': 'Transaction failed.'}, status=400)



# Create your views here.

def award_page(request):
    search_item = request.GET.get('search')
    
    if search_item:
        all_categories = Category.objects.filter(Q(award__icontains=search_item))
    else:
        all_categories = Category.objects.all()

    context = {
        'all_categories': all_categories,
    }
    return render(request, 'vote/awardPage.html', context)


def joinUs(request):
    if request.method == 'POST':
        # Get form data
        event_name = request.POST.get('event_name')
        organization_name = request.POST.get('organization_name')
        contact_name = request.POST.get('contact_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        event_description = request.POST.get('event_description')
        event_type = request.POST.get('event_type')
        promo_code = request.POST.get('promo_code', None)
        
        # Basic validation
        if not all([event_name, organization_name, contact_name, phone_number, email, event_description, event_type]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('joinUs')
        
        # Save to database
        try:
            EventOrganizer.objects.create(
                event_name=event_name,
                organization_name=organization_name,
                contact_name=contact_name,
                phone_number=phone_number,
                email=email,
                event_description=event_description,
                event_type=event_type,
                promo_code=promo_code if promo_code else None
            )
            receive_sms_from_event_organizer(event_name)
            messages.success(request, 'Your application has been submitted successfully! We will contact you soon.')
            return redirect('joinUs')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('joinUs')
    context = {
        
    }
    return render(request, 'vote/joinUs.html', context)