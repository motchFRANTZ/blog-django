# posts/forms.py
from django import forms
from .models import Comment, Post

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

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'status')
        
        # Adiciona classes Tailwind aos widgets
        widgets = {
            # Campo Título (Input de texto)
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-primary focus:border-primary transition duration-150',
                'placeholder': 'Título do seu novo artigo'
            }),
            # Campo Conteúdo (Textarea)
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-primary focus:border-primary transition duration-150',
                'rows': 15,
                'placeholder': 'Escreva o conteúdo completo do seu artigo aqui...'
            }),
            # Campo Status (Select)
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-primary focus:border-primary transition duration-150',
            }),
        }