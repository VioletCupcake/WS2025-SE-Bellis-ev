"""
case survey Manager - handles actions with case_survey
Most operations handled by Django ORM in views.

"""

from typing import Any
from uuid import UUID
from datetime import date

from django.db import transaction
from django.core.exceptions import ValidationError, PermissionDenied

from core.models import Fall, User, CaseSurveyQuestion, CaseSurveyAnswer

class SurveyManager:
    
    "Service class for operations requiring atomic transactions or permission checks."

    @staticmethod
    def createCaseSurveyQuestion (data: dict, user: User) -> CaseSurveyQuestion:
        #create new Survey Question 
        
        question = CaseSurveyQuestion(**data)
        
        return question
    
    @staticmethod
    def deleteSurveyQuestion(question_id: UUID, user: User) -> None:

        question = CaseSurveyQuestion.objects.get(pk=question_id)
        question.delete()

    @staticmethod
    @transaction.atomic
    def setSurveyAnswer(case_id: UUID,question_id: UUID,value: Any) -> CaseSurveyAnswer:
        """
        Creates or updates an answer atomically.
        """

        Fall = Fall.objects.get(pk= fall_id)
        question = CaseSurveyQuestion.objects.get(pk=question_id)


        answer, _ = CaseSurveyAnswer.objects.update_or_create(
            Fall = Fall,
            question=question,
            defaults={"value": str(value)}
        )

        return answer
     


