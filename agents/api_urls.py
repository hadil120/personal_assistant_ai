# agents/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, TaskViewSet, InteractionViewSet

router = DefaultRouter()
router.register(r'agents', AgentViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'interactions', InteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
