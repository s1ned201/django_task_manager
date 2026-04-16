from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from account.models import User
from task_manager.models import Tasks, Comments, Attachments


def validate_max_count_split(value):
    if len(value.split()) > 4:
        raise ValidationError("%(value)s is too long. It must be less than 4 parts",
            params={"value": value},
        )


class UserCreateForm(forms.ModelForm):

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        help_text='Минимум 8 символов'
    )

    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'user@example.com'
        })
    )

    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        }),
        help_text='Обязательное поле. Только буквы, цифры и @/./+/-/_.'
    )

    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя'
        })
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите фамилию'
        })
    )

    is_active = forms.BooleanField(
        label='Активен',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    is_staff = forms.BooleanField(
        label='Персонал (доступ в админку)',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    is_superuser = forms.BooleanField(
        label='Суперпользователь (все права)',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'is_superuser']

    def unique_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username

    def unique_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def conf_pass(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают.')

        if password and len(password) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = [
            "name",
            "description",
            "priority",
            "status"
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задачи'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'cols': 50,
                'placeholder': 'Подробное описание задачи...'
            }),
            'priority': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'step': 1
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        def clean(self):
            cleaned_data = super().clean()
            priority = cleaned_data.get('priority')
            description = cleaned_data.get('description')
            name = cleaned_data.get('name')
            if priority and priority >= 8:
                if not description or description.strip() == '':
                    raise ValidationError({
                        'description': 'Для задач с высоким приоритетом (8-10) обязательно указание описания.'
                    })
            if name:
                forbidden_chars = '@#$%^&*'
                if any(char in name for char in forbidden_chars):
                    raise ValidationError({
                        'name': f'Название задачи не должно содержать спецсимволы: {forbidden_chars}'
                    })

            return cleaned_data

class CommentForm(forms.ModelForm):
    message = forms.CharField(
        label='Текст комментария',
        max_length=500,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Введите ваш комментарий...',
            'class': 'form-control'
        }),
    )

    user = forms.ModelChoiceField(
        label='Пользователь',
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = Comments
        fields = ['message', 'user']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachments
        fields = ['name', 'photo', 'task']