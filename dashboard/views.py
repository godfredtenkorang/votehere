from django.shortcuts import render

# Create your views here.

def admin(request):
    context = {
        'title': 'adminPage'
    }
    return render(request, 'dashboard/admin.html', context)


