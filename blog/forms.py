from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextField


# Apply summernote to specific fields.
# class SomeForm(forms.Form):
#     foo = forms.CharField(widget=SummernoteWidget())  # instead of forms.Textarea

# If you don't like <iframe>, then use inplace widget
# Or if you're using django-crispy-forms, please use this.
# class PostForm(forms.Form):
#     content = forms.CharField(widget=SummernoteInplaceWidget())

class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ( 'title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', )
        widgets = {
            'content': SummernoteWidget(),
            # 'tags' : forms.CharField()
        }
