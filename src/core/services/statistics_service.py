"""
Statistics computation service.

Implements modular, filterable statistics for staff.
Designed to be consumed by the REST API endpoints in core/api.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Iterable

from django.db.models import Count, QuerySet
from django.db.models.functions import Coalesce
from django.db.models import Value, CharField

from core.models import (
    Fall,
    Beratung,
    Anfrage,
    PersonenbezogeneDaten,
    CaseSurveyAnswer,
    CaseSurveyQuestion,
)


def _choices_to_label_map(choices: Iterable[tuple[Any, Any]]) -> dict[str, str]:
    return {str(k): str(v) for k, v in choices}


CHOICE_LABELS: dict[str, dict[str, str]] = {
    "fall.zustaendige_beratungsstelle": _choices_to_label_map(Fall.BERATUNGSSTELLE_CHOICES),
    "person.wohnort": _choices_to_label_map(PersonenbezogeneDaten.WOHNORT_CHOICES),
    "person.staatsangehoerigkeit_deutsch": _choices_to_label_map(PersonenbezogeneDaten.STAATSANGEHOERIGKEIT_CHOICES),
    "person.rolle_der_ratsuchenden_person": _choices_to_label_map(PersonenbezogeneDaten.ROLLE_CHOICES),
    "person.geschlechtsidentitaet": _choices_to_label_map(PersonenbezogeneDaten.GESCHLECHT_CHOICES),
    "person.sexualitaet": _choices_to_label_map(PersonenbezogeneDaten.SEXUALITAET_CHOICES),
    "person.berufliche_situation": _choices_to_label_map(PersonenbezogeneDaten.BERUF_CHOICES),
    "person.schwerbehinderung": _choices_to_label_map(PersonenbezogeneDaten.SCHWERBEHINDERUNG_CHOICES),
    "beratung.durchfuehrungsart": _choices_to_label_map(Beratung.DURCHFUEHRUNGSART_CHOICES),
    "beratung.durchfuehrungsort": _choices_to_label_map(Beratung.ORT_CHOICES),
    "anfrage.anfrage_aus": _choices_to_label_map(Anfrage.ANFRAGE_AUS_CHOICES),
}


@dataclass(frozen=True)
class Bucket:
    key: str
    label: str
    count: int


def _bucketize(
    *,
    rows: list[dict[str, Any]],
    value_key: str,
    count_key: str,
    label_map: dict[str, str] | None = None,
) -> list[Bucket]:
    buckets: list[Bucket] = []
    for r in rows:
        raw = r.get(value_key)
        key = "" if raw is None else str(raw)
        label = (label_map or {}).get(key, key if key else "—")
        buckets.append(Bucket(key=key, label=label, count=int(r[count_key] or 0)))
    return buckets


def _apply_fall_filters(falls: QuerySet[Fall], filters: dict[str, Any]) -> QuerySet[Fall]:
    """
    Apply supported filter keys to Fall queryset.
    """
    include_archived = bool(filters.get("include_archived", False))
    if not include_archived:
        falls = falls.filter(status="AKTIV")

    # Beratungsstelle (codes)
    bs = filters.get("zustaendige_beratungsstelle")
    if bs:
        if isinstance(bs, str):
            bs = [bs]
        falls = falls.filter(zustaendige_beratungsstelle__in=list(bs))

    # PersonenbezogeneDaten filters (codes)
    person_map = {
        "wohnort": "personenbezogene_daten__wohnort",
        "staatsangehoerigkeit_deutsch": "personenbezogene_daten__staatsangehoerigkeit_deutsch",
        "rolle_der_ratsuchenden_person": "personenbezogene_daten__rolle_der_ratsuchenden_person",
        "geschlechtsidentitaet": "personenbezogene_daten__geschlechtsidentitaet",
        "sexualitaet": "personenbezogene_daten__sexualitaet",
        "berufliche_situation": "personenbezogene_daten__berufliche_situation",
        "schwerbehinderung": "personenbezogene_daten__schwerbehinderung",
    }

    for key, orm_field in person_map.items():
        val = filters.get(key)
        if val:
            if isinstance(val, str):
                val = [val]
            falls = falls.filter(**{f"{orm_field}__in": list(val)})

    return falls


def _apply_beratung_filters(beratungen: QuerySet[Beratung], filters: dict[str, Any]) -> QuerySet[Beratung]:
    ba = filters.get("beratung_durchfuehrungsart")
    if ba:
        if isinstance(ba, str):
            ba = [ba]
        beratungen = beratungen.filter(durchfuehrungsart__in=list(ba))

    bo = filters.get("beratung_durchfuehrungsort")
    if bo:
        if isinstance(bo, str):
            bo = [bo]
        beratungen = beratungen.filter(durchfuehrungsort__in=list(bo))

    return beratungen


def _falls_from_period(*, date_from: date, date_to: date, filters: dict[str, Any]) -> QuerySet[Fall]:
    """
    Definition for 'Personen im Zeitraum beraten':
    A Fall is counted if it has at least one Beratung within [date_from, date_to],
    optionally filtered by Beratung attributes.
    """
    beratungen = Beratung.objects.filter(datum__gte=date_from, datum__lte=date_to)
    beratungen = _apply_beratung_filters(beratungen, filters)

    falls = Fall.objects.filter(beratungen__in=beratungen).distinct()
    falls = _apply_fall_filters(falls, filters)
    return falls


def _beratungen_from_period(*, date_from: date, date_to: date, filters: dict[str, Any]) -> QuerySet[Beratung]:
    """
    Beratungen within [date_from, date_to] for filtered falls.
    """
    falls = _falls_from_period(date_from=date_from, date_to=date_to, filters=filters)
    beratungen = Beratung.objects.filter(datum__gte=date_from, datum__lte=date_to, fall__in=falls)
    beratungen = _apply_beratung_filters(beratungen, filters)
    return beratungen


def _anfragen_from_period(*, date_from: date, date_to: date, filters: dict[str, Any]) -> QuerySet[Anfrage]:
    qs = Anfrage.objects.filter(datum_anfrage__gte=date_from, datum_anfrage__lte=date_to)
    # Optional filter: anfrage_aus
    ao = filters.get("anfrage_aus")
    if ao:
        if isinstance(ao, str):
            ao = [ao]
        qs = qs.filter(anfrage_aus__in=list(ao))
    return qs


def compute_statistics(
    *,
    date_from: date,
    date_to: date,
    filters: dict[str, Any],
    modules: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Compute requested statistics modules.

    Returns a JSON-serializable dict:
    {
      "period": {"date_from": "...", "date_to": "..."},
      "filters": {...},
      "modules": { "key": {...}, ... },
      "rows": [ {module, bucket_key, bucket_label, value}, ... ]  # for exports
    }
    """
    falls = _falls_from_period(date_from=date_from, date_to=date_to, filters=filters)
    beratungen = _beratungen_from_period(date_from=date_from, date_to=date_to, filters=filters)
    anfragen = _anfragen_from_period(date_from=date_from, date_to=date_to, filters=filters)

    out_modules: dict[str, Any] = {}
    rows: list[dict[str, Any]] = []

    def add_value(module_key: str, value: int):
        out_modules[module_key] = {"value": int(value)}
        rows.append({"module": module_key, "bucket_key": "", "bucket_label": "", "value": int(value)})

    def add_buckets(module_key: str, buckets: list[Bucket]):
        out_modules[module_key] = {
            "buckets": [{"key": b.key, "label": b.label, "count": b.count} for b in buckets]
        }
        for b in buckets:
            rows.append({"module": module_key, "bucket_key": b.key, "bucket_label": b.label, "value": b.count})

    for mod in modules:
        key = mod.get("key")
        if not key:
            continue

        if key == "cases_total":
            add_value("cases_total", falls.count())
            continue

        if key == "consultations_total":
            add_value("consultations_total", beratungen.count())
            continue

        if key == "inquiries_total":
            add_value("inquiries_total", anfragen.count())
            continue

        if key == "cases_by_beratungsstelle":
            agg = (
                falls.values(val=Coalesce("zustaendige_beratungsstelle", Value("", output_field=CharField())))
                .annotate(count=Count("fall_id", distinct=True))
                .order_by("val")
            )
            buckets = _bucketize(
                rows=list(agg),
                value_key="val",
                count_key="count",
                label_map=CHOICE_LABELS["fall.zustaendige_beratungsstelle"],
            )
            add_buckets("cases_by_beratungsstelle", buckets)
            continue

        if key == "clients_by_wohnort":
            agg = (
                falls.values(val=Coalesce("personenbezogene_daten__wohnort", Value("", output_field=CharField())))
                .annotate(count=Count("fall_id", distinct=True))
                .order_by("val")
            )
            buckets = _bucketize(rows=list(agg), value_key="val", count_key="count", label_map=CHOICE_LABELS["person.wohnort"])
            add_buckets("clients_by_wohnort", buckets)
            continue

        if key == "clients_by_staatsangehoerigkeit":
            agg = (
                falls.values(val=Coalesce("personenbezogene_daten__staatsangehoerigkeit_deutsch", Value("", output_field=CharField())))
                .annotate(count=Count("fall_id", distinct=True))
                .order_by("val")
            )
            buckets = _bucketize(
                rows=list(agg),
                value_key="val",
                count_key="count",
                label_map=CHOICE_LABELS["person.staatsangehoerigkeit_deutsch"],
            )
            add_buckets("clients_by_staatsangehoerigkeit", buckets)
            continue

        if key == "clients_by_rolle":
            agg = (
                falls.values(val=Coalesce("personenbezogene_daten__rolle_der_ratsuchenden_person", Value("", output_field=CharField())))
                .annotate(count=Count("fall_id", distinct=True))
                .order_by("val")
            )
            buckets = _bucketize(
                rows=list(agg),
                value_key="val",
                count_key="count",
                label_map=CHOICE_LABELS["person.rolle_der_ratsuchenden_person"],
            )
            add_buckets("clients_by_rolle", buckets)
            continue

        if key == "clients_by_geschlecht":
            agg = (
                falls.values(val=Coalesce("personenbezogene_daten__geschlechtsidentitaet", Value("", output_field=CharField())))
                .annotate(count=Count("fall_id", distinct=True))
                .order_by("val")
            )
            buckets = _bucketize(
                rows=list(agg),
                value_key="val",
                count_key="count",
                label_map=CHOICE_LABELS["person.geschlechtsidentitaet"],
            )
            add_buckets("clients_by_geschlecht", buckets)
            continue

        if key == "consultations_by_durchfuehrungsart":
            agg = (
                beratungen.values(val=Coalesce("durchfuehrungsart", Value("", output_field=CharField())))
                .annotate(count=Count("beratung_id"))
                .order_by("val")
            )
            buckets = _bucketize(
                rows=list(agg),
                value_key="val",
                count_key="count",
                label_map=CHOICE_LABELS["beratung.durchfuehrungsart"],
            )
            add_buckets("consultations_by_durchfuehrungsart", buckets)
            continue

        if key == "consultations_by_durchfuehrungsort":
            agg = (
                beratungen.values(val=Coalesce("durchfuehrungsort", Value("", output_field=CharField())))
                .annotate(count=Count("beratung_id"))
                .order_by("val")
            )
            buckets = _bucketize(
                rows=list(agg),
                value_key="val",
                count_key="count",
                label_map=CHOICE_LABELS["beratung.durchfuehrungsort"],
            )
            add_buckets("consultations_by_durchfuehrungsort", buckets)
            continue

        if key == "survey_question":
            question_id = mod.get("question_id")
            if not question_id:
                out_modules[key] = {"error": "question_id is required"}
                continue

            # Ensure question exists (label in response)
            question = CaseSurveyQuestion.objects.filter(question_id=question_id).first()
            q_label = question.label if question else str(question_id)

            agg = (
                CaseSurveyAnswer.objects.filter(case__in=falls, question_id=question_id)
                .values(val=Coalesce("value", Value("", output_field=CharField())))
                .annotate(count=Count("answer_id"))
                .order_by("val")
            )
            buckets = _bucketize(rows=list(agg), value_key="val", count_key="count", label_map=None)
            out_modules[key] = {
                "question_id": str(question_id),
                "question_label": q_label,
                "buckets": [{"key": b.key, "label": b.label, "count": b.count} for b in buckets],
            }
            for b in buckets:
                rows.append({"module": f"survey_question:{question_id}", "bucket_key": b.key, "bucket_label": b.label, "value": b.count})
            continue

        # Unknown module key -> keep info for debugging
        out_modules[key] = {"error": "unknown_module"}

    return {
        "period": {"date_from": date_from.isoformat(), "date_to": date_to.isoformat()},
        "filters": filters,
        "modules": out_modules,
        "rows": rows,
    }


def stats_meta() -> dict[str, Any]:
    """
    Returns available modules and filter/choice metadata for building a modular UI.
    """
    modules = [
        {"key": "cases_total", "label": "Anzahl beratener Personen (Fälle) im Zeitraum"},
        {"key": "consultations_total", "label": "Anzahl Beratungstermine im Zeitraum"},
        {"key": "inquiries_total", "label": "Anzahl Anfragen im Zeitraum"},
        {"key": "cases_by_beratungsstelle", "label": "Fälle nach zuständiger Beratungsstelle"},
        {"key": "clients_by_wohnort", "label": "Klientinnen nach Wohnort"},
        {"key": "clients_by_staatsangehoerigkeit", "label": "Klientinnen nach Staatsangehörigkeit (deutsch / nicht deutsch)"},
        {"key": "clients_by_rolle", "label": "Rolle der ratsuchenden Person"},
        {"key": "clients_by_geschlecht", "label": "Geschlechtsidentität"},
        {"key": "consultations_by_durchfuehrungsart", "label": "Beratungen nach Durchführungsart"},
        {"key": "consultations_by_durchfuehrungsort", "label": "Beratungen nach Durchführungsort"},
        {"key": "survey_question", "label": "Zusatzfrage (Survey) – Auswertung nach Antwortwerten", "requires": ["question_id"]},
    ]

    filters = {
        "include_archived": {"type": "boolean", "default": False},
        "zustaendige_beratungsstelle": {"type": "multi_choice", "choices": CHOICE_LABELS["fall.zustaendige_beratungsstelle"]},
        "wohnort": {"type": "multi_choice", "choices": CHOICE_LABELS["person.wohnort"]},
        "staatsangehoerigkeit_deutsch": {"type": "multi_choice", "choices": CHOICE_LABELS["person.staatsangehoerigkeit_deutsch"]},
        "rolle_der_ratsuchenden_person": {"type": "multi_choice", "choices": CHOICE_LABELS["person.rolle_der_ratsuchenden_person"]},
        "geschlechtsidentitaet": {"type": "multi_choice", "choices": CHOICE_LABELS["person.geschlechtsidentitaet"]},
        "sexualitaet": {"type": "multi_choice", "choices": CHOICE_LABELS["person.sexualitaet"]},
        "berufliche_situation": {"type": "multi_choice", "choices": CHOICE_LABELS["person.berufliche_situation"]},
        "schwerbehinderung": {"type": "multi_choice", "choices": CHOICE_LABELS["person.schwerbehinderung"]},
        "beratung_durchfuehrungsart": {"type": "multi_choice", "choices": CHOICE_LABELS["beratung.durchfuehrungsart"]},
        "beratung_durchfuehrungsort": {"type": "multi_choice", "choices": CHOICE_LABELS["beratung.durchfuehrungsort"]},
        "anfrage_aus": {"type": "multi_choice", "choices": CHOICE_LABELS["anfrage.anfrage_aus"]},
    }

    survey_questions = list(CaseSurveyQuestion.objects.all().values("question_id", "label", "field_type").order_by("label"))

    return {"modules": modules, "filters": filters, "survey_questions": survey_questions}

