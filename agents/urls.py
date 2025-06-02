from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, TaskViewSet, InteractionViewSet
from agents.views import AskOpenAIView, GetResultView
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from agents.schema import schema
from . import views
from django.http import HttpResponse


urlpatterns = [
    
    path('ask/', AskOpenAIView.as_view(), name='ask_openai'),
    path('result/<str:task_id>/', GetResultView.as_view(), name='get_result'),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('home/', views.home, name='home'),


    # Agent URLs
    path('agents/', views.AgentListView.as_view(), name='agent-list'),
    path('agents/create/', views.AgentCreateView.as_view(), name='agent-create'),
    path('agents/<int:pk>/update/', views.AgentUpdateView.as_view(), name='agent-update'),
    path('agents/<int:pk>/delete/', views.AgentDeleteView.as_view(), name='agent-delete'),

    # Task URLs
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),

    # Interactions
    path('interactions/', views.InteractionListView.as_view(), name='interaction-list'),
]

