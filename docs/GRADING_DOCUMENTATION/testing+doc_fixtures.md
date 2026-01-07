
====================================
### FIXTURES
===================================

Created a Django fixture file: a JSON file containing the initial database that Django can automatically load.
Reason:
Our forms need reference Data to work.
For example:
GewalttatForm has a multi-select dropdown for violence types -> needs GewalttatArt records in database
Login authentication -> needs User accounts to test with
Permission testing -> needs all 3 roles (BASIS/ERWEITERT/ADMIN) configured

Django has a built in way to load pre-defned data. without it, you'd have to manually create the 50+ Database records in shell or an interface before testing anything. 
The loaddata command reads the JSON file, creates records in the proper order and preserves the relationships

Another advantage is that the whole team has the same base during testing, and you can just reset it after

# 1. Generate password hash
python manage.py shell
>>> from django.contrib.auth.hashers import make_password
>>> print(make_password('test123'))
# Copy the output (starts with "pbkdf2_sha256$...")

# 2. Edit seed_data.json
# Replace all three "password" fields with the hash you just copied

# 3. Load the fixture
python manage.py loaddata seed_data.json


TL;DR:
Fixture = pre-made database records in JSON format. Run loaddata seed_data.json once after migrations to populate your database with 3 test users, all role configurations, and reference data from the Statistikbogen. This lets you immediately start testing forms without manually creating 50+ records.    


>>> python manage.py loaddata seed_data.json
Traceback (most recent call last):
  File "/usr/lib/python3.12/code.py", line 63, in runsource
    code = self.compile(source, filename, symbol)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/codeop.py", line 161, in __call__
    return _maybe_compile(self.compiler, source, filename, symbol)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/codeop.py", line 73, in _maybe_compile
    return compiler(source, filename, symbol, incomplete_input=False)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/codeop.py", line 126, in __call__
    codeob = compile(source, filename, symbol, flags, True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<console>", line 1
    python manage.py loaddata seed_data.json
           ^^^^^^
SyntaxError: invalid syntax
>>> 
[5]+  Stopped                 python manage.py shell
bash: syntax error near unexpected token `>'
bash: syntax error near unexpected token `>'
(venv) violet@PiltoversFinest:~/repos/WS2025-SE-Bellis-ev/src$ python manage.py loaddata seed_data.json
Installed 47 object(s) from 1 fixture(s)
(venv) violet@PiltoversFinest:~/repos/WS2025-SE-Bellis-ev/src$ python manage.py shell
Ctrl click to launch VS Code Native REPL
Python 3.12.3 (main, Nov  6 2025, 13:44:16) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from core.models import User, Role, GewalttatArt, FolgenDerGewalt
>>> 
>>> # Check counts
>>> User.objects.count()  # Should return 3
ld return 3
GewalttatArt.objects.count()  # Should return 18
FolgenDerGewalt.objects.count()  # Should return 20

# Test login works
from django.contrib.auth import authenticate
user = authenticate(username='user_basis', password='test123')
print(use5
>>> Role.objects.count()  # Should return 3
r.role.name)  # Should print: BASIS3

print(user.rol>>> GewalttatArt.objects.count()  # Should return 18
19
>>> FolgenDerGewalt.objects.count()  # Should return 20
20
>>> 
e.permissions.can_edit_cases)  # Should print: Tru>>> # Test login works
>>> from django.contrib.auth import authenticate
>>> user = authenticate(username='user_basis', password='test123')
e
print(user.role.permissions.can_hard_delete_cases)  # Should print: False

# Check hierarchy
art = GewalttatArt.objects.get(name='Sexuelle Belästigung')
print(art.unterkategorien.count())  # Should print: 3
>>> print(user.role.name)  # Should print: BASIS
BASIS
>>> print(user.role.permissions.can_edit_cases)  # Should print: True
True
>>> print(user.role.permissions.can_hard_delete_cases)  # Should print: False
False
>>> 
>>> # Check hierarchy
>>> art = GewalttatArt.objects.get(name='Sexuelle Belästigung')
>>> print(art.unterkategorien.count())  # Should print: 3
3


