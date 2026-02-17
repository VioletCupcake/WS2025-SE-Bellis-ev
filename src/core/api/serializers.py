"""
DRF Serializers for the Bellis REST API.
Maps Django models to JSON for the Quasar frontend.
"""
from rest_framework import serializers
from core.models import (
    Fall, PersonenbezogeneDaten, Beratung, Gewalttat, Anfrage,
    GewalttatArt, FolgenDerGewalt, Fall_FolgenDerGewalt
)


# ===== REFERENCE DATA =====

class GewalttatArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = GewalttatArt
        fields = ['art_id', 'name', 'ist_unterkategorie', 'hauptkategorie', 'beschreibung']


class FolgenDerGewaltSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolgenDerGewalt
        fields = ['folge_id', 'name', 'kategorie', 'ist_unterkategorie', 'hauptkategorie', 'beschreibung']


# ===== FALL (CASE) =====

class PersonenbezogeneDatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonenbezogeneDaten
        exclude = ['fall']


class FallListSerializer(serializers.ModelSerializer):
    """Kurzansicht für die Fälle-Liste."""
    alias = serializers.CharField(source='personenbezogene_daten.alias', read_only=True, default='')

    class Meta:
        model = Fall
        fields = [
            'fall_id', 'alias', 'zustaendige_beratungsstelle',
            'status', 'erstellungsdatum', 'beratungsanzahl'
        ]


class FallDetailSerializer(serializers.ModelSerializer):
    """Vollansicht mit verschachtelten PersonenbezogeneDaten."""
    personenbezogene_daten = PersonenbezogeneDatenSerializer(read_only=True)
    zustaendige_beratungsstelle_display = serializers.CharField(
        source='get_zustaendige_beratungsstelle_display', read_only=True
    )
    folgen = serializers.SerializerMethodField()

    class Meta:
        model = Fall
        fields = '__all__'

    def get_folgen(self, obj):
        relations = Fall_FolgenDerGewalt.objects.filter(fall=obj).select_related('folge')
        return [
            {
                'id': str(rel.folge.folge_id),
                'name': rel.folge.name,
                'kategorie': rel.folge.kategorie,
                'weitere_informationen': rel.weitere_informationen,
            }
            for rel in relations
        ]


class FallCreateSerializer(serializers.Serializer):
    """
    Flaches Format passend zum Frontend-Formular.
    Erstellt Fall + PersonenbezogeneDaten zusammen.
    """
    # Fall fields
    zustaendige_beratungsstelle = serializers.CharField()
    informationsquelle = serializers.CharField(required=False, allow_blank=True)
    informationsquelle_andere_details = serializers.CharField(required=False, allow_blank=True)
    dolmetschung_in_anspruch_genommen = serializers.BooleanField(required=False, default=False)
    anzahl_dolmetschungen_stunden = serializers.FloatField(required=False, default=0.0)
    dolmetschung_sprachen = serializers.CharField(required=False, allow_blank=True)
    weitere_notizen = serializers.CharField(required=False, allow_blank=True)

    # PersonenbezogeneDaten fields
    alias = serializers.CharField()
    rolle_der_ratsuchenden_person = serializers.CharField()
    alter = serializers.IntegerField(required=False, allow_null=True)
    alter_keine_angabe = serializers.BooleanField(required=False, default=False)
    geschlechtsidentitaet = serializers.CharField(required=False, allow_blank=True)
    sexualitaet = serializers.CharField(required=False, allow_blank=True)
    wohnort = serializers.CharField(required=False, allow_blank=True)
    wohnort_details = serializers.CharField(required=False, allow_blank=True)
    staatsangehoerigkeit_deutsch = serializers.CharField(required=False, allow_blank=True)
    staatsangehoerigkeit_land = serializers.CharField(required=False, allow_blank=True)
    berufliche_situation = serializers.CharField(required=False, allow_blank=True)
    schwerbehinderung = serializers.CharField(required=False, allow_blank=True)
    form_der_behinderung = serializers.CharField(required=False, allow_blank=True)
    grad_der_behinderung = serializers.IntegerField(required=False, allow_null=True)
    personenbezogene_notizen = serializers.CharField(required=False, allow_blank=True)

    # Gewalttat fields (embedded in the same form)
    alter_zum_zeitpunkt_der_tat = serializers.IntegerField(required=False, allow_null=True)
    alter_tat_keine_angabe = serializers.BooleanField(required=False, default=False)
    zeitraum_von = serializers.DateField(required=False, allow_null=True)
    zeitraum_bis = serializers.DateField(required=False, allow_null=True)
    zeitraum_keine_angabe = serializers.BooleanField(required=False, default=False)
    tatort = serializers.CharField(required=False, allow_blank=True)
    gewalt_notizen = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        # Split data into Fall, PersonenbezogeneDaten, and Gewalttat fields
        fall_fields = {
            'zustaendige_beratungsstelle': validated_data.get('zustaendige_beratungsstelle', ''),
            'informationsquelle': validated_data.get('informationsquelle', ''),
            'informationsquelle_andere_details': validated_data.get('informationsquelle_andere_details', ''),
            'anzahl_dolmetschungen_stunden': validated_data.get('anzahl_dolmetschungen_stunden', 0.0),
            'dolmetschung_sprachen': validated_data.get('dolmetschung_sprachen', ''),
            'weitere_notizen': validated_data.get('weitere_notizen', ''),
        }

        person_fields = {
            'alias': validated_data['alias'],
            'rolle_der_ratsuchenden_person': validated_data['rolle_der_ratsuchenden_person'],
            'alter': validated_data.get('alter'),
            'alter_keine_angabe': validated_data.get('alter_keine_angabe', False),
            'geschlechtsidentitaet': validated_data.get('geschlechtsidentitaet', ''),
            'sexualitaet': validated_data.get('sexualitaet', ''),
            'wohnort': validated_data.get('wohnort', ''),
            'wohnort_details': validated_data.get('wohnort_details', ''),
            'staatsangehoerigkeit_deutsch': validated_data.get('staatsangehoerigkeit_deutsch', ''),
            'staatsangehoerigkeit_land': validated_data.get('staatsangehoerigkeit_land', ''),
            'berufliche_situation': validated_data.get('berufliche_situation', ''),
            'schwerbehinderung': validated_data.get('schwerbehinderung', ''),
            'form_der_behinderung': validated_data.get('form_der_behinderung', ''),
            'grad_der_behinderung': validated_data.get('grad_der_behinderung'),
            'personenbezogene_notizen': validated_data.get('personenbezogene_notizen', ''),
        }

        # Create Fall
        fall = Fall.objects.create(**fall_fields)

        # Create PersonenbezogeneDaten linked to Fall
        PersonenbezogeneDaten.objects.create(fall=fall, **person_fields)

        # Create Gewalttat if any gewalttat data is provided
        gewalttat_data = {}
        for field in ['alter_zum_zeitpunkt_der_tat', 'alter_tat_keine_angabe',
                       'zeitraum_von', 'zeitraum_bis', 'zeitraum_keine_angabe',
                       'tatort', 'gewalt_notizen']:
            val = validated_data.get(field)
            if val not in (None, '', False):
                gewalttat_data[field] = val

        if gewalttat_data:
            Gewalttat.objects.create(fall=fall, **gewalttat_data)

        return fall


class FallUpdateSerializer(serializers.ModelSerializer):
    """Für PUT /api/fall/<id>/ – aktualisiert Fall-Felder."""
    class Meta:
        model = Fall
        fields = [
            'zustaendige_beratungsstelle', 'informationsquelle',
            'informationsquelle_andere_details',
            'anzahl_dolmetschungen_stunden', 'dolmetschung_sprachen',
            'weitere_notizen'
        ]


# ===== BERATUNG =====

class BeratungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beratung
        fields = '__all__'
        read_only_fields = ['beratung_id']


# ===== ANFRAGE =====

class AnfrageCreateSerializer(serializers.Serializer):
    """
    Serializer der das Frontend-Format für Anfragen akzeptiert.
    Frontend sendet camelCase-Felder, hier mappen wir auf die Model-Felder.
    """
    wie = serializers.CharField()
    datumAnfrage = serializers.DateField()
    anfrageAus = serializers.CharField()
    werHatAngefragt = serializers.CharField()
    artDerAnfrage = serializers.CharField()
    terminVergeben = serializers.BooleanField(default=False)
    terminDatum = serializers.DateField(required=False, allow_null=True)
    terminOrt = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    notizen = serializers.CharField(required=False, allow_blank=True, default='')
    dolmetscherStunden = serializers.FloatField(required=False, allow_null=True)
    dolmetscherSprachen = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )

    def _map_wie(self, value):
        """Map frontend display value to model choice key."""
        mapping = {
            'Telefon': 'TELEFON',
            'E-Mail': 'EMAIL',
            'Persönlich': 'ANDERE',
        }
        return mapping.get(value, value)

    def _map_anfrage_aus(self, value):
        mapping = {
            'Leipzig Stadt': 'LEIPZIG_STADT',
            'Leipzig Land': 'LEIPZIG_LAND',
            'Nordsachsen': 'NORDSACHSEN',
            'Sachsen': 'SACHSEN',
            'andere': 'ANDERE',
        }
        return mapping.get(value, value)

    def _map_wer_hat_angefragt(self, value):
        mapping = {
            'Fachkraft': 'F',
            'Angehörige:r': 'A',
            'Betroffene:r': 'B',
            'Anonym': 'ANONYM',
            'queer Betroffene:r': 'QB',
            'queer Fachkraft': 'QF',
            'queer Angehörige:r': 'QA',
            'queer anonym': 'Q_ANONYM',
            'Fachkraft für Betroffene': 'FFB',
            'Angehörige:r für Betroffene': 'AFB',
            'Fachkraft für queere Betroffene': 'FFQB',
            'Angehörige für queere Betroffene': 'AFQB',
        }
        return mapping.get(value, value)

    def _map_art_der_anfrage(self, value):
        mapping = {
            'medizinische Soforthilfe': 'MEDIZINISCHE_SOFORTHILFE',
            'Vertrauliche Spurensicherung': 'VERTRAULICHE_SPURENSICHERUNG',
            'Beratungsbedarf': 'BERATUNGSBEDARF',
            'zu Rechtlichem': 'ZU_RECHTLICHEN',
            'Sonstiges': 'SONSTIGES',
        }
        return mapping.get(value, value)

    def _map_termin_ort(self, value):
        mapping = {
            'Leipzig Stadt': 'LEIPZIG_STADT',
            'Leipzig Land': 'LEIPZIG_NORD',
            'Nordsachsen': 'NORDSACHSEN',
        }
        return mapping.get(value, value)

    def create(self, validated_data):
        sprachen = validated_data.get('dolmetscherSprachen', [])

        anfrage = Anfrage.objects.create(
            wie=self._map_wie(validated_data['wie']),
            datum_anfrage=validated_data['datumAnfrage'],
            anfrage_aus=self._map_anfrage_aus(validated_data['anfrageAus']),
            wer_hat_angefragt=self._map_wer_hat_angefragt(validated_data['werHatAngefragt']),
            art_der_anfrage=self._map_art_der_anfrage(validated_data['artDerAnfrage']),
            termin_vergeben=validated_data.get('terminVergeben', False),
            termin_datum=validated_data.get('terminDatum'),
            termin_ort=self._map_termin_ort(validated_data.get('terminOrt', '') or ''),
        )
        return anfrage


# ===== FALL-FOLGEN JUNCTION =====

class FallFolgenCreateSerializer(serializers.Serializer):
    """Für POST /api/fall/<id>/folge/ – verknüpft eine Folge mit einem Fall."""
    folge = serializers.UUIDField()
    weitere_informationen = serializers.CharField(required=False, allow_blank=True, default='')

    def create(self, validated_data):
        fall = self.context['fall']
        folge = FolgenDerGewalt.objects.get(folge_id=validated_data['folge'])
        relation = Fall_FolgenDerGewalt.objects.create(
            fall=fall,
            folge=folge,
            weitere_informationen=validated_data.get('weitere_informationen', '')
        )
        return relation
