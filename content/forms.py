from django import forms
from taggit.forms import TagField
from .models import Content, UploadFile


class CreatePostForm(forms.ModelForm):
    """Форма создания поста"""
    class Meta:
        model = Content
        fields = ['title', 'description', 'preview', 'status']

    tags = TagField(label='Tags')


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadFileForm(forms.ModelForm):
    """Форма загрузки нескольких изображений"""
    file = MultipleFileField()

    class Meta:
        model = UploadFile
        fields = ['file']


class SearchForm(forms.Form):
    query = forms.CharField()


