"""
Django forms for case management.

Combines Fall and PersonenbezogeneDaten models into single creation form.
Uses ModelForm for automatic field generation and validation.
"""

from django import forms
from core.models import Fall, PersonenbezogeneDaten


class FallCreateForm(forms.ModelForm):
    """
    Combined form for creating Fall with PersonenbezogeneDaten.
    
    Includes fields from both models. PersonenbezogeneDaten fields
    are prefixed with 'personen_' to avoid naming conflicts.
    
    Usage in view:
        if request.method == 'POST':
            form = FallCreateForm(request.POST)
            if form.is_valid():
                # Extract Fall and PersonenbezogeneDaten data
                fall_data = {
                    'zustaendige_beratungsstelle': form.cleaned_data['zustaendige_beratungsstelle'],
                    'informationsquelle': form.cleaned_data['informationsquelle'],
                    # ... etc
                }
                personen_data = {
                    'alias': form.cleaned_data['personen_alias'],
                    'rolle_der_ratsuchenden_person': form.cleaned_data['personen_rolle_der_ratsuchenden_person'],
                    # ... etc
                }
                fall = FallManager.create_fall(fall_data, personen_data)
    """
    
    # PersonenbezogeneDaten fields with 'personen_' prefix
    personen_alias = forms.CharField(
        max_length=64,
        required=True,
        label="Alias (Pseudonym)",
        help_text="Eindeutiger Identifikator für den Fall"
    )
    
    personen_rolle_der_ratsuchenden_person = forms.ChoiceField(
        choices=PersonenbezogeneDaten.ROLLE_CHOICES,
        required=True,
        label="Rolle der ratsuchenden Person"
    )
    
    personen_alter = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=120,
        label="Alter",
        widget=forms.NumberInput(attrs={'placeholder': 'Jahre'})
    )
    
    personen_alter_keine_angabe = forms.BooleanField(
        required=False,
        label="Keine Angabe zum Alter"
    )
    
    personen_geschlechtsidentitaet = forms.ChoiceField(
        choices=[('', '--- Bitte wählen ---')] + list(PersonenbezogeneDaten.GESCHLECHT_CHOICES),
        required=False,
        label="Geschlechtsidentität"
    )
    
    personen_sexualitaet = forms.ChoiceField(
        choices=[('', '--- Bitte wählen ---')] + list(PersonenbezogeneDaten.SEXUALITAET_CHOICES),
        required=False,
        label="Sexualität"
    )
    
    personen_wohnort = forms.ChoiceField(
        choices=[('', '--- Bitte wählen ---')] + list(PersonenbezogeneDaten.WOHNORT_CHOICES),
        required=False,
        label="Wohnort"
    )
    
    personen_wohnort_details = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        label="Wohnort Details"
    )
    
    personen_staatsangehoerigkeit_deutsch = forms.ChoiceField(
        choices=[('', '--- Bitte wählen ---')] + list(PersonenbezogeneDaten.STAATSANGEHOERIGKEIT_CHOICES),
        required=False,
        label="Staatsangehörigkeit",
        help_text="Wählen Sie 'deutsch' oder 'nicht deutsch'"
    )
    
    personen_staatsangehoerigkeit_land = forms.CharField(
        max_length=100,
        required=False,
        label="Staatsangehörigkeit Land",
        help_text="Nur ausfüllen wenn 'nicht deutsch'"
    )
    
    personen_berufliche_situation = forms.ChoiceField(
        choices=[('', '--- Bitte wählen ---')] + list(PersonenbezogeneDaten.BERUF_CHOICES),
        required=False,
        label="Berufliche Situation"
    )
    
    personen_schwerbehinderung = forms.ChoiceField(
        choices=[('', '--- Bitte wählen ---')] + list(PersonenbezogeneDaten.SCHWERBEHINDERUNG_CHOICES),
        required=False,
        label="Schwerbehinderung"
    )
    
    personen_form_der_behinderung = forms.ChoiceField(
        choices=[('', '--- Bitte wählen ---')] + list(PersonenbezogeneDaten.BEHINDERUNG_CHOICES),
        required=False,
        label="Form der Behinderung"
    )
    
    personen_grad_der_behinderung = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=100,
        label="Grad der Behinderung (GdB)",
        help_text="Wert zwischen 0 und 100",
        widget=forms.NumberInput(attrs={'placeholder': '0-100'})
    )
    
    personen_personenbezogene_notizen = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Personenbezogene Notizen"
    )
    
    class Meta:
        model = Fall
        fields = [
            'zustaendige_beratungsstelle',
            'informationsquelle',
            'informationsquelle_andere_details',
            'anzahl_dolmetschungs_stunden',
            'dolmetschungs_sprachen',
            'weitere_notizen',
        ]
        
        labels = {
            'zustaendige_beratungsstelle': 'Zuständige Beratungsstelle',
            'informationsquelle': 'Informationsquelle',
            'informationsquelle_andere_details': 'Informationsquelle Details (bei "andere")',
            'anzahl_dolmetschungs_stunden': 'Anzahl Dolmetschungsstunden',
            'dolmetschungs_sprachen': 'Dolmetschungssprachen',
            'weitere_notizen': 'Weitere Notizen',
        }
        
        widgets = {
            'informationsquelle_andere_details': forms.Textarea(attrs={'rows': 2}),
            'dolmetschungs_sprachen': forms.Textarea(attrs={'rows': 2}),
            'weitere_notizen': forms.Textarea(attrs={'rows': 3}),
        }
        
        help_texts = {
            'anzahl_dolmetschungs_stunden': '0.0 = keine Dolmetschung verwendet',
        }
    
    def clean(self):
        """
        Cross-field validation matching model validation logic.
        """
        cleaned_data = super().clean()
        
        # Fall validation: informationsquelle='andere Quelle' requires details
        if cleaned_data.get('informationsquelle') == 'ANDERE':
            if not cleaned_data.get('informationsquelle_andere_details', '').strip():
                self.add_error(
                    'informationsquelle_andere_details',
                    'Details erforderlich wenn Informationsquelle "andere Quelle" ist'
                )
        
        # PersonenbezogeneDaten validation: alter_keine_angabe requires alter=NULL
        if cleaned_data.get('personen_alter_keine_angabe'):
            if cleaned_data.get('personen_alter') is not None:
                self.add_error(
                    'personen_alter',
                    'Alter muss leer sein wenn "Keine Angabe" ausgewählt ist'
                )
        
        # grad_der_behinderung requires schwerbehinderung='JA'
        if cleaned_data.get('personen_grad_der_behinderung') is not None:
            if cleaned_data.get('personen_schwerbehinderung') != 'JA':
                self.add_error(
                    'personen_grad_der_behinderung',
                    'Nur gültig wenn Schwerbehinderung "Ja" ist'
                )
        
        # form_der_behinderung requires schwerbehinderung='JA'
        if cleaned_data.get('personen_form_der_behinderung'):
            if cleaned_data.get('personen_schwerbehinderung') != 'JA':
                self.add_error(
                    'personen_form_der_behinderung',
                    'Nur gültig wenn Schwerbehinderung "Ja" ist'
                )
        
        # staatsangehoerigkeit_land requires staatsangehoerigkeit_deutsch='NICHTDEUTSCH'
        if cleaned_data.get('personen_staatsangehoerigkeit_land'):
            if cleaned_data.get('personen_staatsangehoerigkeit_deutsch') == 'DEUTSCH':
                self.add_error(
                    'personen_staatsangehoerigkeit_land',
                    'Nur gültig wenn Staatsangehörigkeit "nicht deutsch" ist'
                )
        
        return cleaned_data
