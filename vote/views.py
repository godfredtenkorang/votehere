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
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_GET
from django.utils import timezone


def index(request):
    search_item = request.GET.get('search')
    nominee_code = request.GET.get('nominee_code')
    
    # Hnadle nominee code search (redirect to vote page)
    if nominee_code:
        try:
            nominee = Nominees.objects.get(code=nominee_code)
            return redirect('vote-page', nominee_slug=nominee.slug)
        except Nominees.DoesNotExist:
            messages.error(request, 'Invalid nominee code. Please try again.')
            return redirect('index')
    
    if search_item:
        all_categories = Category.objects.filter(Q(award__icontains=search_item))
    else:
        all_categories = Category.objects.all()[:8]

    context = {
        'all_categories': all_categories,
    }
    return render(request, 'vote/index.html', context)


def about(request):
    context = {
        'title': 'About us'
    }
    return render(request, 'vote/about.html', context)


class BlogListView(ListView):
    model = Blog
    template_name = 'vote/blog.html'
    context_object_name = 'blogs'
    paginate_by = 8  # Number of blogs per page
    
    def get_queryset(self):
        return Blog.objects.filter(blog_recommended=True).order_by('-date_added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommended_blogs'] = Blog.objects.filter(blog_recommended=True).order_by('-date_added')[:3]
        return context

def blog(request):
    blogs = Blog.objects.all()
    context = {
        'blogs': blogs,
        'title': 'Blog',
    }
    return render(request, 'vote/blog.html', context)

# def blog_detail(request, blog_slug):
#     blog = get_object_or_404(Blog, slug=blog_slug)
#     context = {
#         'blog': blog,
#         'title': 'Blog Detail'
#     }
#     return render(request, 'vote/blog-detail.html', context)

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'vote/blog-detail.html'
    context_object_name = 'blog'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['share_urls'] = self.object.get_share_urls(self.request)
        context['recommended_blogs'] =  Blog.objects.filter(blog_recommended=True).exclude(id=self.object.id).order_by('-date_added')[:3]
        return context

def blog_detail(request):
    return render(request, 'vote/blog-detail.html')

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
    category_updates = []
    bulk_voting_data = []
    time_remaining = None
    dynamic_updates = []
    
    
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        award = award.filter(category=category)
        
        # Get category-specific updates
        category_updates = CategoryUpdate.objects.filter(
            category=category,
            is_active=True
        )[:10]  # Limit to the latest 100 updates
        
        # Add dynamic updates based on category status
        dynamic_updates = []
        
        # Check if voting is ending soon (e.g., within 24 hours)
        if category.end_date and timezone.now() <= category.end_date:
            time_remaining = category.end_date - timezone.now()
            if time_remaining.total_seconds() <= 86400:  # 24 hours
                dynamic_updates.append({
                    "message": f"⚠️ Voting for {category.award} ends in {time_remaining.seconds//3600} hours! Cast your vote now!",
                    "update_type": "deadline"
                })
                
        # Check nomination period
        if category.nomination_end_date and category.nomination_end_date > timezone.now().date():
            days_until_nomination_end = (category.nomination_end_date - timezone.now().date()).days
            
            if 0 < days_until_nomination_end <= 3:
                dynamic_updates.append({
                    "message": f"📢 Nomination for {category.award} ends in {days_until_nomination_end} days! Nominate your favorite now!",
                    "update_type": "warning"
                })
        # Add nomination ended message
        if category.nomination_end_date and category.nomination_end_date <= timezone.now().date():
            if category.end_date and timezone.now() <= category.end_date:
                dynamic_updates.append({
                    "message": f"✅ Nominations for {category.award} have closed. Voting is now in progress!",
                    "update_type": "success"
                })
        
        # Add voting ended message
        if category.end_date and timezone.now() > category.end_date:
            dynamic_updates.append({
                "message": f"🏆 Voting for {category.award} has ended. Thank you for your participation!",
                "update_type": "warning"
            })
                
        # Add bulk voting options to context
        if category.bulk_voting_options:
            bulk_voting_data = category.bulk_voting_options
            
            
        
    # Add search functionality
    if search_item:
        award = award.filter(
            Q(category__title__icontains=search_item) | 
            Q(content__icontains=search_item)
        )
    
    now = timezone.now().date()
    
    # Calculate voting progress for category
    voting_progress = None
    if category and category.end_date:
        total_voting_days = (category.end_date.date() - category.date_added.date()).days
        days_elipsed = (now - category.date_added.date()).days
        if total_voting_days > 0:
            voting_progress = min(100, (days_elipsed / total_voting_days) * 100)
            
    # Merge category_updates and dynamic_updates for the context
    # Convert category_updates queryset to list of dicts for easier merging
    merged_updates = []
    
    # Add database updates
    for update in category_updates:
        merged_updates.append({
            "message": update.message,
            "update_type": update.update_type,
            "created_at": update.created_at
        })
    
    # Add dynamic updates
    merged_updates.extend(dynamic_updates)
    
    # Sort by priority (you can adjust this logic)
    # For now, keep dynamic updates at the end
    # Or sort by created_at if available

    context = {
        'category': category,
        'award': award,
        'title': f'Category Detail - {category.award if category else "All Categories"}',
        'search_item': search_item,  # Pass the search term back to template
        'now': now,
        'category_updates': merged_updates,
        'dynamic_updates': dynamic_updates,
        'bulk_voting_data': bulk_voting_data,
        'voting_progress': voting_progress,
        'time_remaining': time_remaining,
    }
    return render(request, 'vote/category.html', context)

@require_GET
def get_category_updates(request, category_slug):
    """Returns the latest updates for a given category as JSON."""
    try:
        category = Category.objects.get(slug=category_slug)
        updates = CategoryUpdate.objects.filter(
            category=category, 
            is_active=True
        ).values('message', 'update_type', 'created_at')[:5]  # Limit to latest 10 updates
        
        # Add dynamic updates
        dynamic_msgs = []
        if category.end_date and timezone.now() > category.end_date:
            dynamic_msgs.append({
                "message": f"⏰ {category.award} voting has ended! Thank you for participating.",
                "update_type": "warning"
            })
            
        return JsonResponse({
            'success': True,
            'updates': list(updates),
            'dynamic_updates': dynamic_msgs
        })
        
    except Category.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Category not found.'}, status=404)

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