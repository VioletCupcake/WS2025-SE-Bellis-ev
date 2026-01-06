
from django.contrib import admin
from core.models import GewalttatArt, FolgenDerGewalt

@admin.register(GewalttatArt)
class GewalttatArtAdmin(admin.ModelAdmin):
    list_display = ['name', 'ist_unterkategorie', 'hauptkategorie']
    search_fields = ['name']

@admin.register(FolgenDerGewalt)  
class FolgenDerGewaltAdmin(admin.ModelAdmin):
    list_display = ['name', 'kategorie', 'ist_unterkategorie']
    list_filter = ['kategorie']
