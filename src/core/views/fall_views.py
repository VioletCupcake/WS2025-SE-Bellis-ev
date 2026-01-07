"""
Views for Fall (Case) management.

Handles case listing, creation, editing, and deletion.
Uses FallManager for atomic operations, direct ORM for simple queries.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from core.models import Fall, PersonenbezogeneDaten
from core.forms import FallCreateForm
from core.services.fall_manager import FallManager
from core.decorators import permission_required_custom


@login_required
def case_list(request):
    """
    Display list of all active cases.
    
    Permission: All authenticated users (BASIS, ERWEITERT, ADMIN)
    """
    # Query all active cases, ordered by creation date (newest first)
    cases = Fall.objects.filter(
        status='AKTIV'
    ).select_related(
        'personenbezogene_daten'
    ).order_by('-erstellungsdatum')
    
    # Optional: Search by alias
    search_query = request.GET.get('search', '')
    if search_query:
        cases = cases.filter(
            personenbezogene_daten__alias__icontains=search_query
        )
    
    context = {
        'cases': cases,
        'search_query': search_query,
    }
    return render(request, 'core/case_list.html', context)


@login_required
@permission_required_custom('can_edit_cases')
def case_create(request):
    """
    Create new case (Fall + PersonenbezogeneDaten atomically).
    
    Permission: Users with can_edit_cases permission (BASIS, ERWEITERT, ADMIN)
    Uses FallManager.createFall() for atomic transaction.
    """
    if request.method == 'POST':
        form = FallCreateForm(request.POST)
        
        if form.is_valid():
            try:
                # Extract data for both models
                fall_data = form.get_fall_data()
                personen_data = form.get_personen_data()
                
                # Add bearbeitet_von from request context
                fall_data['bearbeitet_von'] = request.user
                
                # Atomic creation via FallManager
                fall = FallManager.createFall(fall_data, personen_data)
                
                messages.success(
                    request,
                    f'Fall "{fall.personenbezogene_daten.alias}" erfolgreich erstellt.' # type: ignore
                )
                return redirect('core:case_detail', fall_id=fall.fall_id)
                
            except Exception as e:
                messages.error(request, f'Fehler beim Erstellen: {str(e)}')
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler im Formular.')
    else:
        form = FallCreateForm()
    
    context = {
        'form': form,
        'action': 'Erstellen',
    }
    return render(request, 'core/case_form.html', context)


@login_required
def case_detail(request, fall_id):
    """
    Display case details with related Beratungen and Gewalttaten.
    
    Permission: All authenticated users (view access)
    """
    fall = get_object_or_404(
        Fall.objects.select_related(
            'personenbezogene_daten',
            'bearbeitet_von'
        ).prefetch_related(
            'beratungen',
            'gewalttaten__gewalttat_arten'
        ),
        fall_id=fall_id
    )
    
    context = {
        'fall': fall,
        'personenbezogene_daten': fall.personenbezogene_daten, # type: ignore
        'beratungen': fall.beratungen.all().order_by('-datum'), # type: ignore
        'gewalttaten': fall.gewalttaten.all(), # type: ignore
    }
    return render(request, 'core/case_detail.html', context)


@login_required
@permission_required_custom('can_edit_cases')
def case_edit(request, fall_id):
    """
    Edit existing case.
    
    Permission: Users with can_edit_cases permission
    Note: For MVP, only Fall fields editable (not PersonenbezogeneDaten)
    """
    fall = get_object_or_404(Fall, fall_id=fall_id)
    
    if request.method == 'POST':
        # For MVP: Simple field updates via direct ORM
        # Post-MVP: Use dedicated edit form
        fall.informationsquelle = request.POST.get('informationsquelle', fall.informationsquelle)
        fall.weitere_notizen = request.POST.get('weitere_notizen', fall.weitere_notizen)
        fall.bearbeitet_von = request.user
        fall.save(update_fields=['informationsquelle', 'weitere_notizen', 'bearbeitet_von', 'letzte_bearbeitung'])
        
        messages.success(request, f'Fall "{fall}" aktualisiert.')
        return redirect('core:case_detail', fall_id=fall.fall_id)
    
    context = {
        'fall': fall,
    }
    return render(request, 'core/case_edit.html', context)


@login_required
@permission_required_custom('can_edit_cases')
def case_close(request, fall_id):
    """
    Close case (set ist_abgeschlossen=True).
    
    Permission: Users with can_edit_cases permission
    """
    fall = get_object_or_404(Fall, fall_id=fall_id)
    
    if request.method == 'POST':
        fall.close()  # Model method sets ist_abgeschlossen + abschlussdatum
        fall.bearbeitet_von = request.user
        fall.save(update_fields=['bearbeitet_von', 'letzte_bearbeitung'])
        
        messages.success(request, f'Fall "{fall}" abgeschlossen.')
        return redirect('core:case_detail', fall_id=fall.fall_id)
    
    context = {
        'fall': fall,
    }
    return render(request, 'core/case_close_confirm.html', context)


@login_required
def case_delete(request, fall_id):
    """
    Delete case (soft or hard depending on permissions).
    
    Permission: 
    - Soft delete (archive): can_delete_cases (ERWEITERT, ADMIN)
    - Hard delete: can_hard_delete_cases (ADMIN only)
    """
    fall = get_object_or_404(Fall, fall_id=fall_id)
    
    # Check permissions via custom PermissionSet
    user = request.user
    
    # Ensure user has role and permissions
    if not user.role or not user.role.permissions:
        raise PermissionDenied("Benutzer hat keine Berechtigungen konfiguriert.")
    
    can_soft_delete = user.role.permissions.can_delete_cases
    can_hard_delete = user.role.permissions.can_hard_delete_cases
    
    if not (can_soft_delete or can_hard_delete):
        raise PermissionDenied("Keine Berechtigung zum Löschen von Fällen.")
    
    if request.method == 'POST':
        delete_type = request.POST.get('delete_type', 'soft')
        
        if delete_type == 'hard' and can_hard_delete:
            # Hard delete via FallManager (checks permissions again)
            alias = str(fall.personenbezogene_daten.alias) # type: ignore
            FallManager.hardDeleteFall(fall.fall_id, user)
            messages.success(request, f'Fall "{alias}" permanent gelöscht.')
            return redirect('core:case_list')
            
        elif delete_type == 'soft' and can_soft_delete:
            # Soft delete (archive)
            fall.archive()
            messages.success(request, f'Fall "{fall}" archiviert.')
            return redirect('core:case_list')
        else:
            messages.error(request, 'Ungültige Löschoption oder fehlende Berechtigung.')
    
    context = {
        'fall': fall,
        'can_soft_delete': can_soft_delete,
        'can_hard_delete': can_hard_delete,
    }
    return render(request, 'core/case_delete_confirm.html', context)
