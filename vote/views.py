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


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Extract data from the callback
            transaction_id = data.get('transaction_id')
            status = data.get('status')
            amount = data.get('amount')
            customer_number = data.get('customerNumber')
            order_id = data.get('order_id')  # Get the order_id from the callback
            
            

            # Update the PaymentTransaction record
            transaction = PaymentTransaction.objects.filter(transaction_id=transaction_id).first()
            
            if transaction:
                transaction.status = status
                transaction.amount = amount
                transaction.save()
            else:
                # If transaction doesn't exist, create a new one (optional)
                transaction = PaymentTransaction.objects.create(
                    transaction_id=transaction_id,
                    status=status,
                    amount=amount,
                    order_id=order_id,
                    msisdn=customer_number
                )

            # Handle session based on payment status
            session = CustomSession.objects.filter(
                user_id=customer_number,
                level='payment'
            ).first()

            if session:
                if status.lower() == "success":
                    try:
                        nominee = Nominees.objects.get(code=session.candidate_id)
                        nominee.total_vote += session.votes # Add the votes from the session
                        nominee.save()
                        
                        # Delete the session after successful processing
                        session.delete()
                    
                        return JsonResponse({
                            'status': 'success', 
                            'message': 'Payment processed and votes added to nominee.'
                        }, status=200)
                    except Nominees.DoesNotExist:
                        return JsonResponse({
                            'status': 'error', 
                            'message': 'Nominee not found.'
                         }, status=404)
                    except Exception as e:
                        return JsonResponse({
                            'status': 'error',
                            'message': f'Error updating nominee votes {str(e)}'
                        }, status=500)
                else:
                    # Payment failed, you might want to keep the session for retry
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'Payment failed, session retained.'
                    }, status=400)
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Session not found.'
                }, status=404)

        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error', 
        'message': 'Invalid request method'
    }, status=405)

