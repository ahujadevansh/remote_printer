from django import forms
from django.forms import modelformset_factory
from django.forms import BaseModelFormSet

from tinymce.widgets import TinyMCE

from .models import PrintRequest, PrintRequestFile

class PrintRequestForm(forms.ModelForm):

    error_css_class = 'error'
    required_css_class = 'required'

    description = forms.CharField(widget=TinyMCE(attrs={'cols': 10, 'rows': 10, 'required': False},), required=False)

    class Meta:

        model = PrintRequest
        fields = ['description', 'is_both_side', 'is_color', 'no_of_front_page', 'no_of_blank_page']
        help_texts = {
            'description': 'Shortcut ctrl + k to insert link',
        }

class PrintRequestFileForm(forms.ModelForm):

    document = forms.FileField(allow_empty_file=True, required=False)
    no_of_copies = forms.IntegerField(required=False)
    class Meta:

        model = PrintRequestFile
        fields = ['document', 'no_of_copies']

class BasePrintRequestFileFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = PrintRequestFile.objects.none()
PrintRequestFileFormSet = modelformset_factory(PrintRequestFile, form=PrintRequestFileForm, extra=1, max_num=10,
                                               formset=BasePrintRequestFileFormSet)
