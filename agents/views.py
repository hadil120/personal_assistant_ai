#agents/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Agent, Task, Interaction
from .serializers import AgentSerializer, TaskSerializer, InteractionSerializer
from .tasks import ask_openai
from celery.result import AsyncResult
from rest_framework.views import APIView
from .forms import AgentForm, TaskForm

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        agent_id = request.data.get('agent')
        task_id = request.data.get('task')

        if not prompt or not agent_id or not task_id:
            return Response({"detail": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agent = Agent.objects.get(id=agent_id)
            task = Task.objects.get(id=task_id)
        except Agent.DoesNotExist:
            return Response({"detail": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Appel asynchrone de la tâche Celery
        async_result = ask_openai.delay(prompt)

        # Création de l’interaction avec une réponse "en cours"
        interaction = Interaction.objects.create(
            prompt=prompt,
            response="Processing...",
            agent=agent,
            task=task,
        )

        serializer = self.get_serializer(interaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class AskOpenAIView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Le champ 'prompt' est requis."}, status=status.HTTP_400_BAD_REQUEST)

        task = ask_openai.delay(prompt)
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)

class GetResultView(APIView):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        if task_result.ready():
            if task_result.successful():
                return Response({"result": task_result.get()})
            else:
                return Response({"error": "La tâche a échoué."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"status": "En cours de traitement..."})


# Home page
def home(request):
    return render(request, 'home.html')


# Agent views
class AgentListView(ListView):
    model = Agent
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

class AgentCreateView(CreateView):
    model = Agent
    form_class = AgentForm
    template_name = 'agents/agent_form.html'
    success_url = reverse_lazy('agent-list')

class AgentUpdateView(UpdateView):
    model = Agent
    form_class = AgentForm
    template_name = 'agents/agent_form.html'
    success_url = reverse_lazy('agent-list')

class AgentDeleteView(DeleteView):
    model = Agent
    template_name = 'agents/agent_confirm_delete.html'
    success_url = reverse_lazy('agent-list')

# Task views
class TaskListView(ListView):
    model = Task
    template_name = 'agents/task_list.html'
    context_object_name = 'tasks'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'agents/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'agents/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'agents/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

# Interactions
class InteractionListView(ListView):
    model = Interaction
    template_name = 'agents/interaction_list.html'
    context_object_name = 'interactions'
