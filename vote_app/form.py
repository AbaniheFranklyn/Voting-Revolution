from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form
from .models import votingperiod,voter


  
class CustomUserCreationForm(UserCreationForm):  
    username = forms.CharField(label='username', min_length=5, max_length=150)
    email = forms.EmailField(label='email')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput) 

    

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_passwords(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  
class votingperiodform(forms.ModelForm):
    class Meta:
        model = votingperiod
        fields = ['start_date','end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type':'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()



class VoterForm(forms.ModelForm):
    class Meta:
        model = voter
        fields = '__all__'
        exclude = ['user']

    




# class AddParty(forms.ModelForm):
#     class Meta:
#         model = PoliticalParty
#         fields = ['party_name','party_logo','candidate_level']
#         widgets = {
#             'party_name' : forms.TextInput(attrs={'type':'party'}),
#             'party_logo' : forms.FileInput(attrs={'type':'party'}),
#             'candidate_level' : forms.SelectMultiple(attrs={'type':'party'})
#         }



