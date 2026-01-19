"""
Views for Gewalttat (Violence Incident) management.

Handles complex form with M2M relationships and JSON validation.
Uses direct ORM — no manager needed.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import Fall, Gewalttat
from core.forms import GewalttatForm
from core.decorators import permission_required_custom


@login_required
@permission_required_custom('can_edit_cases')
def gewalttat_add(request, fall_id):
    """
    Add violence incident to existing case.
    
    Permission: Users with can_edit_cases permission
    Handles M2M relationship with GewalttatArt and JSON perpetrator details.
    """
    fall = get_object_or_404(Fall, fall_id=fall_id)
    
    if request.method == 'POST':
        form = GewalttatForm(request.POST, fall=fall)
        
        if form.is_valid():
            gewalttat = form.save()  # Saves instance + M2M relationships
            
            # Count of selected violence types
            arten_count = gewalttat.gewalttat_arten.count()
            
            messages.success(
                request,
                f'Gewalttat für Fall "{fall}" hinzugefügt ({arten_count} Gewaltarten ausgewählt).'
            )
            return redirect('core:case_detail', fall_id=fall.fall_id)
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler im Formular.')
    else:
        form = GewalttatForm(fall=fall)
    
    context = {
        'form': form,
        'fall': fall,
        'action': 'Hinzufügen',
    }
    return render(request, 'core/gewalttat_form.html', context)


@login_required
@permission_required_custom('can_edit_cases')
def gewalttat_edit(request, gewalttat_id):
    """
    Edit existing violence incident.
    
    Permission: Users with can_edit_cases permission
    """
    gewalttat = get_object_or_404(
        Gewalttat.objects.select_related('fall').prefetch_related('gewalttat_arten'),
        gewalttat_id=gewalttat_id
    )
    fall = gewalttat.fall
    
    if request.method == 'POST':
        form = GewalttatForm(request.POST, instance=gewalttat, fall=fall)
        
        if form.is_valid():
            form.save()  # Updates instance + M2M relationships
            
            messages.success(request, f'Gewalttat für Fall "{fall}" aktualisiert.')
            return redirect('core:case_detail', fall_id=fall.fall_id)
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler im Formular.')
    else:
        # Pre-populate form with existing data including M2M selections
        form = GewalttatForm(instance=gewalttat, fall=fall)
    
    context = {
        'form': form,
        'fall': fall,
        'gewalttat': gewalttat,
        'action': 'Bearbeiten',
    }
    return render(request, 'core/gewalttat_form.html', context)


@login_required
@permission_required_custom('can_delete_cases')
def gewalttat_delete(request, gewalttat_id):
    """
    Delete violence incident.
    
    Permission: Users with can_delete_cases permission
    CASCADE deletes junction table entries (Gewalttat_GewalttatArt).
    """
    gewalttat = get_object_or_404(
        Gewalttat.objects.select_related('fall'),
        gewalttat_id=gewalttat_id
    )
    fall = gewalttat.fall
    
    if request.method == 'POST':
        gewalttat.delete()  # CASCADE removes M2M junction rows automatically
        
        messages.success(request, f'Gewalttat für Fall "{fall}" gelöscht.')
        return redirect('core:case_detail', fall_id=fall.fall_id)
    
    context = {
        'gewalttat': gewalttat,
        'fall': fall,
    }
    return render(request, 'core/gewalttat_delete_confirm.html', context)
