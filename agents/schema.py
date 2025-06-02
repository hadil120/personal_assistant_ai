import graphene
from graphene_django import DjangoObjectType
from agents.models import Agent, Task
from agents.tasks import ask_openai

class AgentType(DjangoObjectType):
    class Meta:
        model = Agent
        fields = "__all__"

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"

class Query(graphene.ObjectType):
    all_agents = graphene.List(AgentType)
    agent_by_id = graphene.Field(AgentType, id=graphene.ID(required=True))

    all_tasks = graphene.List(TaskType)
    task_by_id = graphene.Field(TaskType, id=graphene.ID(required=True))

    def resolve_all_agents(root, info):
        return Agent.objects.all()

    def resolve_agent_by_id(root, info, id):
        return Agent.objects.get(pk=id)

    def resolve_all_tasks(root, info):
        return Task.objects.all()

    def resolve_task_by_id(root, info, id):
        return Task.objects.get(pk=id)

# Mutation pour lancer une tâche ask_openai
class AskOpenAIMutation(graphene.Mutation):
    class Arguments:
        prompt = graphene.String(required=True)

    task = graphene.Field(TaskType)

    def mutate(self, info, prompt):
        # Lance la tâche asynchrone Celery
        async_result = ask_openai.delay(prompt)

        # Crée une instance Task dans la base (adapter selon ton modèle)
        task = Task.objects.create(
            celery_id=async_result.id,
            prompt=prompt,
            status='PENDING'
        )
        return AskOpenAIMutation(task=task)

class Mutation(graphene.ObjectType):
    ask_openai = AskOpenAIMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
