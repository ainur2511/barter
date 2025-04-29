# ads/forms.py
from django import forms
from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
        }


class AdFilterForm(forms.Form):
    query = forms.CharField(
        label="Поиск",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по заголовку и описанию'})
    )
    category = forms.CharField(
        label="Категория",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Категория'})
    )
    condition = forms.ChoiceField(
        label="Состояние",
        choices=[('', 'Все')] + [('new', 'Новый'), ('used', 'Б/У')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Введите комментарий'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем текущего пользователя
        super().__init__(*args, **kwargs)
        if user:
            # Фильтруем объявления отправителя
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)