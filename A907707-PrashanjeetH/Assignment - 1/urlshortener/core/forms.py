from django import forms
from core.models import UrlModel
class UrlForm(forms.ModelForm):
    class Meta:
        model = UrlModel

        exclude = ('url_id','created_on',)
