from django.core.management.base import BaseCommand
from core.models import GewalttatArt, FolgenDerGewalt

class Command(BaseCommand):
    help = 'Populates initial reference data (Gewalttat Arten and Folgen der Gewalt) matching Frontend choices'

    def handle(self, *args, **options):
        self.stdout.write('Populating reference data...')
        
        # 1. GEWALTTAT ARTEN
        # Defined in frontend/src/services/choices.js as GEWALTTAT_ART_CHOICES
        gewalttat_arten = [
            {'name': 'SEXUELLE_BELAESTIGUNG_OEFFENTLICH', 'beschreibung': 'Sexuelle Belästigung – im öffentlichen Raum'},
            {'name': 'SEXUELLE_BELAESTIGUNG_ARBEIT', 'beschreibung': 'Sexuelle Belästigung – am Arbeitsplatz'},
            {'name': 'SEXUELLE_BELAESTIGUNG_PRIVAT', 'beschreibung': 'Sexuelle Belästigung – im Privaten'},
            {'name': 'VERGEWALTIGUNG', 'beschreibung': 'Vergewaltigung'},
            {'name': 'VERSUCHTE_VERGEWALTIGUNG', 'beschreibung': 'Versuchte Vergewaltigung'},
            {'name': 'SEXUELLER_MISSBRAUCH', 'beschreibung': 'Sexueller Missbrauch'},
            {'name': 'SEXUELLER_MISSBRAUCH_KINDHEIT', 'beschreibung': 'Sexueller Missbrauch in der Kindheit'},
            {'name': 'SEXUELLE_NOETIGUNG', 'beschreibung': 'Sexuelle Nötigung'},
            {'name': 'RITUELLE_GEWAELT', 'beschreibung': 'Rituelle Gewalt'},
            {'name': 'ZWANGSPROSTITUTION', 'beschreibung': 'Zwangsprostitution'},
            {'name': 'SEXUELLE_AUSBEUTUNG', 'beschreibung': 'Sexuelle Ausbeutung'},
            {'name': 'UPSKIRTING', 'beschreibung': 'Upskirting'},
            {'name': 'CATCALLING', 'beschreibung': 'Catcalling'},
            {'name': 'DIGITALE_SEXUELLE_GEWAELT', 'beschreibung': 'Digitale sexuelle Gewalt'},
            {'name': 'SPIKING', 'beschreibung': 'Spiking'},
            {'name': 'ANDERE', 'beschreibung': 'Andere'},
            {'name': 'KEINE_ANGABE', 'beschreibung': 'Keine Angabe'},
        ]

        count_created = 0
        for item in gewalttat_arten:
            obj, created = GewalttatArt.objects.get_or_create(
                name=item['name'],
                defaults={'beschreibung': item['beschreibung']}
            )
            if created:
                count_created += 1
        
        self.stdout.write(f'Created {count_created} Gewalttat Arten.')

        # 2. FOLGEN DER GEWALT
        # Defined in frontend/src/services/choices.js as FOLGE_DER_GEWAELT_CHOICES
        
        folgen_data = [
            {
                'kategorie': 'PSYCHISCH',
                'children': [
                    {'name': 'DEPRESSION', 'beschreibung': 'Depression'},
                    {'name': 'ANGSTSTOERUNG', 'beschreibung': 'Angststörung'},
                    {'name': 'PTBS', 'beschreibung': 'PTBS'},
                    {'name': 'ANDERE_DIAGNOSE', 'beschreibung': 'andere Diagnose'},
                    {'name': 'BURNOUT', 'beschreibung': 'Burn-Out'},
                    {'name': 'SCHLAFSTOERUNG', 'beschreibung': 'Schlafstörungen'},
                    {'name': 'SUCHT', 'beschreibung': 'Sucht/Abhängigkeit'},
                    {'name': 'KOMMUNIKATION', 'beschreibung': 'Kommunikationsschwierigkeiten'},
                    {'name': 'VERNACHLAESSIGUNG', 'beschreibung': 'Vernachlässigung alltäglicher Dinge'},
                ]
            },
            {
                'kategorie': 'KOERPERLICH',
                'children': [
                    {'name': 'SCHMERZEN', 'beschreibung': 'Schmerzen'},
                    {'name': 'LAHMUNGEN', 'beschreibung': 'Lähmungen'},
                    {'name': 'KRANKHEIT', 'beschreibung': 'Krankheit'},
                ]
            },
            {
                'kategorie': 'DAUERHAFT',
                'children': [
                     {'name': 'DAUERHAFT_KOERPERLICH', 'beschreibung': 'Dauerhafte körperliche Beeinträchtigung'}
                ]
            },
            {
                'kategorie': 'FINANZIELL',
                 'children': [
                     {'name': 'FINANZIELL', 'beschreibung': 'Finanzielle Folgen'},
                     {'name': 'ARBEIT', 'beschreibung': 'Arbeitseinschränkung/Arbeitsunfähigkeit'},
                     {'name': 'VERLUST_ARBEIT', 'beschreibung': 'Verlust Arbeitsstelle'},
                     {'name': 'SOZIALE_ISOLATION', 'beschreibung': 'Soziale Isolation'},
                     {'name': 'SUIZIDALITAET', 'beschreibung': 'Suizidalität'},
                     {'name': 'WEITERES', 'beschreibung': 'Weiteres'},
                     {'name': 'KEINE_ANGABE', 'beschreibung': 'Keine Angabe'},
                 ]
            }
        ]

        count_folgen = 0
        for group in folgen_data:
            kat = group['kategorie'] 
            
            for item in group['children']:
                obj, created = FolgenDerGewalt.objects.get_or_create(
                    name=item['name'],
                    defaults={
                        'beschreibung': item['beschreibung'],
                        'kategorie': kat
                    }
                )
                if created:
                    count_folgen += 1
        
        self.stdout.write(f'Created {count_folgen} Folgen der Gewalt.')
        self.stdout.write(self.style.SUCCESS('Successfully populated reference data.'))
