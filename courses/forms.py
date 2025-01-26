from django import forms
from .models import Quiz, Question, Answer

class QuizSubmissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.quiz = kwargs.pop('quiz')
        super().__init__(*args, **kwargs)

        # Dynamically generate fields for each question
        for question in self.quiz.questions.all():
            field_name = f"question_{question.id}"
            if question.type == Question.MULTIPLE_CHOICE:
                self.fields[field_name] = forms.ChoiceField(
                    choices=[(answer.id, answer.content) for answer in question.answers.all()],
                    widget=forms.RadioSelect,
                    label=question.content,
                )
            elif question.type == Question.TRUE_FALSE:
                self.fields[field_name] = forms.ChoiceField(
                    choices=[
                        (answer.id, "True") for answer in question.answers.filter(is_correct=True)
                    ] + [
                        (answer.id, "False") for answer in question.answers.filter(is_correct=False)
                    ],
                    widget=forms.RadioSelect,
                    label=question.content,
                )
            elif question.type == Question.SHORT_ANSWER:
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea,
                    label=question.content,
                    required=False
                )