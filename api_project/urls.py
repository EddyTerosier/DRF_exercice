from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from bibliotheque.views import LivreViewSet, AuteurViewSet, UserRegistrationView, BasicExampleView, SessionExampleView, TokenExampleView, ProfileView, JWTRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'livres', LivreViewSet, basename='livre')
router.register(r'auteurs', AuteurViewSet, basename='auteur')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('api/register/', UserRegistrationView.as_view()),
    path('basic-example/', BasicExampleView.as_view()),
    path('session-example/', SessionExampleView.as_view()),
    path('token-example/', TokenExampleView.as_view()),
    path('api/jwt/create/', TokenObtainPairView.as_view()),
    path('api/jwt/refresh/', TokenRefreshView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('api/jwt/register/', JWTRegisterView.as_view()),
    path('api/jwt/login/', TokenObtainPairView.as_view()),
]