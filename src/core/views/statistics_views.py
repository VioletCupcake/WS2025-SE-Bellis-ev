"""
Template-based UI integration for statistics.

Provides a simple page where staff can:
- wählen: Zeitraum, Filter, Module
- Presets laden/speichern
- Ergebnisse anzeigen und exportieren (CSV/XLSX/PDF)

Die eigentliche Berechnung erfolgt über core.services.statistics_service
und die REST-API steht zusätzlich für ein mögliches JS-Frontend zur Verfügung.
"""

from __future__ import annotations

import json
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from core.models import StatsPreset
from core.services.statistics_service import stats_meta, compute_statistics
from core.decorators import permission_required_custom


def _default_period() -> tuple[date, date]:
    today = date.today()
    # Default: letzte 6 Monate
    six_months_ago = today - timedelta(days=180)
    return six_months_ago, today


@login_required
@permission_required_custom("can_view_cases")
def statistics_ui(request: HttpRequest) -> HttpResponse:
    """
    Einfache Statistik-Übersichtsseite.

    - GET ohne Parameter: zeigt leere Ansicht mit Default-Zeitraum + Meta-Infos + Presets
    - GET mit ?preset=<uuid>: wendet Preset-Payload als initiale Filter/Module an
    - POST: führt Berechnung mit gewählten Filtern/Modulen aus (Server-seitig)
    """
    meta = stats_meta()
    user = request.user

    # Sichtbare Presets: globale + persönliche des Users
    presets = StatsPreset.objects.filter(scope="GLOBAL").filter(owner__isnull=True).order_by("name") | StatsPreset.objects.filter(scope="PERSONAL", owner=user).order_by("name")

    date_from, date_to = _default_period()
    current_filters: dict = {}
    current_modules: list[dict] = []
    current_preset: StatsPreset | None = None
    result: dict | None = None

    # Falls ein Preset geladen wird
    preset_id = request.GET.get("preset")
    if preset_id:
        try:
            current_preset = get_object_or_404(
                StatsPreset,
                preset_id=preset_id,
            )
            payload = current_preset.payload or {}
            current_filters = payload.get("filters", {})
            current_modules = payload.get("modules", [])
        except Exception:
            messages.error(request, "Ausgewähltes Preset konnte nicht geladen werden.")

    # POST: Auswertung
    if request.method == "POST":
        try:
            date_from_str = request.POST.get("date_from", "")
            date_to_str = request.POST.get("date_to", "")
            if date_from_str:
                date_from = date.fromisoformat(date_from_str)
            if date_to_str:
                date_to = date.fromisoformat(date_to_str)
        except ValueError:
            messages.error(request, "Ungültiges Datumsformat. Bitte yyyy-mm-dd verwenden.")
            return redirect("core:statistics_ui")

        # Filter + Module kommen als JSON aus Hidden Fields
        try:
            current_filters = json.loads(request.POST.get("filters_json") or "{}")
        except json.JSONDecodeError:
            current_filters = {}
        try:
            current_modules = json.loads(request.POST.get("modules_json") or "[]")
        except json.JSONDecodeError:
            current_modules = []

        if not current_modules:
            messages.warning(request, "Bitte mindestens ein Statistik-Modul auswählen.")
        else:
            result = compute_statistics(
                date_from=date_from,
                date_to=date_to,
                filters=current_filters,
                modules=current_modules,
            )

    context = {
        "meta": meta,
        "presets": presets,
        "current_preset": current_preset,
        "date_from": date_from,
        "date_to": date_to,
        "current_filters_json": json.dumps(current_filters),
        "current_modules_json": json.dumps(current_modules),
        "result": result,
    }
    return render(request, "core/statistics.html", context)

