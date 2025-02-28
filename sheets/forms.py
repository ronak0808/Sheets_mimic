from django import forms
from .models import Cell

class CellForm(forms.ModelForm):
    class Meta:
        model = Cell
        fields = ['row', 'col', 'value', 'formula']
