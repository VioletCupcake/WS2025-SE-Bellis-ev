"""
Case Survey Manager - handles operations with case surveys.
Provides atomic transactions and business logic for survey questions/answers.
"""

from typing import Any
from uuid import UUID

from django.db import transaction

from core.models import Fall, User, CaseSurveyQuestion, CaseSurveyAnswer


class SurveyManager:
    """Service class for survey operations requiring atomic transactions."""

    @staticmethod
    def create_question(data: dict, user: User) -> CaseSurveyQuestion:
        """Create and save a new survey question."""
        question = CaseSurveyQuestion(**data)
        question.save()
        return question

    @staticmethod
    def delete_question(question_id: UUID, user: User) -> None:
        """Delete a survey question by its ID."""
        question = CaseSurveyQuestion.objects.get(pk=question_id)
        question.delete()

    @staticmethod
    @transaction.atomic
    def set_answer(case_id: UUID, question_id: UUID, value: Any) -> CaseSurveyAnswer:
        """Create or update an answer atomically."""
        fall = Fall.objects.get(pk=case_id)
        question = CaseSurveyQuestion.objects.get(pk=question_id)

        answer, _ = CaseSurveyAnswer.objects.update_or_create(
            case=fall,
            question=question,
            defaults={"value": str(value)}
        )

        return answer
