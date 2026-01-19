"""
Forms for Gewalttat (Violence Incident) management.

Most complex form in MVP - handles 18+ fields, M2M relationships,
and JSON validation for perpetrator details.
Also the form where we finally got the dynamic formset working lol
"""

import json
from django import forms
from django.core.exceptions import ValidationError
from core.models import Gewalttat, GewalttatArt
from core.models.fall_models import PersonenbezogeneDaten
from core.validators.json_validators import validate_taeterinnen_details


# choices for taeterinnen dynamic formset - reuse from PersonenbezogeneDaten
TAETER_GESCHLECHT_CHOICES = [('', '-- Geschlecht --')] + list(PersonenbezogeneDaten.GESCHLECHT_CHOICES)

# from the json validator, but as proper choices now
TAETER_VERHAELTNIS_CHOICES = [
    ('', '-- Verhältnis --'),
    ('Unbekannte:r', 'Unbekannte:r'),
    ('Bekannte:r', 'Bekannte:r'),
    ('Partner:in', 'Partner:in'),
    ('Partner:in ehemalig', 'Partner:in ehemalig'),
    ('Ehepartner:in oder eingetragene:r Lebenspartner:in', 'Ehepartner:in oder eingetragene:r Lebenspartner:in'),
    ('andere Familienangehörige', 'andere Familienangehörige'),
    ('sonstige Personen', 'sonstige Personen'),
    ('keine Angabe', 'keine Angabe'),
]


class GewalttatForm(forms.ModelForm):
    """
    Form for adding/editing violence incidents.
    
    Handles:
    - 18+ incident fields
    - Many-to-many violence types (GewalttatArt) with hierarchical checkboxes
    - JSON perpetrator details via dynamic formset (way better UX than raw JSON lol)
    - Complex cross-field validation rules
    """
    
    # Override M2M field to use checkboxes instead of default multi-select
    # template renders these hierarchically with JS for subcategory handling
    gewalttat_arten = forms.ModelMultipleChoiceField(
        queryset=GewalttatArt.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Art der Gewalt",
        required=False,
        help_text="Mehrfachauswahl möglich"
    )
    
    # Hidden field that receives JSON from the dynamic formset JS
    # the actual input comes from the dynamic rows, this just holds the serialized result
    taeterinnen_details = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    class Meta:
        model = Gewalttat
        fields = [
            'alter_zum_zeitpunkt_der_tat',
            'alter_tat_keine_angabe',
            'zeitraum_von',
            'zeitraum_bis',
            'zeitraum_keine_angabe',
            'zahl_der_vorfaelle',
            'zahl_der_vorfaelle_genau',
            'anzahl_taeterinnen',
            'anzahl_taeterinnen_genau',
            'taeterinnen_details',
            'gewalttat_arten',  # M2M field
            'art_der_gewalt_andere_details',
            'tatort',
            'anzeige',
            'medizinische_versorgung',
            'vertrauliche_spurensicherung',
            'mitbetroffene_kinder',
            'davon_direkt_betroffen',
            'gewalt_notizen',
        ]
        widgets = {
            'alter_zum_zeitpunkt_der_tat': forms.NumberInput(attrs={'class': 'form-control'}), 
            'alter_tat_keine_angabe': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'zeitraum_von': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'zeitraum_bis': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'zeitraum_keine_angabe': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'zahl_der_vorfaelle': forms.Select(attrs={'class': 'form-control'}),
            'zahl_der_vorfaelle_genau': forms.NumberInput(attrs={'class': 'form-control'}),
            'anzahl_taeterinnen': forms.Select(attrs={'class': 'form-control'}),
            'anzahl_taeterinnen_genau': forms.NumberInput(attrs={'class': 'form-control'}),
            'art_der_gewalt_andere_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tatort': forms.Select(attrs={'class': 'form-control'}),
            'anzeige': forms.Select(attrs={'class': 'form-control'}),
            'medizinische_versorgung': forms.Select(attrs={'class': 'form-control'}),
            'vertrauliche_spurensicherung': forms.Select(attrs={'class': 'form-control'}),
            'mitbetroffene_kinder': forms.NumberInput(attrs={'class': 'form-control'}),
            'davon_direkt_betroffen': forms.NumberInput(attrs={'class': 'form-control'}),
            'gewalt_notizen': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'alter_zum_zeitpunkt_der_tat': 'Alter zum Zeitpunkt der Tat', 
            'alter_tat_keine_angabe': 'Alter - keine Angabe',
            'zeitraum_von': 'Zeitraum von',
            'zeitraum_bis': 'Zeitraum bis',
            'zeitraum_keine_angabe': 'Zeitraum - keine Angabe',
            'zahl_der_vorfaelle': 'Zahl der Vorfälle',
            'zahl_der_vorfaelle_genau': 'Zahl der Vorfälle (genaue Zahl)',
            'anzahl_taeterinnen': 'Anzahl Täter:innen',
            'anzahl_taeterinnen_genau': 'Anzahl Täter:innen (genaue Zahl)',
            'art_der_gewalt_andere_details': 'Art der Gewalt - Andere (Details)',
            'tatort': 'Tatort',
            'anzeige': 'Anzeige',
            'medizinische_versorgung': 'Medizinische Versorgung',
            'vertrauliche_spurensicherung': 'Vertrauliche Spurensicherung',
            'mitbetroffene_kinder': 'Mitbetroffene Kinder',
            'davon_direkt_betroffen': 'Davon direkt betroffen',
            'gewalt_notizen': 'Weitere Notizen',
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize form with Fall instance for linking."""
        self.fall = kwargs.pop('fall', None)
        super().__init__(*args, **kwargs)
        
        # Set field requirements
        self.fields['zahl_der_vorfaelle'].required = False
        self.fields['anzahl_taeterinnen'].required = False
        self.fields['tatort'].required = False
        self.fields['anzeige'].required = False
        
        # Build hierarchical structure for gewalttat_arten rendering
        # template uses this to show parent/child checkbox relationships
        self._build_gewalttat_hierarchy()
    
    def _build_gewalttat_hierarchy(self):
        """
        Prepares hierarchical data for gewalttat_arten checkboxes.
        Groups main categories with their subcategories for proper rendering.
        Basically the secret sauce for the conditional subcategory display
        """
        all_arten = GewalttatArt.objects.all().order_by('name')
        
        # separate main categories from subcategories
        main_categories = []
        subcategories_map = {}  # hauptkategorie_id -> [subcats]
        
        for art in all_arten:
            if not art.ist_unterkategorie:
                main_categories.append(art)
                subcategories_map[str(art.art_id)] = []
            else:
                parent_id = str(art.hauptkategorie_id) if art.hauptkategorie_id else None
                if parent_id and parent_id in subcategories_map:
                    subcategories_map[parent_id].append(art)
        
        # store for template access
        self.gewalttat_hierarchy = {
            'main_categories': main_categories,
            'subcategories_map': subcategories_map,
        }
        
        # find the Sexuelle Belästigung category for JS reference
        # need this id in template for conditional subcategory logic
        self.sexuelle_belaestigung_id = None
        for art in main_categories:
            if 'Sexuelle Belästigung' in art.name and not art.ist_unterkategorie:
                self.sexuelle_belaestigung_id = str(art.art_id)
                break
    
    def clean_taeterinnen_details(self):
        """
        Validate JSON structure for perpetrator details.
        Converts string input to Python list/dict and validates schema.
        """
        raw_data = self.cleaned_data.get('taeterinnen_details', '')
        
        # Empty is valid (not required field)
        if not raw_data or not raw_data.strip():
            return []
        
        # Try to parse JSON
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError as e:
            raise ValidationError(f"Ungültiges JSON-Format: {str(e)}")
        
        # Validate schema using custom validator
        try:
            validate_taeterinnen_details(data)
        except ValidationError as e:
            raise ValidationError(f"JSON-Schema-Fehler: {e.message}")
        
        return data
    
    def clean(self):
        """
        Cross-field validation.
        Implements conditional field requirements from Gewalttat model.
        """
        cleaned_data = super().clean()
        
        # reject completely empty submissions
        meaningful_fields = [
            cleaned_data.get('alter_zum_zeitpunkt_der_tat'),
            cleaned_data.get('zeitraum_von'),
            cleaned_data.get('zeitraum_bis'),
            cleaned_data.get('zahl_der_vorfaelle'),
            cleaned_data.get('anzahl_taeterinnen'),
            cleaned_data.get('tatort'),
            cleaned_data.get('anzeige'),
            cleaned_data.get('medizinische_versorgung'),
            cleaned_data.get('vertrauliche_spurensicherung'),
            cleaned_data.get('gewalt_notizen'),
        ]
        has_arten = bool(cleaned_data.get('gewalttat_arten'))
        has_data = any(f is not None and f != '' for f in meaningful_fields) or has_arten
        
        if not has_data:
            raise ValidationError('Mindestens ein Feld muss ausgefüllt werden.')
        
        # Validate: zahl_der_vorfaelle="GENAUE_ZAHL" requires zahl_der_vorfaelle_genau
        if cleaned_data.get('zahl_der_vorfaelle') == 'GENAUE_ZAHL':
            if not cleaned_data.get('zahl_der_vorfaelle_genau'):
                self.add_error(
                    'zahl_der_vorfaelle_genau',
                    'Genaue Zahl erforderlich bei Auswahl "genaue Zahl"'
                )
        
        # Validate: anzahl_taeterinnen="GENAUE_ZAHL" requires anzahl_taeterinnen_genau
        if cleaned_data.get('anzahl_taeterinnen') == 'GENAUE_ZAHL':
            if not cleaned_data.get('anzahl_taeterinnen_genau'):
                self.add_error(
                    'anzahl_taeterinnen_genau',
                    'Genaue Zahl erforderlich bei Auswahl "genaue Zahl"'
                )
        
        # Validate: zeitraum_von <= zeitraum_bis
        zeitraum_von = cleaned_data.get('zeitraum_von')
        zeitraum_bis = cleaned_data.get('zeitraum_bis')
        if zeitraum_von and zeitraum_bis:
            if zeitraum_von > zeitraum_bis:
                self.add_error(
                    'zeitraum_von',
                    'Startdatum muss vor oder gleich Enddatum sein'
                )
        
        # Validate: davon_direkt_betroffen <= mitbetroffene_kinder
        mitbetroffene = cleaned_data.get('mitbetroffene_kinder', 0)
        direkt_betroffen = cleaned_data.get('davon_direkt_betroffen', 0)
        if direkt_betroffen > mitbetroffene:
            self.add_error(
                'davon_direkt_betroffen',
                'Kann nicht größer sein als mitbetroffene Kinder'
            )
        
        # Validate: alter_tat_keine_angabe=True requires alter_zum_zeitpunkt_der_tat=None
        if cleaned_data.get('alter_tat_keine_angabe'):
            if cleaned_data.get('alter_zum_zeitpunkt_der_tat') is not None:
                self.add_error(
                    'alter_zum_zeitpunkt_der_tat',
                    'Alter muss leer sein wenn "keine Angabe" ausgewählt'
                )
        
        # Validate: zeitraum_keine_angabe=True requires both dates=None
        if cleaned_data.get('zeitraum_keine_angabe'):
            if zeitraum_von or zeitraum_bis:
                self.add_error(
                    'zeitraum_von',
                    'Zeitraum-Felder müssen leer sein wenn "keine Angabe" ausgewählt'
                )
        
        # Validate: if "Sexuelle Belästigung" selected, at least one subcategory required
        # this is the conditional subcategory logic server-side
        selected_arten = cleaned_data.get('gewalttat_arten', [])
        if selected_arten and self.sexuelle_belaestigung_id:
            selected_ids = [str(art.art_id) for art in selected_arten]
            
            if self.sexuelle_belaestigung_id in selected_ids:
                # check if any subcategory is also selected
                subcats = self.gewalttat_hierarchy['subcategories_map'].get(self.sexuelle_belaestigung_id, [])
                subcat_ids = [str(s.art_id) for s in subcats]
                has_subcat = any(sid in selected_ids for sid in subcat_ids)
                
                if not has_subcat:
                    self.add_error(
                        'gewalttat_arten',
                        'Bei "Sexuelle Belästigung" muss mindestens eine Unterkategorie ausgewählt werden '
                        '(öffentlicher Raum, Arbeitsplatz oder Privat)'
                    )
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Override save to attach Fall before database commit.
        M2M relationships (gewalttat_arten) saved automatically by Django.
        """
        gewalttat = super().save(commit=False)
        
        if self.fall:
            gewalttat.fall = self.fall
        
        if commit:
            gewalttat.save()
            # Save M2M relationships (must happen after instance is saved)
            self.save_m2m()
        
        return gewalttat
