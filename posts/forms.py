# posts/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    # O conteúdo do comentário será a única coisa visível/editável pelo usuário
    class Meta:
        model = Comment
        fields = ('content',)
        # Adicionando um placeholder
        widgets = {
           'content': forms.Textarea(attrs={'placeholder': 'Digite seu comentário aqui...', 'rows': 4, 
                                 'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-primary focus:border-primary transition duration-150'}),
        }
        labels = {
            'content': 'Seu Comentário:',
        }