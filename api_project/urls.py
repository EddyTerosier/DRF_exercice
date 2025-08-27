from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from bibliotheque.views import LivreViewSet, AuteurViewSet

router = DefaultRouter()
router.register(r'livres', LivreViewSet, basename='livre')
router.register(r'auteurs', AuteurViewSet, basename='auteur')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
]
