from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter strong password (min 6 characters)',
        'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'e.g. aryavarta_explorer',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@heritage.in',
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', 'Passwords do not match.')
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm'
    }))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm'
    }))

    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'location', 'favorite_state']
        widgets = {
            'avatar': forms.URLInput(attrs={
                'placeholder': 'https://...',
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Share your passion for Indian heritage...',
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'City, State or Country',
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm'
            }),
            'favorite_state': forms.TextInput(attrs={
                'placeholder': 'e.g. Rajasthan, Kerala, Odisha',
                'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-sm'
            }),
        }
