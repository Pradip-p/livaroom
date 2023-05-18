from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
  
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg', 'placeholder': 'Password', 'required': True}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-lg', 'placeholder': 'Verify Password', 'required': True}))

    class Meta:
        model = CustomUser
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control input-lg', 'placeholder': 'Email', 'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user