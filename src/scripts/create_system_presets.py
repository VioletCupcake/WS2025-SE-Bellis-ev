
from core.models import StatistikPreset

presets_data = [
    {
        'name': 'FBS Leipzig Stadt (Statistik)',
        'filter_config': {
            'beratungsstellen': ['FBS_1_LE'],
            'modules': ['personen', 'beratung', 'gewalttat', 'folgen', 'anfragen']
        }
    },
    {
        'name': 'Fachberatung gegen sexualisierte Gewalt im Landkreis Nordsachsen',
        'filter_config': {
            'beratungsstellen': ['FBS_2_LKNSA'],
            'modules': ['personen', 'beratung', 'gewalttat', 'folgen', 'anfragen']
        }
    },
    {
        'name': 'Fachberatung gegen sexualisierte Gewalt im Landkreis Leipzig',
        'filter_config': {
            'beratungsstellen': ['FBS_3_LKLE'],
            'modules': ['personen', 'beratung', 'gewalttat', 'folgen', 'anfragen']
        }
    }
]

for p in presets_data:
    preset, created = StatistikPreset.objects.get_or_create(
        name=p['name'],
        defaults={
            'filter_config': p['filter_config'],
            'ist_global': True,
            'ist_system_preset': True
        }
    )
    if created:
        print(f"Created preset: {p['name']}")
    else:
        print(f"Preset exists: {p['name']}")
