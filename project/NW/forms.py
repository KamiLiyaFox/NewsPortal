from django import forms
from .models import *
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = News
        fields = ['name', 'description', 'category']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return cleaned_data
