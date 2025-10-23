# post/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Obtém o Model de Usuário que o Django está usando (boa prática de referência)
User = get_user_model()

# Create your models here.
class Post(models.Model):
    # Relacionamento: Um post é escrito por um usuário
    # on_delete = models.CASCADE: Se o autor for deletado, todos os posts dele também serão deletados
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    # Campo principal: título do post.
    title = models.CharField(max_length=200, verbose_name='Título')

    # O conteúdo do post
    content = models.TextField(verbose_name='Conteúdo')

    # URL amigável (slug). Usado em URLs: /blog/um-titulo-de-post
    # unique=True: garante que o slug seja exclusivo
    slug = models.SlugField(max_length=200, unique=True)

    # Data de criação (automaticamente preenchida na primeira vez)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    # Data da ultima modificação (atualizada em cada edição)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última atualização')

    # Status de Publicação: Podemos ter rascunhos ou publicados
    STATUS_CHOICES = (
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Método mágico que define como o post será apresentado
    def __str__(self):
        return self.title
    
    # Classe meta para definir ordenação e outros metadados
    class Meta:
        # Posts serão listados do mais novo para o mais antigo (0 '-' inverte a ordem)
        ordering = ['-created_at']  