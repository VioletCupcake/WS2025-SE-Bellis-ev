"""
DRF API Views for statistics, presets and export.
"""

import csv
import io

from django.http import HttpResponse
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from core.models import StatistikPreset
from core.services.statistics_service import compute_statistics, stats_meta
from .statistics_serializers import (
    StatisticsRequestSerializer,
    StatsPresetSerializer,
    StatsPresetCreateSerializer,
)


def _user_can_manage_global_presets(user) -> bool:
    """
    Keep this conservative: require authenticated user with can_manage_users OR admin role.
    """
    if not getattr(user, "is_authenticated", False):
        return False
    role = getattr(user, "role", None)
    perms = getattr(role, "permissions", None) if role else None
    if perms and getattr(perms, "can_manage_users", False):
        return True
    if role and getattr(role, "name", "") == "ADMIN":
        return True
    return False


class StatisticsMetaView(APIView):
    """
    GET /api/stats/meta/ – provides available modules/filters and survey questions.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(stats_meta())


class StatisticsComputeView(APIView):
    """
    POST /api/stats/compute/
    Body: {date_from, date_to, filters, modules}
    """

    permission_classes = [AllowAny]

    def post(self, request):
        ser = StatisticsRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        result = compute_statistics(
            date_from=data["date_from"],
            date_to=data["date_to"],
            filters=data.get("filters") or {},
            modules=data.get("modules") or [],
        )
        return Response(result)


class StatisticsExportView(APIView):
    """
    POST /api/stats/export/<format>/
    format in: csv | xlsx | pdf
    Body: same as /compute
    """

    permission_classes = [AllowAny]

    def post(self, request, export_format: str):
        ser = StatisticsRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        result = compute_statistics(
            date_from=data["date_from"],
            date_to=data["date_to"],
            filters=data.get("filters") or {},
            modules=data.get("modules") or [],
        )
        rows = result.get("rows", [])
        period = result.get("period", {})

        filename_base = f"statistik_{period.get('date_from','')}_{period.get('date_to','')}".strip("_")

        if export_format == "csv":
            return _export_csv(rows, f"{filename_base}.csv")
        if export_format == "xlsx":
            return _export_xlsx(rows, f"{filename_base}.xlsx")
        if export_format == "pdf":
            return _export_pdf(rows, f"{filename_base}.pdf")

        return Response({"error": "unsupported_format"}, status=status.HTTP_400_BAD_REQUEST)


def _export_csv(rows: list[dict], filename: str) -> HttpResponse:
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(["module", "bucket_key", "bucket_label", "value"])
    for r in rows:
        writer.writerow([r.get("module", ""), r.get("bucket_key", ""), r.get("bucket_label", ""), r.get("value", 0)])
    return response


def _export_xlsx(rows: list[dict], filename: str) -> HttpResponse:
    wb = Workbook()
    ws = wb.active
    ws.title = "Statistik"
    ws.append(["module", "bucket_key", "bucket_label", "value"])
    for r in rows:
        ws.append([r.get("module", ""), r.get("bucket_key", ""), r.get("bucket_label", ""), r.get("value", 0)])

    out = io.BytesIO()
    wb.save(out)
    out.seek(0)

    response = HttpResponse(
        out.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def _export_pdf(rows: list[dict], filename: str) -> HttpResponse:
    """
    Minimal PDF export using reportlab (table-like, line based).
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Statistik-Export")
    y -= 30

    c.setFont("Helvetica", 9)
    header = ["module", "bucket_key", "bucket_label", "value"]
    c.drawString(40, y, " | ".join(header))
    y -= 16

    for r in rows:
        line = f"{r.get('module','')} | {r.get('bucket_key','')} | {r.get('bucket_label','')} | {r.get('value',0)}"
        c.drawString(40, y, line[:150])  # keep line short to avoid overflow
        y -= 12
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 9)
            y = height - 40

    c.save()
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


# ===== PRESETS =====


class StatsPresetListCreateView(generics.ListCreateAPIView):
    """
    GET /api/stats/presets/ – list presets visible to user (GLOBAL + personal)
    POST /api/stats/presets/ – create preset (PERSONAL by default)
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # scope="GLOBAL" -> ist_global=True
        # scope="PERSONAL" -> ist_global=False, erstellt_von=user
        return StatistikPreset.objects.filter(
            Q(ist_global=True) | Q(ist_global=False, erstellt_von=user)
        ).order_by("name")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StatsPresetCreateSerializer
        return StatsPresetSerializer

    def perform_create(self, serializer):
        user = self.request.user
        # serializer.validated_data already contains 'ist_global' from create() method in serializer?
        # No, perform_create calls save(), serializer.save() calls create()
        # The serializer create() method handles the scope -> ist_global mapping.
        # But we need to enforce permissions here if ist_global is explicitly set.
        
        # We need to access the raw data or validated data to check scope/ist_global
        ist_global = serializer.validated_data.get("ist_global", False)
        # Note: StatsPresetCreateSerializer.create() logic might run AFTER perform_create calls save().
        # Actually save() calls create().
        
        # Let's rely on the serializer validation or check here.
        # The serializer has `scope` in `initial_data`.
        scope = self.request.data.get("scope", "PERSONAL")

        if scope == "GLOBAL" and not _user_can_manage_global_presets(user):
            raise PermissionDenied("Not allowed to create GLOBAL presets")

        serializer.save(
            erstellt_von=user,
            ist_system_preset=False,
        )


class StatsPresetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET/PUT/DELETE /api/stats/presets/<preset_id>/
    """

    permission_classes = [IsAuthenticated]
    lookup_field = "preset_id"
    serializer_class = StatsPresetSerializer

    def get_queryset(self):
        user = self.request.user
        return StatistikPreset.objects.filter(
            Q(ist_global=True) | Q(ist_global=False, erstellt_von=user)
        )

    def update(self, request, *args, **kwargs):
        preset = self.get_object()
        user = request.user

        if preset.ist_system_preset and not _user_can_manage_global_presets(user):
            return Response({"error": "system_preset_readonly"}, status=status.HTTP_403_FORBIDDEN)

        # Allow editing name/payload/scope within bounds
        data = request.data.copy()
        
        # If existing preset is global, check permissions
        if preset.ist_global and not _user_can_manage_global_presets(user):
            return Response({"error": "not_allowed_global"}, status=status.HTTP_403_FORBIDDEN)

        # If user attempts to change to GLOBAL, enforce permission
        if data.get("scope") == "GLOBAL" and not _user_can_manage_global_presets(user):
            return Response({"error": "not_allowed_global"}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        preset = self.get_object()
        user = request.user

        if preset.ist_system_preset and not _user_can_manage_global_presets(user):
            return Response({"error": "system_preset_readonly"}, status=status.HTTP_403_FORBIDDEN)

        if preset.ist_global and not _user_can_manage_global_presets(user):
            return Response({"error": "not_allowed_global"}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

