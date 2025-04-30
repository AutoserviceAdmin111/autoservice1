from django import forms
from service.models import Appointment
from django.contrib.auth.models import User
from .models import UserProfile

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'problem']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ProfileForm(forms.ModelForm):
    patronymic = forms.CharField(
        label='Отчество',
        max_length=150,
        required=False
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'phone']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True