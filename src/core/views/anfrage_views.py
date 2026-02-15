"""
Views for Anfrage (Inquiry) management.

Handles inquiry listing, creation, editing, and deletion
with soft validation warnings and date-based search.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import Anfrage
from core.forms import AnfrageCreateForm, AnfrageEditForm
from core.decorators import permission_required_custom


@login_required
def anfrage_list(request):
    """
    Display list of all inquiries with optional date and text search.
    
    Permission: All authenticated users
    
    GET parameters:
        search: text filter on art_der_anfrage / anfrage_aus
        datum: date filter on datum_anfrage (YYYY-MM-DD)
    """
    # Query all inquiries ordered by date (newest first)
    anfragen = Anfrage.objects.all().select_related(
        'bearbeitet_von'
    ).order_by('-datum_anfrage')
    
    # Date-based search
    datum_filter = request.GET.get('datum', '')
    if datum_filter:
        anfragen = anfragen.filter(datum_anfrage=datum_filter)
    
    # Text-based search
    search_query = request.GET.get('search', '')
    if search_query:
        anfragen = anfragen.filter(
            art_der_anfrage__icontains=search_query
        ) | anfragen.filter(
            anfrage_aus__icontains=search_query
        )
    
    context = {
        'anfragen': anfragen,
        'search_query': search_query,
        'datum_filter': datum_filter,
    }
    return render(request, 'core/anfrage_list.html', context)


@login_required
@permission_required_custom('can_edit_cases')
def anfrage_create(request):
    """
    Create new inquiry with soft validation.
    
    Permission: Users with can_edit_cases permission
    
    Workflow:
    1. User submits form
    2. If incomplete and not force_save, show warning with incomplete fields
    3. User can choose "Felder anpassen" (return to form) or "Trotzdem speichern" (force save)
    4. On force_save or complete form, save and redirect to list
    """
    # Check if this is a force save (user confirmed saving incomplete data)
    force_save = request.POST.get('force_save') == 'true'
    
    if request.method == 'POST':
        form = AnfrageCreateForm(request.POST)
        
        if form.is_valid():
            # Check for incomplete fields (soft validation)
            incomplete_fields = form.get_incomplete_fields()
            
            if incomplete_fields and not force_save:
                # Show warning dialog with incomplete fields
                context = {
                    'form': form,
                    'action': 'Erstellen',
                    'show_warning': True,
                    'incomplete_fields': incomplete_fields,
                }
                return render(request, 'core/anfrage_form.html', context)
            
            try:
                # Get form data
                anfrage_data = form.get_anfrage_data()
                
                # Add user from request context
                anfrage_data['bearbeitet_von'] = request.user
                
                # Create the Anfrage record
                anfrage = Anfrage.objects.create(**anfrage_data)
                
                messages.success(
                    request,
                    f'Anfrage vom {anfrage.datum_anfrage} erfolgreich gespeichert.'
                )
                return redirect('core:anfrage_list')
                
            except Exception as e:
                messages.error(request, f'Fehler beim Speichern: {str(e)}')
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler im Formular.')
    else:
        form = AnfrageCreateForm()
    
    context = {
        'form': form,
        'action': 'Erstellen',
        'show_warning': False,
        'incomplete_fields': [],
    }
    return render(request, 'core/anfrage_form.html', context)


@login_required
@permission_required_custom('can_edit_cases')
def anfrage_edit(request, anfrage_id):
    """
    Edit an existing inquiry with soft validation.
    
    Permission: Users with can_edit_cases permission
    """
    anfrage = get_object_or_404(Anfrage, anfrage_id=anfrage_id)
    
    force_save = request.POST.get('force_save') == 'true'
    
    if request.method == 'POST':
        form = AnfrageEditForm(request.POST, instance=anfrage)
        
        if form.is_valid():
            incomplete_fields = form.get_incomplete_fields()
            
            if incomplete_fields and not force_save:
                context = {
                    'form': form,
                    'anfrage': anfrage,
                    'action': 'Bearbeiten',
                    'show_warning': True,
                    'incomplete_fields': incomplete_fields,
                }
                return render(request, 'core/anfrage_form.html', context)
            
            try:
                form.save(user=request.user)
                
                messages.success(
                    request,
                    f'Anfrage vom {anfrage.datum_anfrage} erfolgreich aktualisiert.'
                )
                return redirect('core:anfrage_list')
                
            except Exception as e:
                messages.error(request, f'Fehler beim Speichern: {str(e)}')
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler im Formular.')
    else:
        form = AnfrageEditForm(instance=anfrage)
    
    context = {
        'form': form,
        'anfrage': anfrage,
        'action': 'Bearbeiten',
        'show_warning': False,
        'incomplete_fields': [],
    }
    return render(request, 'core/anfrage_form.html', context)


@login_required
@permission_required_custom('can_delete_cases')
def anfrage_delete(request, anfrage_id):
    """
    Delete an inquiry after confirmation.
    
    Permission: Users with can_delete_cases permission
    """
    anfrage = get_object_or_404(Anfrage, anfrage_id=anfrage_id)
    
    if request.method == 'POST':
        datum = anfrage.datum_anfrage
        anfrage.delete()
        
        messages.success(request, f'Anfrage vom {datum} gelöscht.')
        return redirect('core:anfrage_list')
    
    context = {
        'anfrage': anfrage,
    }
    return render(request, 'core/anfrage_delete_confirm.html', context)
