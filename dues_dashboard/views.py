from django.shortcuts import render


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