"""
Forms for Anfrage (Inquiry) management.

Simple Django Form for one-time inquiry creation with soft validation.
Unlike Fall, Anfrage does not create a persistent editable record.
"""

from django import forms
from core.models import Anfrage


class AnfrageCreateForm(forms.Form):
    """
    Form for creating a new Anfrage (one-time inquiry).
    
    Provides soft validation: warns users about incomplete fields
    but allows saving with force_save parameter.
    """
    
    # Contact method
    wie = forms.ChoiceField(
        choices=Anfrage.WIE_CHOICES,
        label="Wie (Kontaktweg)",
        required=True
    )
    
    # Date of inquiry
    datum_anfrage = forms.DateField(
        label="Datum der Anfrage",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    # Origin
    anfrage_aus = forms.ChoiceField(
        choices=Anfrage.ANFRAGE_AUS_CHOICES,
        label="Anfrage aus",
        required=True
    )
    
    # Who made the inquiry
    wer_hat_angefragt = forms.ChoiceField(
        choices=Anfrage.WER_HAT_ANGEFRAGT_CHOICES,
        label="Wer hat angefragt",
        required=True
    )
    
    # Type of inquiry
    art_der_anfrage = forms.ChoiceField(
        choices=Anfrage.ART_DER_ANFRAGE_CHOICES,
        label="Art der Anfrage",
        required=True
    )
    
    # Appointment scheduled
    termin_vergeben = forms.BooleanField(
        label="Termin vergeben",
        required=False
    )
    
    # Appointment date (conditional)
    termin_datum = forms.DateField(
        label="Datum des Termins",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    # Appointment location (conditional)
    termin_ort = forms.ChoiceField(
        choices=[('', '---------')] + list(Anfrage.TERMIN_ORT_CHOICES),
        label="Ort des Termins",
        required=False
    )
    
    def clean(self):
        """
        Cross-field validation.
        Note: Soft validation - returns warnings, does not block submission.
        """
        cleaned_data = super().clean()
        termin_vergeben = cleaned_data.get('termin_vergeben')
        termin_datum = cleaned_data.get('termin_datum')
        termin_ort = cleaned_data.get('termin_ort')
        
        # If termin_vergeben=False but termin fields filled, clear them
        if not termin_vergeben:
            if termin_datum or termin_ort:
                cleaned_data['termin_datum'] = None
                cleaned_data['termin_ort'] = ''
        
        return cleaned_data
    
    def get_incomplete_fields(self):
        """
        Returns list of field names that are missing when termin_vergeben=True.
        Used to show warning dialog before saving.
        """
        incomplete = []
        
        if self.is_valid():
            data = self.cleaned_data
            
            # Check if termin_vergeben but missing termin details
            if data.get('termin_vergeben'):
                if not data.get('termin_datum'):
                    incomplete.append('Datum des Termins')
                if not data.get('termin_ort'):
                    incomplete.append('Ort des Termins')
        
        return incomplete
    
    def get_anfrage_data(self):
        """Extract Anfrage-specific fields from cleaned_data."""
        return {
            'wie': self.cleaned_data['wie'],
            'datum_anfrage': self.cleaned_data['datum_anfrage'],
            'anfrage_aus': self.cleaned_data['anfrage_aus'],
            'wer_hat_angefragt': self.cleaned_data['wer_hat_angefragt'],
            'art_der_anfrage': self.cleaned_data['art_der_anfrage'],
            'termin_vergeben': self.cleaned_data.get('termin_vergeben', False),
            'termin_datum': self.cleaned_data.get('termin_datum'),
            'termin_ort': self.cleaned_data.get('termin_ort', ''),
        }


class AnfrageEditForm(AnfrageCreateForm):
    """
    Form for editing an existing Anfrage.
    
    Extends AnfrageCreateForm with instance loading and saving.
    """
    
    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        
        # Pre-populate initial values from instance
        if instance and not args:
            initial = kwargs.get('initial', {})
            initial.update({
                'wie': instance.wie,
                'datum_anfrage': instance.datum_anfrage,
                'anfrage_aus': instance.anfrage_aus,
                'wer_hat_angefragt': instance.wer_hat_angefragt,
                'art_der_anfrage': instance.art_der_anfrage,
                'termin_vergeben': instance.termin_vergeben,
                'termin_datum': instance.termin_datum,
                'termin_ort': instance.termin_ort,
            })
            kwargs['initial'] = initial
        
        super().__init__(*args, **kwargs)
    
    def save(self, user=None):
        """Update the existing Anfrage instance with form data."""
        data = self.get_anfrage_data()
        for field, value in data.items():
            setattr(self.instance, field, value)
        if user:
            self.instance.bearbeitet_von = user
        self.instance.save()
        return self.instance
