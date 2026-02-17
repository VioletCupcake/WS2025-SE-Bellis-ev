"""
URL routing for the Bellis REST API.
All paths are prefixed with /api/ (configured in B_EV/urls.py).
"""
from django.urls import path
from . import views

urlpatterns = [
    # Fall (Case)
    path('cases/', views.FallListView.as_view(), name='api-fall-list'),
    path('fall/create/', views.FallCreateView.as_view(), name='api-fall-create'),
    path('fall/<uuid:fall_id>/', views.FallDetailView.as_view(), name='api-fall-detail'),

    # Folgen der Gewalt (Consequences)
    path('folgen/', views.FolgenListView.as_view(), name='api-folgen-list'),
    path('fall/<uuid:fall_id>/folge/', views.FallFolgeCreateView.as_view(), name='api-fall-folge-create'),

    # Beratung (Consultation)
    path('beratung/create/', views.BeratungCreateView.as_view(), name='api-beratung-create'),
    path('beratungen/<uuid:beratung_id>/', views.BeratungDeleteView.as_view(), name='api-beratung-delete'),

    # Anfrage (Inquiry)
    path('anfragen/', views.AnfrageCreateView.as_view(), name='api-anfrage-create'),
]
