
"""
Forms for Fall (Case) management.

Uses Django ModelForm for automatic field generation and validation.
No custom form managers - Django's form.is_valid() calls model.clean() automatically.
"""

from django import forms
from django.core.exceptions import ValidationError
from core.models import Fall, PersonenbezogeneDaten


class FallCreateForm(forms.Form):
    """
    Combined form for creating Fall + PersonenbezogeneDaten atomically.
    
    NOT a ModelForm because it spans two models.
    Uses FallManager.createFall() for atomic transaction on save.
    """
    
    # ===== FALL FIELDS =====
    zustaendige_beratungsstelle = forms.ChoiceField(
        choices=Fall.BERATUNGSSTELLE_CHOICES,
        label="Zuständige Beratungsstelle",
        required=True
    )
    
    informationsquelle = forms.ChoiceField(
        choices=Fall.INFO_QUELLE_CHOICES,
        label="Informationsquelle",
        required=False
    )
    
    informationsquelle_andere_details = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Andere Quelle - Details",
        required=False
    )
    
    anzahl_dolmetschungen_stunden = forms.FloatField(
        initial=0.0,
        min_value=0.0,
        label="Dolmetschungen (Stunden)",
        required=False
    )
    
    dolmetschung_sprachen = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Dolmetschung - Sprachen",
        required=False
    )
    
    weitere_notizen = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Weitere Notizen",
        required=False
    )
    
    # ===== PERSONENBEZOGENE DATEN FIELDS =====
    alias = forms.CharField(
        max_length=64,
        label="Alias (eindeutige Kennung)",
        required=True,
        help_text="Z.B. MS_001"
    )
    
    rolle_der_ratsuchenden_person = forms.ChoiceField(
        choices=PersonenbezogeneDaten.ROLLE_CHOICES,
        label="Rolle der ratsuchenden Person",
        required=True
    )
    
    alter = forms.IntegerField(
        min_value=0,
        max_value=120,
        label="Alter",
        required=False
    )
    
    alter_keine_angabe = forms.BooleanField(
        label="Alter - keine Angabe",
        required=False
    )
    
    geschlechtsidentitaet = forms.ChoiceField(
        choices=PersonenbezogeneDaten.GESCHLECHT_CHOICES,
        label="Geschlechtsidentität",
        required=False
    )
    
    sexualitaet = forms.ChoiceField(
        choices=PersonenbezogeneDaten.SEXUALITAET_CHOICES,
        label="Sexualität",
        required=False
    )
    
    wohnort = forms.ChoiceField(
        choices=PersonenbezogeneDaten.WOHNORT_CHOICES,
        label="Wohnort",
        required=False
    )
    
    wohnort_details = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Wohnort - Details",
        required=False
    )
    
    staatsangehoerigkeit_deutsch = forms.ChoiceField(
        choices=PersonenbezogeneDaten.STAATSANGEHOERIGKEIT_CHOICES,
        label="Staatsangehörigkeit deutsch?",
        required=False
    )
    
    staatsangehoerigkeit_land = forms.CharField(
        max_length=100,
        label="Staatsangehörigkeit - Land",
        required=False
    )
    
    berufliche_situation = forms.ChoiceField(
        choices=PersonenbezogeneDaten.BERUF_CHOICES,
        label="Berufliche Situation",
        required=False
    )
    
    schwerbehinderung = forms.ChoiceField(
        choices=PersonenbezogeneDaten.SCHWERBEHINDERUNG_CHOICES,
        label="Liegt eine Schwerbehinderung vor?",
        required=False
    )
    
    form_der_behinderung = forms.ChoiceField(
        choices=PersonenbezogeneDaten.BEHINDERUNG_CHOICES,
        label="Form der Behinderung",
        required=False
    )
    
    grad_der_behinderung = forms.IntegerField(
        min_value=0,
        max_value=100,
        label="Grad der Behinderung (GdB)",
        required=False
    )
    
    personenbezogene_notizen = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Personenbezogene Notizen",
        required=False
    )
    
    def clean(self):
        """
        Cross-field validation.
        Django calls this automatically after individual field validation.
        """
        cleaned_data = super().clean()
        
        # Validate: informationsquelle "ANDERE" requires details
        if cleaned_data.get('informationsquelle') == 'ANDERE':
            if not cleaned_data.get('informationsquelle_andere_details', '').strip():
                self.add_error(
                    'informationsquelle_andere_details',
                    'Details erforderlich bei Auswahl "andere Quelle"'
                )
        
        # Validate: alter_keine_angabe=True requires alter=None
        if cleaned_data.get('alter_keine_angabe'):
            if cleaned_data.get('alter') is not None:
                self.add_error(
                    'alter',
                    'Alter muss leer sein wenn "keine Angabe" ausgewählt'
                )
        
        # Validate: schwerbehinderung-dependent fields
        if cleaned_data.get('schwerbehinderung') != 'JA':
            if cleaned_data.get('grad_der_behinderung') is not None:
                self.add_error(
                    'grad_der_behinderung',
                    'Nur gültig bei Schwerbehinderung "Ja"'
                )
            if cleaned_data.get('form_der_behinderung'):
                self.add_error(
                    'form_der_behinderung',
                    'Nur gültig bei Schwerbehinderung "Ja"'
                )
            
        
        # Validate: staatsangehoerigkeit_land requires nicht_deutsch
        if cleaned_data.get('staatsangehoerigkeit_land'):
            if cleaned_data.get('staatsangehoerigkeit_deutsch') == 'DEUTSCH':
                self.add_error(
                    'staatsangehoerigkeit_land',
                    'Nur gültig bei Staatsangehörigkeit "nicht deutsch"'
                )
        
        return cleaned_data
    
    def get_fall_data(self):
        """Extract Fall-specific fields from cleaned_data."""
        return {
            'zustaendige_beratungsstelle': self.cleaned_data['zustaendige_beratungsstelle'],
            'informationsquelle': self.cleaned_data.get('informationsquelle'),
            'informationsquelle_andere_details': self.cleaned_data.get('informationsquelle_andere_details', ''),
            'anzahl_dolmetschungen_stunden': self.cleaned_data.get('anzahl_dolmetschungen_stunden', 0.0),
            'dolmetschung_sprachen': self.cleaned_data.get('dolmetschung_sprachen', ''),
            'weitere_notizen': self.cleaned_data.get('weitere_notizen', ''),
        }
    
    def get_personen_data(self):
        """Extract PersonenbezogeneDaten-specific fields from cleaned_data."""
        return {
            'alias': self.cleaned_data['alias'],
            'rolle_der_ratsuchenden_person': self.cleaned_data['rolle_der_ratsuchenden_person'],
            'alter': self.cleaned_data.get('alter'),
            'alter_keine_angabe': self.cleaned_data.get('alter_keine_angabe', False),
            'geschlechtsidentitaet': self.cleaned_data.get('geschlechtsidentitaet'),
            'sexualitaet': self.cleaned_data.get('sexualitaet'),
            'wohnort': self.cleaned_data.get('wohnort'),
            'wohnort_details': self.cleaned_data.get('wohnort_details', ''),
            'staatsangehoerigkeit_deutsch': self.cleaned_data.get('staatsangehoerigkeit_deutsch'),
            'staatsangehoerigkeit_land': self.cleaned_data.get('staatsangehoerigkeit_land', ''),
            'berufliche_situation': self.cleaned_data.get('berufliche_situation'),
            'schwerbehinderung': self.cleaned_data.get('schwerbehinderung'),
            'form_der_behinderung': self.cleaned_data.get('form_der_behinderung', ''),
            'grad_der_behinderung': self.cleaned_data.get('grad_der_behinderung'),
            'personenbezogene_notizen': self.cleaned_data.get('personenbezogene_notizen', ''),
        }
