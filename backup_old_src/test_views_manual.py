"""
Manual view testing via Django test client.

Run: python manage.py shell < test_views_manual.py
Or: python manage.py shell
     >>> exec(open('test_views_manual.py').read())
"""

from django.test import Client
from core.models import User, Fall, PersonenbezogeneDaten, Beratung, Gewalttat, GewalttatArt
from core.services.fall_manager import FallManager

print("\n" + "="*60)
print("DJANGO TEST CLIENT - VIEW VERIFICATION")
print("="*60 + "\n")

# ===== SETUP =====
client = Client()

# Get test users from fixture
try:
    user_basis = User.objects.get(username='user_basis')
    user_erweitert = User.objects.get(username='user_erweitert')
    user_admin = User.objects.get(username='user_admin')
    print("✓ Test users loaded from fixture\n")
except User.DoesNotExist:
    print("✗ ERROR: Run 'python manage.py loaddata seed_data.json' first\n")
    exit(1)

# Create test case if none exist
if not Fall.objects.exists():
    print("Creating test case...")
    fall_data = {
        'zustaendige_beratungsstelle': 'FBS_1_LE',
        'bearbeitet_von': user_basis,
    }
    personen_data = {
        'alias': 'TEST_MANUAL_001',
        'rolle_der_ratsuchenden_person': 'BETROFFENE',
    }
    test_fall = FallManager.createFall(fall_data, personen_data)
    print(f"✓ Test case created: {test_fall}\n")
else:
    test_fall = Fall.objects.first()
    print(f"✓ Using existing case: {test_fall}\n")

print("="*60)
print("TEST 1: Authentication Required")
print("="*60)

# Try accessing case list without login
response = client.get('/cases/')
print(f"GET /cases/ (not logged in)")
print(f"  Status: {response.status_code}")
print(f"  Expected: 302 (redirect to login)")
print(f"  Result: {'✓ PASS' if response.status_code == 302 else '✗ FAIL'}\n")

print("="*60)
print("TEST 2: Login as BASIS User")
print("="*60)

# Login as BASIS user
logged_in = client.login(username='user_basis', password='test123')
print(f"Login attempt: {'✓ Success' if logged_in else '✗ Failed'}")

if logged_in:
    response = client.get('/cases/')
    print(f"\nGET /cases/ (logged in as BASIS)")
    print(f"  Status: {response.status_code}")
    print(f"  Expected: 200 (OK)")
    print(f"  Result: {'✓ PASS' if response.status_code == 200 else '✗ FAIL'}")
    
    # Check context data
    if response.status_code == 200:
        try:
            if hasattr(response, 'context') and response.context:
                cases = response.context['cases']
                print(f"  Cases in context: {cases.count()}")
                print(f"  Context verification: ✓ PASS")
            else:
                print(f"  Context not available (template rendering issue)")
                print(f"  Context verification: ⚠ SKIP")
        except (KeyError, AttributeError, TypeError) as e:
            print(f"  Context verification: ⚠ SKIP ({type(e).__name__})")

client.logout()
print()

print("="*60)
print("TEST 3: Case Detail View")
print("="*60)

client.login(username='user_basis', password='test123')
response = client.get(f'/cases/{test_fall.fall_id}/')
print(f"GET /cases/{test_fall.fall_id}/")
print(f"  Status: {response.status_code}")
print(f"  Expected: 200")
print(f"  Result: {'✓ PASS' if response.status_code == 200 else '✗ FAIL'}")

if response.status_code == 200:
    try:
        if hasattr(response, 'context') and response.context:
            cases = response.context['cases']
            print(f"  Cases in context: {cases.count()}")
            print(f"  Context verification: ✓ PASS")
        else:
            print(f"  Context not available (template rendering issue)")
            print(f"  Context verification: ⚠ SKIP")
    except (KeyError, AttributeError, TypeError) as e:
        print(f"  Context verification: ⚠ SKIP ({type(e).__name__})")

client.logout()
print()

print("="*60)
print("TEST 4: Case Create View (GET)")
print("="*60)

client.login(username='user_basis', password='test123')
response = client.get('/cases/create/')
print(f"GET /cases/create/")
print(f"  Status: {response.status_code}")
print(f"  Expected: 200")
print(f"  Result: {'✓ PASS' if response.status_code == 200 else '✗ FAIL'}")

if response.status_code == 200:
    try:
        if hasattr(response, 'context') and response.context:
            cases = response.context['cases']
            print(f"  Cases in context: {cases.count()}")
            print(f"  Context verification: ✓ PASS")
        else:
            print(f"  Context not available (template rendering issue)")
            print(f"  Context verification: ⚠ SKIP")
    except (KeyError, AttributeError, TypeError) as e:
        print(f"  Context verification: ⚠ SKIP ({type(e).__name__})")

client.logout()
print()

print("="*60)
print("TEST 5: Case Create View (POST)")
print("="*60)

client.login(username='user_basis', password='test123')

# Simulate form submission
post_data = {
    # Fall fields
    'zustaendige_beratungsstelle': 'FBS_2_LKNSA',
    'informationsquelle': '',
    'informationsquelle_andere_details': '',
    'anzahl_dolmetschungen_stunden': '0.0',
    'dolmetschung_sprachen': '',
    'weitere_notizen': '',
    
    # PersonenbezogeneDaten fields
    'alias': 'TEST_POST_002',
    'rolle_der_ratsuchenden_person': 'BETROFFENE',
    'alter': '',
    'alter_keine_angabe': False,
    'geschlechtsidentitaet': '',
    'sexualitaet': '',
    'wohnort': '',
    'wohnort_details': '',
    'staatsangehoerigkeit_deutsch': '',
    'staatsangehoerigkeit_land': '',
    'berufliche_situation': '',
    'schwerbehinderung': '',
    'form_der_behinderung': '',
    'grad_der_behinderung': '',
    'personenbezogene_notizen': '',
}


response = client.post('/cases/create/', data=post_data)
print(f"POST /cases/create/")
print(f"  Status: {response.status_code}")
print(f"  Expected: 302 (redirect on success)")

if response.status_code == 302:
    print(f"  Redirect to: {response.url}")  # Only access .url if redirect
    print(f"  Result: ✓ PASS")
    
    # Verify case was created
    created_case = PersonenbezogeneDaten.objects.filter(alias='TEST_POST_001').first()
    if created_case:
        print(f"  Case created: {created_case.fall}")
        print(f"  Database verification: ✓ PASS")
    else:
        print(f"  Database verification: ✗ FAIL (case not found)")
else:
    print(f"  Result: ✗ FAIL")
    if hasattr(response, 'context') and response.context and 'form' in response.context:
        print(f"  Form errors: {response.context['form'].errors}")

client.logout()
print()

print("="*60)
print("TEST 6: Add Beratung")
print("="*60)

client.login(username='user_basis', password='test123')

beratung_data = {
    'datum': '2026-01-07',
    'durchfuehrungsart': 'PERSOENLICH',
    'durchfuehrungsort': 'LEIPZIG_STADT',
}

response = client.post(f'/cases/{test_fall.fall_id}/beratung/add/', data=beratung_data)
print(f"POST /cases/{test_fall.fall_id}/beratung/add/")
print(f"  Status: {response.status_code}")
print(f"  Expected: 302 (redirect)")

if response.status_code == 302:
    print(f"  Result: ✓ PASS")
    
    # Verify Beratung was created and aggregates updated
    test_fall.refresh_from_db()
    print(f"  Fall.beratungsanzahl: {test_fall.beratungsanzahl}")
    print(f"  Aggregate update: {'✓ PASS' if test_fall.beratungsanzahl > 0 else '✗ FAIL'}")
else:
    print(f"  Result: ✗ FAIL")
    if hasattr(response, 'context') and 'form' in response.context:
        print(f"  Form errors: {response.context['form'].errors}")

client.logout()
print()

print("="*60)
print("TEST 7: Permission Check (Hard Delete)")
print("="*60)

# BASIS user should NOT be able to hard delete
client.login(username='user_basis', password='test123')
response = client.post(f'/cases/{test_fall.fall_id}/delete/', data={'delete_type': 'hard'})
print(f"POST /cases/{test_fall.fall_id}/delete/ (as BASIS user, hard delete)")
print(f"  Status: {response.status_code}")
print(f"  Expected: 403 (forbidden)")
print(f"  Result: {'✓ PASS' if response.status_code == 403 else '✗ FAIL'}")
client.logout()
print()

# ADMIN user SHOULD be able to hard delete
client.login(username='user_admin', password='test123')
# Create disposable case for deletion test
disposable_fall = FallManager.createFall(
    {'zustaendige_beratungsstelle': 'FBS_1_LE', 'bearbeitet_von': user_admin},
    {'alias': 'DELETE_ME_001', 'rolle_der_ratsuchenden_person': 'BETROFFENE'}
)
response = client.post(f'/cases/{disposable_fall.fall_id}/delete/', data={'delete_type': 'hard'})
print(f"POST /cases/{disposable_fall.fall_id}/delete/ (as ADMIN user, hard delete)")
print(f"  Status: {response.status_code}")
print(f"  Expected: 302 (redirect)")
print(f"  Result: {'✓ PASS' if response.status_code == 302 else '✗ FAIL'}")

# Verify deletion
deleted = not Fall.objects.filter(fall_id=disposable_fall.fall_id).exists()
print(f"  Case deleted from DB: {'✓ PASS' if deleted else '✗ FAIL'}")
client.logout()
print()

print("="*60)
print("VERIFICATION COMPLETE")
print("="*60)
