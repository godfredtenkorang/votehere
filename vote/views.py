from django.shortcuts import render, get_object_or_404

from payment.models import Nominees
from ussd.models import CustomSession, PaymentTransaction
from .models import *
from django.db.models import Q  # New
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    search_item = request.GET.get('search')
    
    if search_item:
        all_categories = Category.objects.filter(Q(award__icontains=search_item))
    else:
        all_categories = Category.objects.all()

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

def blog_detail(request):
    context = {
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
    category = None
    award = SubCategory.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        award = award.filter(category=category)

    context = {
        'category': category,
        'award': award,
        'title': 'Category Detail'
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


@csrf_exempt
def webhook_callback(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body.decode('utf-8'))
            print(f'Received webhook data: {data}')

            # Process the webhook data
            event_type = data.get('event')  # Example: 'transaction.completed', 'transaction.failed', etc.
            transaction_id = data.get('transaction_id')

            # Handle different event types
            if event_type == 'transaction.completed':
                # Handle successful transaction
                print(f'Transaction {transaction_id} completed successfully.')
                # Update your database or perform actions as needed
            elif event_type == 'transaction.failed':
                # Handle failed transaction
                print(f'Transaction {transaction_id} failed.')
                # Update your database or perform actions as needed
            # Add more event handling as needed

            return JsonResponse({'status': 'success'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            print(f'Error: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)