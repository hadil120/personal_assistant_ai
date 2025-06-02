import requests
from celery import shared_task
from django.conf import settings
from .models import Task, Interaction

import openai
from celery import shared_task
from agents.models import Interaction  # adapte selon ton modèle Interaction
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

@shared_task
def ask_openai(agent_id, prompt):
    # Appelle OpenAI ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # ou autre modèle que tu préfères
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )
    answer = response.choices[0].message.content

    # Stocker la réponse dans Interaction liée à l'agent
    interaction = Interaction.objects.create(
        agent_id=agent_id,
        prompt=prompt,
        response=answer,
    )
    return interaction.id


@shared_task(bind=True)
def autogpt_recursive(self, task_id: int, prompt: str, depth: int = 3):
    """
    Recursive Celery task chaining prompts to AutoGPT-like behavior:
    - Calls AI with prompt
    - Saves prompt/response as Interaction
    - Calls itself with new prompt until depth=0
    """
    if depth <= 0:
        return "AutoGPT chain complete."

    # Call AI API
    try:
        response_text = ask_openai(prompt)
    except Exception as e:
        # Optional: Retry logic or logging here
        raise self.retry(exc=e, countdown=10, max_retries=3)

    # Save interaction to DB
    task = Task.objects.get(id=task_id)
    Interaction.objects.create(task=task, prompt=prompt, response=response_text)

    # Prepare next prompt for chaining
    next_prompt = f"Continue and elaborate based on: {response_text}"

    # Recursive call for next step
    return autogpt_recursive.apply_async(
        args=[task_id, next_prompt, depth - 1]
    )
