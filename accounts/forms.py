#accounts/forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields =('username','email','password1','password2')
        
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['icon', 'introduction']  # アイコンと自己紹介のみを更新

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # フィールドのカスタマイズ（例: プリセット値を設定するなど）
        self.fields['icon'].required = False
        self.fields['introduction'].required = False