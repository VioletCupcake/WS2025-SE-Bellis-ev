"""
Views for Beratung (Counseling Session) management.

Simple CRUD operations using direct ORM.
Automatically updates Fall aggregate counters via model save() override.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import Fall, Beratung
from core.forms import BeratungForm
from core.decorators import permission_required_custom


@login_required
@permission_required_custom('can_edit_cases')
def beratung_add(request, fall_id):
    """
    Add counseling session to existing case.
    
    Permission: Users with can_edit_cases permission
    Automatically updates Fall.beratungsanzahl and Fall.letzte_beratung.
    """
    fall = get_object_or_404(Fall, fall_id=fall_id)
    
    if request.method == 'POST':
        form = BeratungForm(request.POST, fall=fall)
        
        if form.is_valid():
            beratung = form.save()  # Triggers Fall aggregate updates
            
            messages.success(
                request,
                f'Beratung vom {beratung.datum} für Fall "{fall}" hinzugefügt.'
            )
            return redirect('core:case_detail', fall_id=fall.fall_id)
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler im Formular.')
    else:
        form = BeratungForm(fall=fall)
    
    context = {
        'form': form,
        'fall': fall,
        'action': 'Hinzufügen',
    }
    return render(request, 'core/beratung_form.html', context)


@login_required
@permission_required_custom('can_edit_cases')
def beratung_edit(request, beratung_id):
    """
    Edit existing counseling session.
    
    Permission: Users with can_edit_cases permission
    """
    beratung = get_object_or_404(
        Beratung.objects.select_related('fall'),
        beratung_id=beratung_id
    )
    fall = beratung.fall
    
    if request.method == 'POST':
        form = BeratungForm(request.POST, instance=beratung, fall=fall)
        
        if form.is_valid():
            form.save()  # Updates Fall.letzte_beratung if datum changed
            
            messages.success(request, f'Beratung vom {beratung.datum} aktualisiert.')
            return redirect('core:case_detail', fall_id=fall.fall_id)
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler im Formular.')
    else:
        form = BeratungForm(instance=beratung, fall=fall)
    
    context = {
        'form': form,
        'fall': fall,
        'beratung': beratung,
        'action': 'Bearbeiten',
    }
    return render(request, 'core/beratung_form.html', context)


@login_required
@permission_required_custom('can_delete_cases')
def beratung_delete(request, beratung_id):
    """
    Delete counseling session.
    
    Permission: Users with can_delete_cases permission (soft delete permission applies)
    Automatically updates Fall aggregate counters via model delete() override.
    """
    beratung = get_object_or_404(
        Beratung.objects.select_related('fall'),
        beratung_id=beratung_id
    )
    fall = beratung.fall
    
    if request.method == 'POST':
        datum = beratung.datum
        beratung.delete()  # Triggers Fall aggregate recalculation
        
        messages.success(request, f'Beratung vom {datum} gelöscht.')
        return redirect('core:case_detail', fall_id=fall.fall_id)
    
    context = {
        'beratung': beratung,
        'fall': fall,
    }
    return render(request, 'core/beratung_delete_confirm.html', context)
