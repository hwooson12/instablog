from django import forms
from django.forms import ValidationError

from .models import Post

class PostForm(forms.Form):
    title = forms.CharField(required=True, label='글제목')
    content = forms.CharField(widget=forms.Textarea, required=True, label='내용')


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'categories', 'content', 'tags')
        # exclude = ('title','categories',) // not using fields
        # fields ='__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title','')
        if '바보' in title:
            raise ValidationError('바보같은놈')
        return title.strip()

    def clean(self):
        super(PostEditForm, self).clean()
        title = self.cleaned_data.get('title','')
        content = self.cleaned_data.get('content', '')

        if '안녕' in title:
            self.add_error('title', '안녕은 이제 그만')
        if'안녕' in content:
            self.add_error('content', '안녕은 이제 그만')
