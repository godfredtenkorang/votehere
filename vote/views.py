from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,

    }
    return render(request, 'vote/index.html', context)


def about(request):
    return render(request, 'vote/about.html')


def policy(request):
    return render(request, 'vote/policy.html')


def termsCondition(request):
    return render(request, 'vote/termsCondition.html')


def contact(request):
    return render(request, 'vote/contact.html')


def nominees(request, nominee_slug):
    nominee = get_object_or_404(Nominees, slug=nominee_slug)
    context = {
        'nominee': nominee,
    }
    return render(request, 'vote/nomineesPage.html', context)


def category(request, category_slug=None):
    category = None
    award = Nominees.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        award = award.filter(category=category)

    context = {
        'category': category,
        'award': award,
        'title': 'Category Detail'
    }
    return render(request, 'vote/category.html', context)



def result(request):
    return render(request, 'vote/resultPage.html')
