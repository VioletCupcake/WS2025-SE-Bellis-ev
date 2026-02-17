
"""
Views for Statistics feature.
"""
import json
import csv
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from django.conf import settings
from reportlab.pdfgen import canvas
from openpyxl import Workbook

from core.models import (
    Fall, PersonenbezogeneDaten, Beratung, Gewalttat, Anfrage,
    StatistikPreset, Role, GewalttatArt, FolgenDerGewalt
)
from core.decorators import permission_required_custom

# --- HELPER FUNCTIONS ---

def get_filtered_queryset(filter_config):
    """
    Returns filtered Fall queryset based on config.
    """
    qs = Fall.objects.all()
    
    # Date filter (erstellungsdatum)
    date_from = filter_config.get('date_from')
    date_to = filter_config.get('date_to')
    
    if date_from:
        qs = qs.filter(erstellungsdatum__gte=date_from)
    if date_to:
        qs = qs.filter(erstellungsdatum__lte=date_to)
        
    # Beratungsstelle filter
    beratungsstellen = filter_config.get('beratungsstellen', [])
    if beratungsstellen:
        qs = qs.filter(zustaendige_beratungsstelle__in=beratungsstellen)
        
    # Exclude archived/deleted if not requested (usually we want active cases)
    # But for stats, maybe we want all? Let's default to all non-hard-deleted (so all in DB)
    return qs

def calculate_stats(qs, modules, date_from=None, date_to=None):
    """
    Calculates statistics based on filtered queryset and selected modules.
    qs: Filtered Fall queryset
    modules: List of selected module keys
    """
    stats = {}
    
    # 1. Personenbezogene Daten
    if 'personen' in modules:
        # We need related PersonenbezogeneDaten
        p_qs = PersonenbezogeneDaten.objects.filter(fall__in=qs)
        
        stats['personen'] = {
            'total': p_qs.count(),
            'rolle': list(p_qs.values('rolle_der_ratsuchenden_person').annotate(count=Count('rolle_der_ratsuchenden_person'))),
            'geschlecht': list(p_qs.values('geschlechtsidentitaet').annotate(count=Count('geschlechtsidentitaet'))),
            'wohnort': list(p_qs.values('wohnort').annotate(count=Count('wohnort'))),
            'altersgruppen': {
                'unter_18': p_qs.filter(alter__lt=18).count(),
                '18_27': p_qs.filter(alter__gte=18, alter__lte=27).count(),
                'ueber_27': p_qs.filter(alter__gt=27).count(),
                'unbekannt': p_qs.filter(alter__isnull=True).count(),
            }
        }

    # 2. Beratungen
    if 'beratung' in modules:
        # Filter Beratungen by date if provided, or use Fall filter
        b_qs = Beratung.objects.filter(fall__in=qs)
        if date_from:
            b_qs = b_qs.filter(datum__gte=date_from)
        if date_to:
            b_qs = b_qs.filter(datum__lte=date_to)
            
        stats['beratung'] = {
            'total_termine': b_qs.count(),
            'durchfuehrungsart': list(b_qs.values('durchfuehrungsart').annotate(count=Count('durchfuehrungsart'))),
            'durchfuehrungsort': list(b_qs.values('durchfuehrungsort').annotate(count=Count('durchfuehrungsort'))),
        }

    # 3. Gewalttaten
    if 'gewalttat' in modules:
        g_qs = Gewalttat.objects.filter(fall__in=qs)
        # Note: Gewalttat date filter logic could be complex (Zeitraum), here we rely on Fall filter
        
        stats['gewalttat'] = {
            'total': g_qs.count(),
            'tatort': list(g_qs.values('tatort').annotate(count=Count('tatort'))),
            'anzeige': list(g_qs.values('anzeige').annotate(count=Count('anzeige'))),
            'medizinische_versorgung': list(g_qs.values('medizinische_versorgung').annotate(count=Count('medizinische_versorgung'))),
        }

    # 4. Folgen
    if 'folgen' in modules:
        # Need to join via Fall_FolgenDerGewalt
        from core.models import Fall_FolgenDerGewalt
        f_qs = Fall_FolgenDerGewalt.objects.filter(fall__in=qs)
        
        stats['folgen'] = {
            'kategorien': list(f_qs.values('folge__kategorie').annotate(count=Count('folge__kategorie'))),
            'top_folgen': list(f_qs.values('folge__name').annotate(count=Count('folge__name')).order_by('-count')[:10]),
        }

    # 5. Anfragen (Independent of Fall, so we query directly but match filters)
    if 'anfragen' in modules:
        a_qs = Anfrage.objects.all()
        if date_from:
            a_qs = a_qs.filter(datum_anfrage__gte=date_from)
        if date_to:
            a_qs = a_qs.filter(datum_anfrage__lte=date_to)
        
        # beratungsstelle filter for Anfragen?
        # Anfrage has no direct 'beratungsstelle' field, but maybe 'anfrage_aus' maps somewhat?
        # Or maybe check 'bearbeitet_von' role? 
        # For now, we apply date filter only, as requested in spec "wie viele Beratungstermine insgesamt" etc.
        # But user might expect filters to apply.
        # Given matching field names are different, we'll just return general stats for now or map regions if possible.
        # Simple approach: Return all matching date range.
        
        stats['anfragen'] = {
            'total': a_qs.count(),
            'kontaktweg': list(a_qs.values('wie').annotate(count=Count('wie'))),
            'herkunft': list(a_qs.values('anfrage_aus').annotate(count=Count('anfrage_aus'))),
            'art': list(a_qs.values('art_der_anfrage').annotate(count=Count('art_der_anfrage'))),
        }

    return stats

# --- VIEWS ---

@login_required
def statistics_ui(request):
    """
    Main dashboard for statistics.
    """
    # Create default empty config
    filter_config = {
        'date_from': '',
        'date_to': '',
        'beratungsstellen': [],
        'modules': ['personen', 'beratung', 'gewalttat', 'folgen', 'anfragen'] # Default all
    }
    
    # If POST (Apply Filter), update config
    if request.method == 'POST':
        filter_config['date_from'] = request.POST.get('date_from', '')
        filter_config['date_to'] = request.POST.get('date_to', '')
        filter_config['beratungsstellen'] = request.POST.getlist('beratungsstellen')
        filter_config['modules'] = request.POST.getlist('modules')
        
    # If loading preset (GET param)
    preset_id = request.GET.get('load_preset')
    if preset_id:
        preset = get_object_or_404(StatistikPreset, pk=preset_id)
        # Check permissions? System presets or own presets
        filter_config = preset.filter_config
    
    # Store config in session for export
    request.session['stats_filter_config'] = filter_config
    
    # Calculate Results
    qs = get_filtered_queryset(filter_config)
    results = calculate_stats(
        qs, 
        filter_config.get('modules', []),
        date_from=filter_config.get('date_from'),
        date_to=filter_config.get('date_to')
    )
    
    # Load available presets
    user_presets = StatistikPreset.objects.filter(erstellt_von=request.user)
    global_presets = StatistikPreset.objects.filter(Q(ist_global=True) | Q(ist_system_preset=True)).exclude(erstellt_von=request.user)
    
    context = {
        'results': results,
        'config': filter_config,
        'user_presets': user_presets,
        'global_presets': global_presets,
        'beratungsstellen_choices': Fall.BERATUNGSSTELLE_CHOICES,
    }
    return render(request, 'core/statistik_dashboard.html', context)


@login_required
def preset_save(request):
    """
    Save current filter config as new preset.
    """
    if request.method == 'POST':
        name = request.POST.get('preset_name')
        is_global = request.POST.get('is_global') == 'on'
        
        # Get config from session or reconstruct
        # Better to get from form hidden fields or session
        config = request.session.get('stats_filter_config', {})
        
        preset = StatistikPreset.objects.create(
            name=name,
            filter_config=config,
            erstellt_von=request.user,
            ist_global=is_global
        )
        # Redirect back to dashboard
        return redirect('core:statistics_ui')
    return redirect('core:statistics_ui')

@login_required
def preset_delete(request, preset_id):
    """
    Delete a preset.
    """
    preset = get_object_or_404(StatistikPreset, pk=preset_id)
    if preset.erstellt_von == request.user and not preset.ist_system_preset:
        preset.delete()
    return redirect('core:statistics_ui')


@login_required
def statistics_export(request, format_type):
    """
    Export stats to PDF, XLSX, CSV.
    """
    config = request.session.get('stats_filter_config', {})
    qs = get_filtered_queryset(config)
    stats = calculate_stats(
        qs, 
        config.get('modules', []),
        date_from=config.get('date_from'),
        date_to=config.get('date_to')
    )
    
    filename = f"statistik_{datetime.now().strftime('%Y%m%d')}"
    
    if format_type == 'json':
        return JsonResponse(stats)
        
    elif format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Kategorie', 'Merkmal', 'Wert'])
        
        # Flatten stats dict for CSV
        for category, data in stats.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        for item in value:
                            # Try to find count in dict
                            count = item.get('count', 0)
                            label = list(item.values())[0] # First value usually label
                            writer.writerow([category, f"{key}: {label}", count])
                    elif isinstance(value, dict):
                         for subkey, subval in value.items():
                             writer.writerow([category, f"{key}: {subkey}", subval])
                    else:
                        writer.writerow([category, key, value])
                        
        return response

    elif format_type == 'xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Statistik"
        ws.append(['Kategorie', 'Merkmal', 'Wert'])
        
        for category, data in stats.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        for item in value:
                            count = item.get('count', 0)
                            # extract label carefully
                            # item is like {'rolle_der_ratsuchenden_person': 'BETROFFENE', 'count': 5}
                            # we want keys that are NOT count
                            labels = [v for k,v in item.items() if k != 'count']
                            label = labels[0] if labels else 'N/A'
                            ws.append([category, f"{key}: {label}", count])
                    elif isinstance(value, dict):
                         for subkey, subval in value.items():
                             ws.append([category, f"{key}: {subkey}", subval])
                    else:
                        ws.append([category, key, value])
        
        wb.save(response)
        return response

    elif format_type == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
        
        p = canvas.Canvas(response)
        y = 800
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, y, "Statistik Report")
        y -= 30
        p.setFont("Helvetica", 12)
        p.drawString(100, y, f"Generiert am: {datetime.now().strftime('%d.%m.%Y')}")
        y -= 20
        
        p.drawString(100, y, f"Filter: {config.get('date_from', '')} - {config.get('date_to', '')}")
        y -= 40
        
        for category, data in stats.items():
            if y < 100:
                p.showPage()
                y = 800
                
            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, y, category.upper())
            y -= 20
            p.setFont("Helvetica", 10)
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if y < 50:
                        p.showPage()
                        y = 800
                        
                    if isinstance(value, list):
                        p.drawString(120, y, f"{key}:")
                        y -= 15
                        for item in value:
                            count = item.get('count', 0)
                            labels = [v for k,v in item.items() if k != 'count']
                            label = labels[0] if labels else 'N/A'
                            p.drawString(140, y, f"- {label}: {count}")
                            y -= 15
                    elif isinstance(value, dict):
                        p.drawString(120, y, f"{key}:")
                        y -= 15
                        for subkey, subval in value.items():
                            p.drawString(140, y, f"- {subkey}: {subval}")
                            y -= 15
                    else:
                        p.drawString(120, y, f"{key}: {value}")
                        y -= 15
            y -= 20
            
        p.showPage()
        p.save()
        return response

    return HttpResponse("Unknown format", status=400)
