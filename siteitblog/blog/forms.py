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
                'minlength': 10
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


class AddFeedbackForm(forms.Form):
    name = forms.CharField(label='Вашe имя', min_length=2, max_length=100, widget=forms.TextInput(attrs={'id': 'my-input'}))
    city = forms.CharField(label='Ваш город', min_length=2, max_length=100)
    job = forms.CharField(label='Ваш род занятий', min_length=2, max_length=100)
    gender = forms.ChoiceField(label='Ваш пол',
                               choices=[('Мужской', 'Мужской'), ('Мужской', 'Женский')],
                               widget=forms.RadioSelect, initial=1)
    internet = forms.ChoiceField(label='Вы пользуетесь интернетом', choices=(
                                                    ('Каждый день', "Каждый день"),
                                                    ('Несколько раз в день', 'Несколько раз в день'),
                                                    ('Несколько раз в неделю', 'Несколько раз в неделю'),
                                                    ('Несколько раз в месяц', 'Несколько раз в месяц')
                                                ), initial=1)
    notice = forms.BooleanField(label='Получать новости сайта на e-mail?', required=False)
    email = forms.EmailField(label='Ваш e-mail', min_length=7)
    message = forms.CharField(label='Коротко о себе',
                              widget=forms.Textarea(attrs={'rows': 12, 'cols': 20}))
