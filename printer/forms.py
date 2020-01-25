from django import forms
from .models import PrintRequest

class PrintRequestForm(forms.ModelForm):

    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:

        model = PrintRequest
        fields = ['description', 'is_both_sides', 'is_color']
