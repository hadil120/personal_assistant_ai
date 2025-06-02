# personal_assistant_ai
Ce projet est une application Django complète qui combine :
- Gestion d’agents, tâches, interactions
- API REST avec Django REST Framework
- Authentification JWT (via SimpleJWT)
- Intégration GraphQL (via Graphene)
- Tâches asynchrones avec Celery + Redis
- Frontend simple avec des templates HTML

---

## 🚀 Prérequis

- Python 3.9+ recommandé
- pip ou pipenv/virtualenv
- Redis installé et lancé (par défaut sur `localhost:6379`)

---

## 📦 Installation
Créer un environnement virtuel et l’activer
pipenv shell
pip install Django>=5.1 djangorestframework djangorestframework-simplejwt graphene-django celery redis django-cors-headers django-csp django-environ
pip install -r requirements.txt(

Crée un fichier .env à la racine :(Django>=5.1
djangorestframework
djangorestframework-simplejwt
graphene-django
celery
redis
django-cors-headers
django-csp
environ)

env
Copier le code
DEBUG=True
SECRET_KEY=ton_cle_secrete
ALLOWED_HOSTS=127.0.0.1,localhost
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=5m
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=1d
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
Migrations:
python manage.py makemigrations
python manage.py migrate
Créer un superutilisateur: python manage.py createsuperuser
installer dossier redis (windows)
 Démarrer Redis:redis-server
Démarrer Celery:celery -A personal_assistant_ai worker --loglevel=info
Démarrer le serveur Django:python manage.py runserver
Routes à tester
Auth JWT:
POST /api/token/
avec { "username": "...", "password": "..." }

POST /api/token/refresh/
avec { "refresh": "..." }
GraphQL
Interface graphiql : http://127.0.0.1:8000/api/graphql/
 Endpoints REST à tester
Tous sont préfixés par /api/

 AGENTS
 Liste des agents
URL: http://127.0.0.1:8000/api/agents/

Méthode: POST

 Créer un agent
Méthode: POST

Body (JSON):
{
  "name": "AgentGPT",
}
TASKS
 Liste des tâches
URL: http://127.0.0.1:8000/api/tasks/

Méthode: POST
 Créer une tâche
json

{
  "title": "Analyser un CV",
  "description": "Utiliser GPT pour extraire les compétences",
  "agent": 1
}
INTERACTIONS
Liste des interactions
URL: http://127.0.0.1:8000/api/interactions/

Méthode: GET

Créer une interaction
json

{
  "agent": 1,
  "task": 1,
  "input_data": "Quel est le contenu de ce fichier ?"
}
DEMANDER UNE ACTION À L'AGENT
URL: http://127.0.0.1:8000/api/ask/

Méthode: POST

json

{
  "task_id": 1,
  "question": "Rédige une lettre de motivation pour un poste d'ingénieur"
}
RÉCUPÉRER LE RÉSULTAT D’UNE TÂCHE
URL: http://127.0.0.1:8000/api/result/<task_id>/

Méthode: GET

Remplace <task_id> par un ID existant.
Interface d’administration Django: http://127.0.0.1:8000/admin/
