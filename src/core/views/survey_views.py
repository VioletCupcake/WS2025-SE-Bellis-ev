"""
Views for Survey management.

Handles survey question listing/creation/deletion and saving answers per case.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import CaseSurveyQuestion, CaseSurveyAnswer, Fall
from core.decorators import permission_required_custom


@login_required
@permission_required_custom('can_edit_cases')
def survey_questions(request):
    """
    List all survey questions and handle creation of new ones.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        label = request.POST.get('label', '').strip()
        field_type = request.POST.get('field_type', 'string')
        required = request.POST.get('required') == 'on'

        if name and label:
            try:
                CaseSurveyQuestion.objects.create(
                    name=name,
                    label=label,
                    field_type=field_type,
                    required=required
                )
                messages.success(request, f'Frage "{label}" erfolgreich erstellt.')
            except Exception as e:
                messages.error(request, f'Fehler beim Erstellen: {str(e)}')
        else:
            messages.error(request, 'Name und Label sind Pflichtfelder.')

        return redirect('core:survey_questions')

    questions = CaseSurveyQuestion.objects.all()
    context = {
        'questions': questions,
        'field_type_choices': CaseSurveyQuestion.FIELD_TYPE_CHOICES,
    }
    return render(request, 'core/survey_questions.html', context)


@login_required
@permission_required_custom('can_delete_cases')
def survey_question_delete(request, question_id):
    """
    Delete a survey question after confirmation.
    """
    question = get_object_or_404(CaseSurveyQuestion, question_id=question_id)

    if request.method == 'POST':
        label = question.label
        question.delete()
        messages.success(request, f'Frage "{label}" gelöscht.')
        return redirect('core:survey_questions')

    context = {'question': question}
    return render(request, 'core/survey_question_delete.html', context)


@login_required
@permission_required_custom('can_edit_cases')
def survey_answers_save(request, fall_id):
    """
    Save all survey answers for a case.
    Receives form data where each field is named 'question_<uuid>'.
    """
    fall = get_object_or_404(Fall, fall_id=fall_id)

    if request.method == 'POST':
        questions = CaseSurveyQuestion.objects.all()

        for question in questions:
            field_name = f'question_{question.question_id}'
            value = request.POST.get(field_name, '').strip()

            if value:
                CaseSurveyAnswer.objects.update_or_create(
                    case=fall,
                    question=question,
                    defaults={'value': value}
                )
            else:
                # Remove answer if field is empty
                CaseSurveyAnswer.objects.filter(
                    case=fall,
                    question=question
                ).delete()

        messages.success(request, 'Zusätzliche Angaben gespeichert.')

    return redirect('core:case_detail', fall_id=fall_id)
