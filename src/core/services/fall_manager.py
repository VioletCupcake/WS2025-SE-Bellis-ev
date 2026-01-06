"""
FallManager - Business logic coordinator for case management.
Handles atomic operations, permission checks, and search.
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime, date
from django.db import transaction
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import QuerySet

from core.models import Fall, PersonenbezogeneDaten, Beratung, Gewalttat, GewalttatArt, User
from core.models.reference_models import GewalttatArt




class FallManager:
    """
    Service class for Fall (case) lifecycle management.
    Coordinates multi-model operations with atomic transactions.
    """
    
    @staticmethod
    @transaction.atomic
    def createFall(fall_data: dict, personen_data: dict) -> Fall:
        """
        Create new Fall with PersonenbezogeneDaten atomically.
        
        Context: Fall and PersonenbezogeneDaten have 1:1 relationship.
        transaction.atomic() ensures both created together or not at all.
        
        Args:
            fall_data: Dictionary with Fall field values
                      zustaendige_beratungsstelle must use short code:
                      'FBS_1_LE', 'FBS_2_LKNSA', or 'FBS_3_LKLE'
            personen_data: Dictionary with PersonenbezogeneDaten field values
                          Must include 'alias' (validated for uniqueness)
        
        Returns:
            Fall: Created case with linked PersonenbezogeneDaten
            
        Raises:
            ValidationError: If validation fails or alias already exists
        """
        # Check alias uniqueness
        alias = personen_data.get('alias')
        if not alias:
            raise ValidationError({'alias': ['Alias is required']})
        
        if PersonenbezogeneDaten.objects.filter(alias=alias).exists():
            raise ValidationError({'alias': [f'Alias "{alias}" already exists']})
        
        # Create Fall
        fall = Fall(**fall_data)
        fall.full_clean()
        fall.save()
        
        # Create linked PersonenbezogeneDaten
        personen = PersonenbezogeneDaten(fall=fall, **personen_data)
        personen.full_clean()
        personen.save()
        
        return fall
    
    @staticmethod
    def updateFall(fall_id: UUID, fall_data: dict, 
                   personen_data: Optional[dict] = None) -> Fall:
        """
        Update existing Fall and optionally PersonenbezogeneDaten.
        
        Args:
            fall_id: UUID of Fall to update
            fall_data: Dictionary with Fall fields to update
            personen_data: Optional PersonenbezogeneDaten updates
            
        Returns:
            Fall: Updated case
        """
        fall = Fall.objects.get(fall_id=fall_id)
        
        # Update Fall fields
        for field, value in fall_data.items():
            setattr(fall, field, value)
        
        fall.full_clean()
        # Include letzte_bearbeitung so auto_now triggers
        fall.save(update_fields=list(fall_data.keys()) + ['letzte_bearbeitung'])
        
        # Update PersonenbezogeneDaten if provided
        if personen_data:
            personen = fall.personenbezogene_daten  # type: ignore[attr-defined]
            for field, value in personen_data.items():
                setattr(personen, field, value)
            personen.full_clean()
            personen.save()
        
        return fall
    
    @staticmethod
    def hardDeleteFall(fall_id: UUID, user: User) -> None:
        """
        Permanently delete Fall and all related data.
        
        Context: Executes CASCADE delete chain:
        1. PersonenbezogeneDaten (1:1)
        2. All Beratung records (1:N)
        3. All Gewalttat records (1:N)
        4. All junction table rows (M:N)
        
        Reference data (GewalttatArt, FolgenDerGewalt) protected.
        
        Args:
            fall_id: UUID of Fall to delete
            user: User attempting deletion (for permission check)
            
        Raises:
            PermissionDenied: If user lacks can_hard_delete_cases permission
            ValidationError: If user has no role assigned
            Fall.DoesNotExist: If fall_id not found
        """
        # Defensive check: User must have role assigned
        if not user.role:
            raise ValidationError(
                f"User {user.username} has no role assigned. Cannot check permissions."
            )
        
        # Permission check: Only ADMINISTRATOR role has hard delete
        if not user.role.permissions.can_hard_delete_cases:  # type: ignore[attr-defined]
            raise PermissionDenied(
                f"User {user.username} (role: {user.role.name}) does not have hard delete permission. "
                f"Required role: ADMINISTRATOR"
            )
        
        fall = Fall.objects.get(fall_id=fall_id)
        fall.delete()  # Django handles CASCADE automatically

    
    @staticmethod
    @transaction.atomic
    def addBeratung(fall_id: UUID, beratung_data: dict) -> Beratung:
        """
        Add counseling session to Fall.
        
        Context: Beratung.save() automatically updates Fall aggregates
        (beratungsanzahl, letzte_beratung). transaction.atomic() ensures
        both Beratung creation and Fall update succeed together.
        
        Args:
            fall_id: UUID of Fall
            beratung_data: Dictionary with Beratung fields (datum, durchfuehrungsart, etc.)
                          durchfuehrungsart codes: 'PERSOENLICH', 'VIDEO', 'TELEFON', etc.
                          durchfuehrungsort codes: 'LEIPZIG_STADT', 'LEIPZIG_LAND', 'NORDSACHSEN'
            
        Returns:
            Beratung: Created session (Fall aggregates auto-updated)
        """
        fall = Fall.objects.get(fall_id=fall_id)
        
        beratung = Beratung(fall=fall, **beratung_data)
        beratung.full_clean()
        beratung.save()  # Automatically updates Fall via save() override
        
        return beratung
    
    @staticmethod
    @transaction.atomic
    def addGewalttat(fall_id: UUID, gewalttat_data: dict, 
                     art_ids: Optional[List[UUID]] = None) -> Gewalttat:
        """
        Add violence incident to Fall.
        
        Context: Gewalttat has M:N relationship with GewalttatArt.
        Create Gewalttat first, then link to types via junction table.
        
        Args:
            fall_id: UUID of Fall
            gewalttat_data: Dictionary with Gewalttat fields
            art_ids: Optional list of GewalttatArt UUIDs (M:N relationship)
            
        Returns:
            Gewalttat: Created incident with type associations
        """
        fall = Fall.objects.get(fall_id=fall_id)
        
        gewalttat = Gewalttat(fall=fall, **gewalttat_data)
        gewalttat.full_clean()
        gewalttat.save()
        
        # Link to violence types if provided
        if art_ids:
            gewalttat_art_objects = GewalttatArt.objects.filter(art_id__in=art_ids)
            # Django's M2M manager handles junction table
            gewalttat.gewalttat_arten.set(gewalttat_art_objects)
        
        return gewalttat
    
    @staticmethod
    def searchByAlias(alias: str) -> PersonenbezogeneDaten:
        """
        Search for case by unique alias.
        
        Args:
            alias: Case pseudonym
            
        Returns:
            PersonenbezogeneDaten: Found record (access Fall via .fall)
            
        Raises:
            PersonenbezogeneDaten.DoesNotExist: If not found
        """
        return PersonenbezogeneDaten.objects.select_related('fall').get(alias=alias)
    
    @staticmethod
    def searchByDateRange(from_date: date, to_date: date) -> QuerySet[Fall]:
        """
        Search cases created within date range.
        
        Args:
            from_date: Start date (inclusive)
            to_date: End date (inclusive)
            
        Returns:
            QuerySet[Fall]: Cases created in range
        """
        return Fall.objects.filter(
            erstellungsdatum__gte=from_date,
            erstellungsdatum__lte=to_date
        ).select_related('personenbezogene_daten')
    
    @staticmethod
    def searchByBeratungsstelle(stelle: str) -> QuerySet[Fall]:
        """
        Search cases by counseling center.
        
        Args:
            stelle: Counseling center code ('FBS_1_LE', 'FBS_2_LKNSA', or 'FBS_3_LKLE')
            
        Returns:
            QuerySet[Fall]: Cases assigned to center
        """
        return Fall.objects.filter(
            zustaendige_beratungsstelle=stelle
        ).select_related('personenbezogene_daten')
