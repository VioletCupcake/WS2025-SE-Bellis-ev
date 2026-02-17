"""
Survey models for dynamic questions and answers.
These can be added, edited and deleted dynamically at runtime
without requiring code changes or migrations.
"""
import uuid
from django.db import models
from .fall_models import Fall


class CaseSurveyQuestion(models.Model):
    """A dynamic survey question that can be associated with any Fall (case)."""

    FIELD_TYPE_CHOICES = [
        ("string", "String"),
        ("boolean", "Boolean"),
        ("integer", "Integer"),
        ("double", "Double"),
        ("date", "Date"),
    ]

    question_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    required = models.BooleanField(default=False)
    field_type = models.CharField(max_length=25, choices=FIELD_TYPE_CHOICES)

    class Meta:
        db_table = 'case_survey_question'
        ordering = ['label']
        verbose_name = 'Frage für Fall'
        verbose_name_plural = 'Fragen für Fall'

    def __str__(self):
        return self.label


class CaseSurveyAnswer(models.Model):
    """An answer to a survey question, linked to a specific Fall (case)."""

    answer_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    value = models.CharField(max_length=100)
    case = models.ForeignKey(
        Fall, on_delete=models.CASCADE, related_name='survey_answers'
    )
    question = models.ForeignKey(
        CaseSurveyQuestion, on_delete=models.CASCADE, related_name='answers'
    )

    class Meta:
        db_table = 'case_survey_answer'
        unique_together = [['case', 'question']]
        verbose_name = 'Antwort für Fall'
        verbose_name_plural = 'Antworten für Fall'

    def __str__(self):
        return self.value
