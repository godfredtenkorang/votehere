from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'vote/index.html')


def about(request):
    return render(request, 'vote/about.html')

def policy(request):
    return render(request, 'vote/policy.html')

def termsCondition(request):
    return render(request, 'vote/termsCondition.html')

def contact(request):
    return render(request, 'vote/contact.html')


def nominees(request):
    return render(request, 'vote/nomineesPage.html')

def category(request):
    return render(request, 'vote/category.html')

def nominate(request):
    return render(request, 'vote/nominate.html')

def result(request):
    return render(request, 'vote/resultPage.html')
