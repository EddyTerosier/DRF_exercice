# README — Tester l’API DRF « Bibliothèque »

Ce guide explique comment **lancer** et **tester** l’API avec toutes les authentifications vues en cours (Basic, Session+CSRF, Token, JWT, inscription+login JWT), ainsi que les endpoints métiers (livres/auteurs), la recherche, le filtrage, la pagination et l’action personnalisée.

---

## 1) Prérequis & mise en route

```bash
# 1) Créer / activer l’environnement
python -m venv .venv
# Windows PowerShell
. .venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate

# 2) Installer les dépendances
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers

# 3) Migrations + superuser
python manage.py migrate
python manage.py createsuperuser

# 4) Démarrer
python manage.py runserver
# → http://127.0.0.1:8000/
```

**CORS** : `http://localhost:3000` autorisé si un front local est utilisé.  
**Pagination** : `PageNumberPagination` avec `PAGE_SIZE = 5` (ajoutez `?page=2`).

---

## 2) Endpoints « métier »

- **Livres** : `GET/POST` `/livres/`, `GET/PATCH/DELETE` `/livres/{id}/`  
  - Recherche : `/livres/?search=python`
- **Auteurs** : `GET/POST` `/auteurs/`, `GET/PATCH/DELETE` `/auteurs/{id}/`  
  - Filtre année (nés **après** l’année donnée) : `/auteurs/?year=1980`
  - Action personnalisée (titres) : `/auteurs/{id}/titres/`

### Exemples JSON
Créer un **auteur** :
```json
{
  "nom": "Hugo",
  "prenom": "Victor",
  "nationalite": "Française",
  "date_naissance": "1802-02-26"
}
```
Créer un **livre** (remplacez `1` par l’ID d’un auteur) :
```json
{
  "titre": "Les Misérables",
  "theme": "Roman",
  "auteur": 1,
  "note": "9.5",
  "disponible": true,
  "date_publication": "1862-01-01"
}
```

**Permissions résumé** :
- `AuteurViewSet` : **IsAuthenticated** (tout nécessite être connecté).
- `LivreViewSet` : **IsAuthenticatedOrReadOnly** + **IsOwnerOrReadOnly** (seul le propriétaire peut modifier/supprimer).

---

## 3) Tester chaque mode d’authentification

> ⚠️ N’activez **qu’un seul schéma** à la fois dans `api_project/settings.py` → `REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]`.

### A. BasicAuthentication (Exercice E)

**Activer** :
```python
REST_FRAMEWORK = {
  "DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework.authentication.BasicAuthentication",
  ],
  "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
  "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
  "PAGE_SIZE": 5,
}
```

**Endpoint de test** : `GET /basic-example/`  
- Postman : Authorization → **Basic Auth** → Username/Password = compte Django.  
- curl :
```bash
curl -u USERNAME:PASSWORD http://127.0.0.1:8000/basic-example/
```
Attendu : `200 OK` avec `{"user":"USERNAME","auth":"None"}`. Sans identifiants → `401`.

---

### B. SessionAuthentication + CSRF (Exercice D)

**Activer** :
```python
REST_FRAMEWORK = {
  "DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework.authentication.SessionAuthentication",
  ],
  "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
  "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
  "PAGE_SIZE": 5,
}
```

**Endpoint** : `GET/POST /session-example/`  
**Test (navigateur recommandé)** :  
1) Connectez-vous via `/api-auth/login/`.  
2) Ouvrez `/session-example/` → **GET** renvoie l’utilisateur.  
3) Depuis la page browsable DRF, envoyez un **POST** vide → CSRF géré automatiquement → `200 OK`.  
Sans cookie/CSRF, un POST externe est refusé (`403`).

---

### C. TokenAuthentication (Exercice C)

**Activer** :
```python
INSTALLED_APPS += ["rest_framework.authtoken"]
REST_FRAMEWORK = {
  "DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework.authentication.TokenAuthentication",
  ],
  "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
  "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
  "PAGE_SIZE": 5,
}
```
**Migrer** :
```bash
python manage.py migrate
```

**Obtenir un token** : `POST /api-token-auth/` (Body **x-www-form-urlencoded**)  
`username=...&password=...` → `{"token":"..."}`

**Tester** : `GET /token-example/` avec header  
`Authorization: Token VOTRE_TOKEN`  
(curl) :
```bash
curl -H "Authorization: Token VOTRE_TOKEN" http://127.0.0.1:8000/token-example/
```
Sans header → `401`.

---

### D. JWT via SimpleJWT (Exercice B)

**Installer** :
```bash
pip install djangorestframework-simplejwt
```

**Activer** :
```python
REST_FRAMEWORK = {
  "DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
  ],
  "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
  "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
  "PAGE_SIZE": 5,
}
```

**Endpoints** :
- Créer tokens : `POST /api/jwt/create/`
```json
{ "username": "votre_login", "password": "votre_mdp" }
```
→ `{"access":"...","refresh":"..."}`

- Rafraîchir : `POST /api/jwt/refresh/`
```json
{ "refresh": "VOTRE_REFRESH_TOKEN" }
```
→ `{"access":"...nouveau..."}`

**Vue protégée** : `GET /api/profile/` avec header  
`Authorization: Bearer VOTRE_ACCESS_TOKEN`

---

### E. Inscription qui renvoie directement les JWT (Exercice A)

**Endpoints** :
- Inscription + JWT : `POST /api/jwt/register/`
```json
{ "username": "alice", "email": "alice@example.com", "password": "Secret123!" }
```
→ `201 Created` avec `access` et `refresh` dans la réponse.

- Login (obtenir JWT) : `POST /api/jwt/login/`
```json
{ "username": "alice", "password": "Secret123!" }
```

**Utiliser l’access token** :  
`GET /api/profile/` avec `Authorization: Bearer <access>` → `200 OK`.

---

## 4) Rappels utiles

- **Créer un auteur** : POST `/auteurs/` (auth requise).  
- **Créer un livre** : POST `/livres/` (auth requise, le `owner` est fixé automatiquement à l’utilisateur connecté).  
- **Filtre année** : `/auteurs/?year=1980` → auteurs nés **après** 1980.  
- **Recherche** : `/livres/?search=python`.  
- **Pagination** : `/livres/?page=2`.  
- **Titres d’un auteur** : `/auteurs/{id}/titres/`.  
- **Erreurs classiques** :  
  - `401` → authentification manquante/invalide.  
  - `403` → CSRF manquant (SessionAuth) ou permission refusée (non-propriétaire pour modifier un livre).  
  - `400` → payload invalide (champs manquants / format incorrect).

Bon tests !
