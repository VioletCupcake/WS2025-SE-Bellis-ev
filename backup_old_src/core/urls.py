"""
URL routing for B-EV case management.

Maps URL patterns to view functions with permission checks.
Uses Django's built-in auth views for login/logout.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import fall_views, beratung_views, gewalttat_views, folgen_views

app_name = 'core'

urlpatterns = [
    # ===== AUTHENTICATION =====
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(
        http_method_names=['get', 'post'],
        next_page='core:login',
        template_name=None
    ), name='logout'),
    
    # ===== CASE MANAGEMENT =====
    path('', fall_views.case_list, name='case_list'),
    path('cases/', fall_views.case_list, name='case_list'),
    path('cases/create/', fall_views.case_create, name='case_create'),
    path('cases/<uuid:fall_id>/', fall_views.case_detail, name='case_detail'),
    path('cases/<uuid:fall_id>/edit/', fall_views.case_edit, name='case_edit'),
    path('cases/<uuid:fall_id>/close/', fall_views.case_close, name='case_close'),
    path('cases/<uuid:fall_id>/delete/', fall_views.case_delete, name='case_delete'),
    
    # ===== BERATUNG (COUNSELING SESSIONS) =====
    path('cases/<uuid:fall_id>/beratung/add/', beratung_views.beratung_add, name='beratung_add'),
    path('beratung/<uuid:beratung_id>/edit/', beratung_views.beratung_edit, name='beratung_edit'),
    path('beratung/<uuid:beratung_id>/delete/', beratung_views.beratung_delete, name='beratung_delete'),
    
    # ===== GEWALTTAT (VIOLENCE INCIDENTS) =====
    path('cases/<uuid:fall_id>/gewalttat/add/', gewalttat_views.gewalttat_add, name='gewalttat_add'),
    path('gewalttat/<uuid:gewalttat_id>/edit/', gewalttat_views.gewalttat_edit, name='gewalttat_edit'),
    path('gewalttat/<uuid:gewalttat_id>/delete/', gewalttat_views.gewalttat_delete, name='gewalttat_delete'),
    
    # ===== FOLGEN DER GEWALT (CONSEQUENCES) =====
    path('cases/<uuid:fall_id>/folgen/add/', folgen_views.folgen_add, name='folgen_add'),
    path('folgen/<int:folgen_id>/edit/', folgen_views.folgen_edit, name='folgen_edit'),
    path('folgen/<int:folgen_id>/delete/', folgen_views.folgen_delete, name='folgen_delete'),
]
