
from django import forms

class CalculatorForm(forms.Form):
   inputQuery = forms.CharField(label='Enter Query', max_length=1000)