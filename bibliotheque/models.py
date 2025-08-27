from django.db import models

# Create your models here.

class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True)
    nationalite = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(null=True, blank=True)

    def __str__(self):
        full = f"{self.prenom} {self.nom}".strip()
        return full or self.nom

class Livre(models.Model):
    THEME_MAX_LEN = 100
    titre = models.CharField(max_length=200)
    theme = models.CharField(max_length=THEME_MAX_LEN, blank=True)
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE, related_name="livres")
    note = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    disponible = models.BooleanField(default=True)
    date_publication = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.titre} — {self.auteur}"