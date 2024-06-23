from django.shortcuts import render, redirect, get_object_or_404
from .models import Register
from django.contrib import messages
from vote.models import Category


def nominate(request, nominate_slug):
    award = Category.objects.get(slug=nominate_slug)
    if request.method == "POST":
        image = request.FILES['image']
        category = request.POST['category']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        content = request.POST['content']
        
        nominate_user = Register(image=image, category=category, name=name, phone=phone, email=email, content=content, award=award)
        nominate_user.save()
    context = {
        'title': 'Nominate',
        'award': award
    }
    return render(request, 'register/nominate.html', context)
    
