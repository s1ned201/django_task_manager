from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from task_manager.models import Tasks


def validate_max_count_split(value):
    if len(value.split()) > 4:
        raise ValidationError("%(value)s is too long. It must be less than 4 parts",
            params={"value": value},
        )


# class TaskForm(forms.Form):
#     name = forms.CharField(
#         label="Task name",
#         max_length=100,
#         validators=[
#         validate_max_count_split
#         ]
#     )
#     priority = forms.IntegerField(
#         label="Priority",
#         validators=[
#             MinValueValidator(1),
#             MaxValueValidator(5)
#         ]
#     )
#     description = forms.CharField(
#         label="Description",
#         widget=forms.TextInput(
#             attrs={
#                 "size": "40",
#                 "class": "special"
#             }
#         )
#     )

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["name","priority", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5, "cols": 50}),
        }