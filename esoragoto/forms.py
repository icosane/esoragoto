from django.forms import ModelForm
from django import forms
#from esoragoto.models import textfield

class TextForm(forms.Form):
    form1 = forms.IntegerField(widget=forms.NumberInput)
    form2 = forms.IntegerField(widget=forms.NumberInput)
    #class Meta:
        #model = textfield
        #fields = '__all__'
