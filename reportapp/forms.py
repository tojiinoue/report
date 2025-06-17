from django import forms
from .models import Report, Comment
from django.contrib.auth.models import User


class ReportCreateForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('data', 'content', 'comment')

class ReportSearchForm(forms.Form):
    data = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))
    author = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    