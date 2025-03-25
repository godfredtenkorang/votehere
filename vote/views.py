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



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import CustomSession, PaymentTransaction, Nominees



@csrf_exempt
def payment_callback(request):
    
    try:
        # Try to parse both form data and JSON data
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            data = request.POST.dict()

        

        # Validate required fields
        required_fields = ['transaction_id', 'status', 'amount', 'customerNumber']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            error_msg = f'Missing required fields: {", ".join(missing_fields)}'
            
            return JsonResponse({'status': 'error', 'message': error_msg}, status=400)

        transaction_id = data['transaction_id']
        status = data['status'].lower()
        amount = data['amount']
        customer_number = data['customerNumber']
        order_id = data.get('order_id', '')
        
        # Ensure customer_number starts with 233 if it's a phone number
        if customer_number.startswith("0"):
            customer_number = "233" + customer_number[1:]
        elif not customer_number.startswith("233"):
            customer_number = "233" + customer_number

        # Update or create payment transaction
        transaction, created = PaymentTransaction.objects.update_or_create(
            transaction_id=transaction_id,
            defaults={
                'status': status,
                'amount': amount,
                'order_id': order_id,
                'msisdn': customer_number
            }
        )

        # Find active session for this payment
        session = CustomSession.objects.filter(
            user_id=customer_number,
            level='payment'
        ).first()

        if not session:
            
            return JsonResponse({
                'status': 'error',
                'message': 'No active voting session found'
            }, status=404)

        if status == 'success':
            try:
                nominee = Nominees.objects.get(code=session.candidate_id)
                nominee.total_votes += session.votes
                nominee.save()
                
                
                
                # Clean up session
                session.delete()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Payment processed and votes counted',
                    'nominee': nominee.name,
                    'votes_added': session.votes
                })
            
            except Nominees.DoesNotExist:
                error_msg = f'Nominee with code {session.candidate_id} not found'
                
                return JsonResponse({
                    'status': 'error',
                    'message': error_msg
                }, status=404)
            
            except Exception as e:
                error_msg = f'Error updating nominee votes: {str(e)}'
                
                return JsonResponse({
                    'status': 'error',
                    'message': error_msg
                }, status=500)
        
        else:
            # Payment failed - you might want to keep the session for retry
           
            return JsonResponse({
                'status': 'error',
                'message': f'Payment failed with status: {status}'
            }, status=400)

    except Exception as e:
        error_msg = f'Unexpected error processing callback: {str(e)}'
        
        return JsonResponse({
            'status': 'error',
            'message': error_msg
        }, status=500)