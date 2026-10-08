from decimal import Decimal

from django.db.models.aggregates import Count, Sum
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ussd.models import Faculty, Department, PaymentTransaction, LevelDues
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count


def dues_login(request):
    """Step 1: validate credentials, stash user in session, go to code entry."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Do NOT log in yet — wait for code verification
            request.session['pending_user_id'] = user.id
            request.session['pending_backend'] = user.backend
            return redirect('enter_code')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'dues_dashboard/login.html')


def enter_code(request):
    """Step 2: user enters a Faculty or Department code to determine their role."""
    pending_id = request.session.get('pending_user_id')
    pending_backend = request.session.get('pending_backend')
    if not pending_id:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('dues_login')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        faculty = Faculty.objects.filter(code__iexact=code).first()
        department = Department.objects.filter(code__iexact=code).first()
        
        user = User.objects.get(id=pending_id)
        
        if faculty and faculty.user_id == pending_id:
            # Actually log the user in now
            
            login(request, user, backend=pending_backend)
            
            request.session.pop('pending_user_id', None)
            request.session.pop('pending_backend', None)
            
            request.session['scope'] = 'faculty'
            request.session['scope_id'] = faculty.id
            return redirect('faculty_dashboard')
        
        elif department and department.user_id == pending_id:
            # Actually log the user in now
           
            login(request, user, backend=pending_backend)
            request.session.pop('pending_user_id', None)
            request.session.pop('pending_backend', None)

            request.session['scope'] = 'department'
            request.session['scope_id'] = department.id
            request.session['faculty_id'] = department.faculty_id
            return redirect('department_dashboard')
        else:
            messages.error(request, 'You are not authorized for this code.')
        
    return render(request, 'dues_dashboard/enter_code.html')

def dues_logout(request):
    logout(request)
    request.session.flush()   # clears scope, scope_id, pending_user_id
    return redirect('dues_login')

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
@login_required
def faculty_dashboard(request):
    # Guard: must have chosen a faculty scope
    if request.session.get('scope') != 'faculty':
        messages.error(request, 'Please enter a valid faculty code.')
        return redirect('enter_code')
    
    faculty_id = request.session.get('scope_id')
    faculty = Faculty.objects.get(id=faculty_id)
    
    # ---- Filters (from GET params, defaults to active year/semester) ----
    academic_year = request.GET.get('academic_year', '2026/2027')
    semester = request.GET.get('semester', '')
    department_code = request.GET.get('department', '')
    level = request.GET.get('level', '')
    
    # Base queryset: paid dues belonging to this faculty
    base_qs = PaymentTransaction.objects.filter(
        faculty=faculty, 
        payment_type='DUES',
        status='PAID',
        academic_year=academic_year,
        )
    if department_code:
        base_qs = base_qs.filter(department__code=department_code)
    if level:
        base_qs = base_qs.filter(level=level)
        
    # ---- Summary cards ----
    totals = base_qs.aggregate(
        total=Sum('amount'),
        students=Count('student_number', distinct=True),
        )
    total_collected = totals['total'] or 0
    student_paid = totals['students'] or 0
    
    # 50/50 split — adjust if your split rule differs
    faculty_split = total_collected / 2
    department_split = total_collected / 2
    
    # ---- Departments table ----
    departments = Department.objects.filter(faculty=faculty)
    dept_rows = []
    for dept in departments:
        dept_qs = base_qs.filter(department=dept)
        agg = dept_qs.aggregate(
            total=Sum('amount'),
            students=Count('student_number', distinct=True),
        )
        dept_total = agg['total'] or 0
        dept_rows.append({
            'code': dept.code,
            'name': dept.name,
            'total': dept_total,
            'faculty_share': dept_total / 2,
            'department_share': dept_total / 2,
            'students_paid': agg['students'] or 0,
        })
    # ---- Recent payments ----
    recent_payments = base_qs.select_related('department').order_by('-created_at')[:10]
    
    context = {
        'faculty': faculty,
        'academic_year': academic_year,
        'semester': semester,
        'department_code': department_code,
        'level': level,
        
        'total_collected': total_collected,
        'students_paid': student_paid,
        'faculty_share': faculty_split,
        'department_share': department_split,
        
        'departments': dept_rows,
        'recent_payments': recent_payments
    }

    return render(
        request,
        "dues_dashboard/faculty_admin/dashboard.html", context
    )


def faculty_payments(request):
    # ---- Scope guard: must have chosen a faculty ----
    if request.session.get('scope') != 'faculty':
        messages.error(request, "Please enter your faculty code.")
        return redirect('enter_code')
    
    
    faculty = Faculty.objects.get(id=request.session['scope_id'])
    
    # ---- GET filters ----
    academic_year = request.GET.get('academic_year', '2026/2027')
    semester = request.GET.get('semester', '')
    department = request.GET.get('department', '')
    level = request.GET.get('level', '')
    status = request.GET.get('status', '')
    search = request.GET.get('q', '').strip()
    
    # ---- Base queryset ----
    qs = (
        PaymentTransaction.objects.filter(
            faculty=faculty,
            payment_type='DUES'
            ).select_related('department').order_by('-timestamp')
    )
    
    if academic_year:
        qs = qs.filter(academic_year=academic_year)
    if semester:
        qs = qs.filter(semester=semester)
    if department:
        qs = qs.filter(department__code=department)
    if level:
        qs = qs.filter(level=level)
    if status:
        qs = qs.filter(status=status.upper())
    if search:
        qs = qs.filter(
            Q(order_id__icontains=search)
            | Q(student_number__icontains=search)
            | Q(student__name__icontains=search)
            
        )
    
    # ---- Attach 50/50 split per row for the template ----
    payments = []
    for p in qs:
        p.faculty_share_amount = (p.amount or 0) / 2
        p.department_share_amount = (p.amount or 0) / 2
        payments.append(p)
        
    # ---- Departments for the filter dropdown (only this faculty's) ----
    departments = Department.objects.filter(faculty=faculty).order_by('name')
    
    # ---- Academic years for the dropdown (distinct from DB, fallback default) ----
    academic_years = list(
        PaymentTransaction.objects.filter(
            faculty=faculty, payment_type='DUES', academic_year__isnull=False
            ).values_list('academic_year', flat=True).distinct()
    )
    if not academic_years:
        academic_years = ['2026/2027']
        
    context = {
        'faculty': faculty,
        'payments': payments,
        'departments': departments,
        'academic_years': academic_years,
        'academic_year': academic_year,
        'semester': semester,
        'department': department,
        'level': level,
        'status': status,
        'search': search
    }

    return render(
        request,
        "dues_dashboard/faculty_admin/payments.html",
        context
    )


def faculty_students(request):
    # ---- Scope guard ----
    if request.session.get('scope') != 'faculty':
        messages.error(request, "Please enter your faculty code")
        return redirect('enter_code')
    
    faculty = Faculty.objects.get(id=request.session['scope_id'])
    
    # ---- GET filters ----
    academic_year = request.GET.get('academic_year', '2026/2027')
    semester = request.GET.get('semester', '')
    department = request.GET.get('department', '')
    level = request.GET.get('level', '')
    status = request.GET.get('status', '')
    search = request.GET.get('q', '').strip()
    
    # ---- Base queryset: every dues payment (any status) for this faculty ----
    qs = PaymentTransaction.objects.filter(faculty=faculty, payment_type='DUES').select_related('department').order_by('timestamp')
    
    if academic_year:
        qs = qs.filter(academic_year=academic_year)
    if semester:
        qs = qs.filter(semester=semester)
    if department:
        qs = qs.filter(department__code=department)
    if level:
        qs = qs.filter(level=level)
    if status:
        qs = qs.filter(status=status.upper())
    if search:
        qs = qs.filter(
            Q(order_id__icontains=search)
            | Q(student_number__icontains=search)
            | Q(student__name__icontains=search)
            
        )
        
    # ---- Collapse to one row per (student_number, academic_year) ----
    # Take the LATEST transaction per student/year as "the" record,
    # but aggregate the paid amount across all PAID transactions.
    
    seen = set()
    students = []
    
    for p in qs:
        key = (p.student_number, p.academic_year)
        if key in seen:
            continue
        seen.add(key)
        
        # Amount paid = sum of PAID transactions for this student/year
        paid_qs = PaymentTransaction.objects.filter(
            faculty=faculty,
            payment_type='DUES',
            student_number=p.student_number,
            academic_year=p.academic_year,
            status='PAID'
        ).aggregate(total=Sum('amount'))
        amount_paid = paid_qs['total'] or 0
        
        # Amount due = LevelDues for this student's dept + level + year
        amount_due = 0
        if p.department_id and p.level:
            due = LevelDues.objects.filter(
                department=p.department,
                level=str(p.level),
                academic_year=p.academic_year,
                is_active=True,
            ).first()
            if due:
                amount_due = due.amount
                
        # Determine display status
        if amount_paid >= amount_due and amount_due > 0:
            display_status = 'Paid'
        elif amount_paid > 0:
            display_status = 'Pending'
        else:
            display_status = p.get_status_display()
            
        students.append({
            'student_number': p.student_number,
            'student_name': p.student_name,
            'department_code': p.department.code if p.department else '',
            'department_name': p.department.name if p.department else '-',
            'level': p.level,
            'academic_year': p.academic_year,
            'semester': (p.extra_data or {}).get('semester', ''),
            'amount_paid': amount_paid,
            'amount_due': amount_due,
            'status': display_status,
        })
        
    # ---- Filter dropdowns ----
    departments = Department.objects.filter(faculty=faculty).order_by('name')
    
    academic_years = list(
        PaymentTransaction.objects.filter(
            faculty=faculty, payment_type='DUES', academic_year__isnull=False
        ).values_list('academic_year', flat=True).distinct()
    )
    if not academic_years:
        academic_years = ['2026/2027']

    context = {
        'faculty': faculty,
        'students': students,
        'departments': departments,
        'academic_years': academic_years,
        'academic_year': academic_year,
        'semester': semester,
        'department': department,
        'level': level,
        'status': status,
        'search': search
    }

    return render(
        request,
        "dues_dashboard/faculty_admin/students.html", context
    )


def faculty_student_detail(request, student_id):
    return render(
        request,
        "dues_dashboard/faculty_admin/student_detail.html"
    )

@login_required
def faculty_reports(request):
    # ---- Scope guard ----
    if request.session.get('scope') != 'faculty':
        messages.error(request, 'Please enter your faculty code.')
        return redirect('enter_code')
    
    faculty = Faculty.objects.get(id=request.session['scope_id'])
    
    # ---- GET filters ----
    academic_year = request.GET.get('academic_year', '2026/2027')
    semester = request.GET.get('semester', '')
    department = request.GET.get('department', '')
    status = request.GET.get('status', '')
    
    # ---- Base queryset: dues transactions for this faculty ----
    qs = PaymentTransaction.objects.filter(faculty=faculty, payment_type='DUES')
    if academic_year:
        qs = qs.filter(academic_year=academic_year)
    if department:
        qs = qs.filter(department=department)
    # If you add a real `semester` field to PaymentTransaction, add:
    # if semester:
    #     qs = qs.filter(semester=semester)

    # ---- Per-department aggregation ----
    departments = Department.objects.filter(faculty=faculty).order_by('name')
    department_rows = []
    overall = {
        'total_collected': 0,
        'faculty_share': 0,
        'department_share': 0,
        'students_paid': 0,
        'pending': 0,
        'failed': 0,
    }
    
    for dept in departments:
        dept_qs = qs.filter(department=dept)
        # Sum of PAID amounts
        paid_agg = dept_qs.filter(status='PAID').aggregate(
            total=Sum('amount'),
            students=Count('student_number', distinct=True),
        )
        total_paid = paid_agg['total'] or 0
        students_paid = paid_agg['students'] or 0

        # Counts of pending/failed (distinct students)
        ending_count = (
            dept_qs.filter(status='Pending').values('student_number').distinct().count()
        )
        failed_count = (
            dept_qs.filter(status='Failed').values('student_number').distinct().count()
        )
        
        # 50/50 split — adjust if your rule differs
        dept_row = {
            'code':dept.code,
            'name':dept.name,
            'students_paid': students_paid,
            'total_collected': total_paid,
            'faculty_share': total_paid / 2,
            'department_share': total_paid / 2,
            'pending': ending_count,
            'failed': failed_count,
            'semester': semester, 
        }
        department_rows.append(dept_row)
        
        overall['total_collected'] += total_paid
        overall['faculty_share'] += Decimal(total_paid) / 2
        overall['department_share'] += Decimal(total_paid) / 2
        overall['students_paid'] += Decimal(students_paid)
        overall['pending'] += ending_count
        overall['failed'] += failed_count
        
        # ---- Academic years for the dropdown ----
        academic_years = list(
            PaymentTransaction.objects.filter(
                faculty=faculty, payment_type='DUES', academic_year__isnull=False
            ).values_list('academic_year', flat=True).distinct()
        )
        if not academic_years:
            academic_years = ['2026/2027']
            
        context = {
            'faculty': faculty,
            'departments': departments,
            'department_rows': department_rows,
            'academic_years': academic_years,
            
            # Summary for initial server-side render
            'total_collected': overall['total_collected'],
            'faculty_share': overall['faculty_share'],
            'department_share': overall['department_share'],
            'students_paid': overall['students_paid'],
            'pending': overall['pending'],
            'failed': overall['failed'],
            
            # Selected filter values
            'academic_year': academic_year,
            'semester': semester,
            'status': status,
        }

    return render(
        request, "dues_dashboard/faculty_admin/reports.html", context)


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