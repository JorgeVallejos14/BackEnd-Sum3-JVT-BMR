
from django import forms
from django.utils import timezone

from .models import Encargo


class EncargoForm(forms.ModelForm):

    class Meta:
        model = Encargo

        fields = [
            "nombre_comprador",
            "correo",
            "fecha_retiro",
            "cantidad",
        ]

        labels = {
            "nombre_comprador": "Nombre completo",
            "correo": "Correo electrónico",
            "fecha_retiro": "Fecha de retiro",
            "cantidad": "Cantidad de unidades",
        }

        widgets = {
            "nombre_comprador": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "correo": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "fecha_retiro": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),
            "cantidad": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 3,
                }
            ),
        }

    def clean_fecha_retiro(self):
        fecha = self.cleaned_data["fecha_retiro"]

        if fecha < timezone.localdate():
            raise forms.ValidationError(
                "La fecha de retiro no puede ser anterior a hoy."
            )

        return fecha

    def clean_cantidad(self):
        cantidad = self.cleaned_data["cantidad"]

        if cantidad < 1 or cantidad > 3:
            raise forms.ValidationError(
                "La cantidad debe estar entre 1 y 3 unidades."
            )

        return cantidad
