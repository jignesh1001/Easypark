from django import forms
from django.db.models import fields
from django.forms import ModelForm
from parkapp.models import TYPER
from parkapp.models import OWNER,CUSTOMER,BOOK

class DateInput(forms.DateInput):
    input_type = 'date'

class TYPEForm(ModelForm):
    class Meta:
        model = TYPER
        fields = ['usertype']

class OWNERForm(ModelForm):
    class Meta:
        model = OWNER
        fields = ['name','phone_number','city','address']

class CUSTOMERForm(ModelForm):
    class Meta:
        model = CUSTOMER
        fields = ['phone','email','address']

class BOOKForm(ModelForm):
    class Meta:
        model = BOOK
        fields = ['date','time']
