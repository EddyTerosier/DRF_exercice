from django.contrib import admin
from .models import Auteur, Livre

# Register your models here.

@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "nationalite")
    search_fields = ("nom", "prenom", "nationalite")

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ("titre", "auteur", "theme", "note", "disponible")
    list_filter = ("disponible", "theme")
    search_fields = ("titre", "auteur__nom", "auteur__prenom", "theme")