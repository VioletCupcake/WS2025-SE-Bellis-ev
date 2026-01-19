"""
Views for FolgenDerGewalt (Consequences of Violence) management.

Handles adding, editing, and removing consequence links to cases.
Uses Fall_FolgenDerGewalt junction table for many-to-many relationships.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import Fall, Fall_FolgenDerGewalt
from core.forms import FolgenDerGewaltForm
from core.decorators import permission_required_custom


@login_required
@permission_required_custom('can_edit_cases')
def folgen_add(request, fall_id):
    """
    Add consequence to existing case.
    
    Permission: Users with can_edit_cases permission
    Creates a new Fall_FolgenDerGewalt junction entry.
    Supports "Save & Add Another" for efficient bulk entry
    """
    fall = get_object_or_404(Fall, fall_id=fall_id)
    
    if request.method == 'POST':
        form = FolgenDerGewaltForm(request.POST, fall=fall)
        
        if form.is_valid():
            folgen_relation = form.save()
            
            messages.success(
                request,
                f'Folge "{folgen_relation.folge.name}" für Fall "{fall}" hinzugefügt.'
            )
            
            # check if user wants to add another one - saves a lot of clicking
            if request.POST.get('action') == 'add_another':
                return redirect('core:folgen_add', fall_id=fall.fall_id)
            
            return redirect('core:case_detail', fall_id=fall.fall_id)
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler im Formular.')
    else:
        form = FolgenDerGewaltForm(fall=fall)
    
    # Check if there are any available consequences to add
    available_count = form.fields['folge'].queryset.count()  # type: ignore[union-attr]
    
    context = {
        'form': form,
        'fall': fall,
        'action': 'Hinzufügen',
        'no_available_folgen': available_count == 0,
    }
    return render(request, 'core/folgen_form.html', context)


@login_required
@permission_required_custom('can_edit_cases')
def folgen_edit(request, folgen_id):
    """
    Edit existing consequence link (mainly the weitere_informationen field).
    
    Permission: Users with can_edit_cases permission
    """
    folgen_relation = get_object_or_404(
        Fall_FolgenDerGewalt.objects.select_related('fall', 'folge'),
        id=folgen_id
    )
    fall = folgen_relation.fall
    
    if request.method == 'POST':
        form = FolgenDerGewaltForm(request.POST, instance=folgen_relation, fall=fall)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, f'Folge für Fall "{fall}" aktualisiert.')
            return redirect('core:case_detail', fall_id=fall.fall_id)
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler im Formular.')
    else:
        form = FolgenDerGewaltForm(instance=folgen_relation, fall=fall)
    
    context = {
        'form': form,
        'fall': fall,
        'folgen_relation': folgen_relation,
        'action': 'Bearbeiten',
    }
    return render(request, 'core/folgen_form.html', context)


@login_required
@permission_required_custom('can_delete_cases')
def folgen_delete(request, folgen_id):
    """
    Remove consequence link from case.
    
    Permission: Users with can_delete_cases permission
    Deletes the Fall_FolgenDerGewalt junction entry (not the FolgenDerGewalt itself).
    """
    folgen_relation = get_object_or_404(
        Fall_FolgenDerGewalt.objects.select_related('fall', 'folge'),
        id=folgen_id
    )
    fall = folgen_relation.fall
    folge_name = folgen_relation.folge.name
    
    if request.method == 'POST':
        folgen_relation.delete()
        
        messages.success(request, f'Folge "{folge_name}" von Fall "{fall}" entfernt.')
        return redirect('core:case_detail', fall_id=fall.fall_id)
    
    context = {
        'folgen_relation': folgen_relation,
        'fall': fall,
    }
    return render(request, 'core/folgen_delete_confirm.html', context)
