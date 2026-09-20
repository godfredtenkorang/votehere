from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.dues_login, name="dues_login"),
    path("enter-code/", views.enter_code, name="enter_code"),

    # =====================================================
    # SUPER ADMIN
    #
    # /dues-dashboard/
    # =====================================================

    path(
        "",
        views.super_dashboard,
        name="dashboard"
    ),

    path(
        "payments/",
        views.super_payments,
        name="dues_payments"
    ),

    path(
        "payments/<str:transaction_ref>/",
        views.super_payment_detail,
        name="dues_payment_detail"
    ),

    path(
        "faculties/",
        views.super_faculties,
        name="dues_faculties"
    ),

    path(
        "faculties/<str:faculty_code>/",
        views.super_faculty_detail,
        name="dues_faculty_detail"
    ),

    path(
        "departments/",
        views.super_departments,
        name="dues_departments"
    ),

    path(
        "departments/<str:department_code>/",
        views.super_department_detail,
        name="dues_department_detail"
    ),

    path(
        "students/",
        views.super_students,
        name="dues_students"
    ),

    path(
        "students/<str:student_id>/",
        views.super_student_detail,
        name="dues_student_detail"
    ),

    path(
        "reports/",
        views.super_reports,
        name="dues_reports"
    ),

    path(
        "settings/",
        views.super_settings,
        name="dues_settings"
    ),


    # =====================================================
    # FACULTY ADMIN
    #
    # /dues-dashboard/faculty/
    # =====================================================

    path(
        "faculty/",
        views.faculty_dashboard,
        name="faculty_dashboard"
    ),

    path(
        "faculty/payments/",
        views.faculty_payments,
        name="faculty_payments"
    ),

    path(
        "faculty/students/",
        views.faculty_students,
        name="faculty_students"
    ),

    path(
        "faculty/students/<str:student_id>/",
        views.faculty_student_detail,
        name="faculty_student_detail"
    ),

    path(
        "faculty/reports/",
        views.faculty_reports,
        name="faculty_reports"
    ),

    path(
        "faculty/departments/<str:department_code>/",
        views.faculty_department_detail,
        name="faculty_department_detail"
    ),


    # =====================================================
    # DEPARTMENT ADMIN
    #
    # /dues-dashboard/department/
    # =====================================================

    path(
        "department/",
        views.department_dashboard,
        name="department_dashboard"
    ),

    path(
        "department/payments/",
        views.department_payments,
        name="department_payments"
    ),

    path(
        "department/students/",
        views.department_students,
        name="department_students"
    ),

    path(
        "department/students/<str:student_id>/",
        views.department_student_detail,
        name="department_student_detail"
    ),

    path(
        "department/reports/",
        views.department_reports,
        name="department_reports"
    ),

]