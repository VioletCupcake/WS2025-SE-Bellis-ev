from django.db import migrations

def assign_permissions(apps, schema_editor):
    User = apps.get_model('core', 'User')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    try:
        # Get user
        user = User.objects.get(username='user_erweitert')
        
        # Get content types
        gewalttat_ct = ContentType.objects.get(app_label='core', model='gewalttatart')
        folgen_ct = ContentType.objects.get(app_label='core', model='folgendergewalt')
        
        # Get permissions
        perms = Permission.objects.filter(
            content_type__in=[gewalttat_ct, folgen_ct]
        )
        
        # Assign
        user.user_permissions.set(perms)
    except User.DoesNotExist:
        pass  # User not created yet

def reverse_permissions(apps, schema_editor):
    User = apps.get_model('core', 'User')
    try:
        user = User.objects.get(username='user_erweitert')
        user.user_permissions.clear()
    except User.DoesNotExist:
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_add_gewalttat_arten_m2m'),  
    ]

    operations = [
        migrations.RunPython(assign_permissions, reverse_permissions),
    ]
