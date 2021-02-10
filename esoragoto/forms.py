from django.forms import ModelForm
from django import forms
#from esoragoto.models import textfield

class TextForm(forms.Form):
    data1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Required', 'size': 3}),error_messages={'required': 'Required'})
    data2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Required', 'size': 3}), error_messages={'required': 'Required'})
    #class Meta:
        #model = textfield
        #fields = '__all__'
