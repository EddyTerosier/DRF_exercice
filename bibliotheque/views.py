from datetime import date
from django.contrib.auth.models import User
from rest_framework import viewsets, filters, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Auteur, Livre
from .serializers import AuteurSerializer, LivreSerializer, UserSerializer, UserRegisterJWTSerializer
from .permissions import IsOwnerOrReadOnly

class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all().order_by("id")
    serializer_class = LivreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["titre"]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AuteurViewSet(viewsets.ModelViewSet):
    serializer_class = AuteurSerializer
    permission_classes = [IsAuthenticated]
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

class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class BasicExampleView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'user': str(request.user), 'auth': str(request.auth)})

class SessionExampleView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'user': str(request.user)})
    def post(self, request):
        return Response({'ok': True, 'user': str(request.user)})
    
class TokenExampleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'user': str(request.user)})
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        u = request.user
        return Response({'id': u.id, 'username': u.username, 'email': u.email})
    
class JWTRegisterView(CreateAPIView):
    serializer_class = UserRegisterJWTSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = RefreshToken.for_user(user)
        data = {
            "user": {"id": user.id, "username": user.username, "email": user.email},
            "access": str(tokens.access_token),
            "refresh": str(tokens)
        }
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)