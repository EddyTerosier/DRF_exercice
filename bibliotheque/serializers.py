from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Auteur, Livre

class LivreSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Livre
        fields = ["id", "titre", "theme", "auteur", "note", "disponible", "date_publication", "owner"]

class AuteurSerializer(serializers.ModelSerializer):
    livres = LivreSerializer(many=True, read_only=True)
    class Meta:
        model = Auteur
        fields = ["id", "nom", "prenom", "nationalite", "date_naissance", "livres"]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserRegisterJWTSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)