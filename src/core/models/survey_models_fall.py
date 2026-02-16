"""

Survey models for questions and answers 
These can be added, edited and deleted dynamically 

"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from fall_models import Fall

#Survey Questions for Cases
class CaseSurveyQuestions(models.Model):
    #Primary Key 
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #Fragenname 
    name = models.CharField(max_length=100, unique= True)
    #Name in form 
    label = models.CharField(max_length= 100)
    #is it a required question for their statistics 
    required = models.BooleanField(default= False)
    #für choices https://docs.djangoproject.com/en/6.0/ref/models/fields/ 
    field_type = models.CharField(max_length=25, choices= 
    [("string", "String"), ("boolean", "Boolean"), ("integer","Integer"), ("double","Double"),("date", "Date")]) 
    class Meta: 
        db_table = 'case_survey_question' 
        ordering = ['label']
        verboose_name = 'Frage für Fall'
        verboose_name_plural = 'Fragen für Fall'
    
    def __str__(self): 
        return self.label 
    
#Survey Answers for Cases 
class CaseSurveyAnswers(models.Model): 
    answer_id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable= False)
    value = models.CharField(max_length=100, unique= False) 
    case_id = models.ForeignKey(Fall, on_delete= models.CASCADE, related_name='survey answer') 
    survey_question = models.ForeignKey(CaseSurveyQuestions, on_delete= models.CASCADE, related_name='answers') 
    class Meta: 
        db_table = 'case_survey_answer'
        unique_together = [['case', 'question' ]]
        verboose_name = 'Antwort für Fall'
        verboose_name_plural = 'Antworten für Fall'
    def __str__(self): 
        return self.value