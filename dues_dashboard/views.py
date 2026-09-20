from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ussd.models import Faculty, Department


def dues_login(request):
    """Step 1: validate credentials, stash user in session, go to code entry."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Do NOT log in yet — wait for code verification
            request.session['pending_user_id'] = user.id
            return redirect('enter_code')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'dues_dashboard/login.html')


def enter_code(request):
    """Step 2: user enters a Faculty or Department code to determine their role."""
    pending_id = request.session.get('pending_user_id')
    if not pending_id:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('dues_login')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        faculty = Faculty.objects.filter(code__iexact=code).first()
        department = Department.objects.filter(code__iexact=code).first()
        
        if faculty and faculty.user_id == pending_id:
            request.session['scope'] = 'faculty'
            request.session['scope_id'] = faculty.id
            return redirect('faculty_dashboard')
        
        elif department and department.user_id == pending_id:
            request.session['scope'] = 'department'
            request.session['scope_id'] = department.id
            return redirect('department_dashboard')
        else:
            messages.error(request, 'You are not authorized for this code.')
        
        messages.error(request, 'Invalid faculty or department code. Please try again.')
        
    return render(request, 'dues_dashboard/enter_code.html')

# =========================================================
# SUPER ADMIN
# =========================================================

def super_dashboard(request):
    return render(
        request,
        "dues_dashboard/super_admin/dashboard.html"
    )


def super_payments(request):
    return render(
        request,
        "dues_dashboard/super_admin/payments.html"
    )


def super_payment_detail(request, transaction_ref):
    return render(
        request,
        "dues_dashboard/super_admin/payment_detail.html"
    )


def super_faculties(request):
    return render(
        request,
        "dues_dashboard/super_admin/faculties.html"
    )


def super_faculty_detail(request, faculty_code):
    return render(
        request,
        "dues_dashboard/super_admin/faculty_detail.html"
    )


def super_departments(request):
    return render(
        request,
        "dues_dashboard/super_admin/departments.html"
    )


def super_department_detail(request, department_code):
    return render(
        request,
        "dues_dashboard/super_admin/department_detail.html"
    )


def super_students(request):
    return render(
        request,
        "dues_dashboard/super_admin/students.html"
    )


def super_student_detail(request, student_id):
    return render(
        request,
        "dues_dashboard/super_admin/student_detail.html"
    )


def super_reports(request):
    return render(
        request,
        "dues_dashboard/super_admin/reports.html"
    )


def super_settings(request):
    return render(
        request,
        "dues_dashboard/super_admin/settings.html"
    )


# =========================================================
# FACULTY ADMIN
# Backend will later restrict data to logged-in Faculty
# =========================================================

def faculty_dashboard(request):
    return render(
        request,
        "dues_dashboard/faculty_admin/dashboard.html"
    )


def faculty_payments(request):
    return render(
        request,
        "dues_dashboard/faculty_admin/payments.html"
    )


def faculty_students(request):
    return render(
        request,
        "dues_dashboard/faculty_admin/students.html"
    )


def faculty_student_detail(request, student_id):
    return render(
        request,
        "dues_dashboard/faculty_admin/student_detail.html"
    )


def faculty_reports(request):
    return render(
        request,
        "dues_dashboard/faculty_admin/reports.html"
    )


def faculty_department_detail(request, department_code):
    return render(
        request,
        "dues_dashboard/faculty_admin/department_detail.html"
    )


# =========================================================
# DEPARTMENT ADMIN
# Backend will later restrict data to logged-in Department
# =========================================================

def department_dashboard(request):
    return render(
        request,
        "dues_dashboard/department_admin/dashboard.html"
    )


def department_payments(request):
    return render(
        request,
        "dues_dashboard/department_admin/payments.html"
    )


def department_students(request):
    return render(
        request,
        "dues_dashboard/department_admin/students.html"
    )


def department_student_detail(request, student_id):
    return render(
        request,
        "dues_dashboard/department_admin/student_detail.html"
    )


def department_reports(request):
    return render(
        request,
        "dues_dashboard/department_admin/reports.html"
    )