"""
DRF API Views for the Bellis REST API.
Provides endpoints for Fall, Beratung, Anfrage, and reference data.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from core.models import (
    Fall, Beratung, Anfrage, FolgenDerGewalt, Fall_FolgenDerGewalt
)
from .serializers import (
    FallListSerializer, FallDetailSerializer, FallCreateSerializer,
    FallUpdateSerializer, BeratungSerializer, AnfrageCreateSerializer,
    FolgenDerGewaltSerializer, FallFolgenCreateSerializer
)


# ===== FALL (CASE) VIEWS =====

class FallListView(generics.ListAPIView):
    """GET /api/cases/ – Alle aktiven Fälle auflisten."""
    permission_classes = [AllowAny]
    serializer_class = FallListSerializer
    queryset = Fall.objects.filter(status='AKTIV').select_related('personenbezogene_daten')


class FallCreateView(generics.CreateAPIView):
    """POST /api/fall/create/ – Neuen Fall anlegen."""
    permission_classes = [AllowAny]
    serializer_class = FallCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fall = serializer.save()
        return Response(
            {'id': str(fall.fall_id), 'message': 'Fall erstellt'},
            status=status.HTTP_201_CREATED
        )


class FallDetailView(generics.RetrieveUpdateAPIView):
    """
    GET /api/fall/<id>/ – Fall-Details laden.
    PUT /api/fall/<id>/ – Fall aktualisieren.
    """
    permission_classes = [AllowAny]
    lookup_field = 'fall_id'
    queryset = Fall.objects.select_related('personenbezogene_daten')

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return FallUpdateSerializer
        return FallDetailSerializer


# ===== FOLGEN (CONSEQUENCES) VIEWS =====

class FolgenListView(generics.ListAPIView):
    """GET /api/folgen/ – Alle Folgen-Typen laden (Referenzdaten)."""
    permission_classes = [AllowAny]
    serializer_class = FolgenDerGewaltSerializer
    queryset = FolgenDerGewalt.objects.all()


class FallFolgeCreateView(generics.CreateAPIView):
    """POST /api/fall/<fall_id>/folge/ – Folge mit Fall verknüpfen."""
    permission_classes = [AllowAny]
    serializer_class = FallFolgenCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['fall'] = get_object_or_404(Fall, fall_id=self.kwargs['fall_id'])
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Folge verknüpft'},
            status=status.HTTP_201_CREATED
        )


# ===== BERATUNG (CONSULTATION) VIEWS =====

class BeratungCreateView(generics.CreateAPIView):
    """POST /api/beratung/create/ – Neue Beratung erstellen."""
    permission_classes = [AllowAny]
    serializer_class = BeratungSerializer


class BeratungDeleteView(generics.DestroyAPIView):
    """DELETE /api/beratungen/<id>/ – Beratung löschen."""
    permission_classes = [AllowAny]
    queryset = Beratung.objects.all()
    lookup_field = 'beratung_id'


# ===== ANFRAGE (INQUIRY) VIEWS =====

class AnfrageCreateView(generics.CreateAPIView):
    """POST /api/anfragen/ – Neue Anfrage erstellen."""
    permission_classes = [AllowAny]
    serializer_class = AnfrageCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        anfrage = serializer.save()
        return Response(
            {'id': str(anfrage.anfrage_id), 'message': 'Anfrage erstellt'},
            status=status.HTTP_201_CREATED
        )
