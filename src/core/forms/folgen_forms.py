"""
Forms for FolgenDerGewalt (Consequences of Violence) management.

Uses Django ModelForm for Fall_FolgenDerGewalt junction table.
Allows selecting a consequence type and adding optional details.
"""

from django import forms
from core.models import FolgenDerGewalt, Fall_FolgenDerGewalt


class FolgenDerGewaltForm(forms.ModelForm):
    """
    Form for adding/editing consequence links to a case.
    
    Uses Fall_FolgenDerGewalt junction table to support:
    - Multiple consequences per case
    - Additional information per consequence
    """
    
    # Override folge field to show hierarchical display
    folge = forms.ModelChoiceField(
        queryset=FolgenDerGewalt.objects.all().order_by('kategorie', 'name'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Folge der Gewalt',
        help_text='Wählen Sie eine Folge der Gewalt aus'
    )
    
    class Meta:
        model = Fall_FolgenDerGewalt
        fields = [
            'folge',
            'weitere_informationen',
        ]
        widgets = {
            'weitere_informationen': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Optionale zusätzliche Informationen zu dieser Folge...'
            }),
        }
        labels = {
            'folge': 'Folge der Gewalt',
            'weitere_informationen': 'Weitere Informationen',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize form with Fall instance.
        Fall is required for linking the consequence to the correct case.
        """
        self.fall = kwargs.pop('fall', None)
        super().__init__(*args, **kwargs)
        
        # Get the folge field (it's a ModelChoiceField with queryset attribute)
        folge_field = self.fields['folge']
        self.fields['weitere_informationen'].required = False
        
        # If adding new (not editing), exclude already linked consequences
        if self.fall and not self.instance.pk:
            # Get already linked consequence IDs
            existing_folgen_ids = Fall_FolgenDerGewalt.objects.filter(
                fall=self.fall
            ).values_list('folge_id', flat=True)
            
            # Exclude them from the queryset
            folge_field.queryset = FolgenDerGewalt.objects.exclude(  # type: ignore[union-attr]
                folge_id__in=existing_folgen_ids
            ).order_by('kategorie', 'name')
    
    def clean(self):
        """
        Validate that this consequence isn't already linked to the case.
        """
        cleaned_data = super().clean()
        folge = cleaned_data.get('folge')
        
        if self.fall and folge and not self.instance.pk:
            # Check for existing link
            if Fall_FolgenDerGewalt.objects.filter(fall=self.fall, folge=folge).exists():
                raise forms.ValidationError(
                    f'Die Folge "{folge.name}" ist bereits mit diesem Fall verknüpft.'
                )
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Override save to attach Fall before database commit.
        """
        folgen_relation = super().save(commit=False)
        
        if self.fall:
            folgen_relation.fall = self.fall
        
        if commit:
            folgen_relation.save()
        
        return folgen_relation
