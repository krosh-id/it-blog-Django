from django import forms
from .models import Post, Category, Comment


class AddPostLentaForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='Выбрать категорию',
                                      widget=forms.Select(attrs={'class': 'main-section__select-category-btn'}))

    class Meta:
        model = Post
        fields = ['text', 'category']
        widgets = {
            'text': forms.Textarea(attrs={
                'wrap': 'soft',
                'rows': 5,
                'placeholder': 'Что интересеного у вас сегодня?',
                'maxlength': 280,
                'minlength': 10
            })
        }


class AddMyPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='Выбрать категорию',
                                      widget=forms.Select(attrs={'class': 'main-section__select-category-btn'}))

    class Meta:
        model = Post
        fields = ['text', 'category', 'image']
        widgets = {
            'text': forms.Textarea(attrs={
                'wrap': 'soft',
                'rows': 5,
                'placeholder': 'Что интересеного у вас сегодня?',
                'maxlength': 500,
                'minlength': 10,
                'id': 'textarea'
            }),
            'image': forms.FileInput(attrs={"hidden": "hidden", "id":"real-input"})
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Оставить комментарий...',
                'maxlength': 150,
                'minlength': 10
            })
        }