# hi_light/forms.py
from django import forms
from .models import PhotoPost

class PhotoPostForm(forms.ModelForm):
    class Meta:
        model = PhotoPost
        fields = ['category', 'title', 'comment', 'image1']  # アイコンと自己紹介は自動的に設定されるので削除

    def __init__(self, *args, **kwargs):
        edit_profile = kwargs.pop('edit_profile', False)  # 'edit_profile' を取り出す
        super().__init__(*args, **kwargs)

        if edit_profile:
            # プロフィール編集の場合、iconとintroductionだけを表示
            self.fields['category'].widget = forms.HiddenInput()
            self.fields['title'].widget = forms.HiddenInput()
            self.fields['comment'].widget = forms.HiddenInput()
            self.fields.pop('image1', None)