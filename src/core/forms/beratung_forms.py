"""
Forms for Beratung (Counseling Session) management.

Uses Django ModelForm for automatic field generation from Beratung model.
Simpler than FallCreateForm because it only touches one model.
"""

from django import forms
from core.models import Beratung


class BeratungForm(forms.ModelForm):
    """
    Form for adding/editing counseling sessions.
    
    Automatically generates fields from Beratung model.
    Django handles validation using model field definitions and clean() method.
    """
    
    class Meta:
        model = Beratung
        fields = [
            'datum',
            'durchfuehrungsart',
            'durchfuehrungsort',
            'weitere_notizen',
        ]
        widgets = {
            'datum': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'durchfuehrungsart': forms.Select(attrs={'class': 'form-control'}),
            'durchfuehrungsort': forms.Select(attrs={'class': 'form-control'}),
            'weitere_notizen': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
        }
        labels = {
            'datum': 'Beratungsdatum',
            'durchfuehrungsart': 'Durchführungsart',
            'durchfuehrungsort': 'Durchführungsort',
            'weitere_notizen': 'Weitere Notizen',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize form with Fall instance.
        Fall is required for linking the Beratung to the correct case.
        """
        self.fall = kwargs.pop('fall', None)
        super().__init__(*args, **kwargs)
        
        # Make all fields optional except datum and durchfuehrungsart
        self.fields['datum'].required = True
        self.fields['durchfuehrungsart'].required = True
        self.fields['durchfuehrungsort'].required = True
        self.fields['weitere_notizen'].required = False
    
    def save(self, commit=True):
        """
        Override save to attach Fall before database commit.
        Also triggers Fall aggregate counter updates via Beratung.save() override.
        """
        beratung = super().save(commit=False)
        
        if self.fall:
            beratung.fall = self.fall
        
        if commit:
            beratung.save()  # Triggers Fall.beratungsanzahl update
        
        return beratung
