from datetime import date
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Auteur, Livre
from .serializers import AuteurSerializer, LivreSerializer

class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all().order_by("id")
    serializer_class = LivreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titre']

class AuteurViewSet(viewsets.ModelViewSet):
    serializer_class = AuteurSerializer

    def get_queryset(self):
        qs = Auteur.objects.all().order_by("id")
        year = self.request.query_params.get("year")
        if year and year.isdigit():
            cutoff = date(int(year), 12, 31)
            qs = qs.filter(date_naissance__gt=cutoff)
        return qs

    @action(detail=True, methods=["get"], url_path="titres")
    def titres(self, request, pk=None):
        auteur = self.get_object()
        titres = list(auteur.livres.values_list("titre", flat=True))
        return Response({"titres": titres})