from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de post
    list_display = ('title', 'author', 'status', 'created_at')

    # Adiciona uma barra lateral para filtrar posts por Status e Author
    list_filter = ('status', 'created_at', 'author')
    
    # Adiciona um campo de busca por título e conteúdo
    search_fields = ('title', 'content')
    
    # Preenche o campo 'slug' automaticamente com base no 'title'
    prepopulated_fields = {'slug': ('title',)}
    
    # Define a ordem dos campos no formulário de edição/criação
    fields = ('title', 'slug', 'author', 'content', 'status')
    
    # Faz com que a data de criação seja somente leitura
    readonly_fields = ('created_at', 'updated_at')

'''
Explicações:

@admin.register(Post): É um decorador que registra o modelo Post no Admin, usando as configurações da classe PostAdmin abaixo.

list_display: Controla as colunas que aparecem na página de listagem de posts. É crucial para uma boa visão geral dos dados.

list_filter: Cria filtros laterais, permitindo, por exemplo, visualizar rapidamente apenas os posts com status='draft' (rascunho).

search_fields: Adiciona uma barra de busca que procura termos nos campos especificados (title e content).

prepopulated_fields = {'slug': ('title',)}: Muito importante! Ao digitar o título de um post, o Django preenche o campo slug automaticamente, transformando "Meu Primeiro Post" em "meu-primeiro-post". Isso economiza tempo e evita erros.
'''

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Exibir o post, o autor e o status de aprovação
    list_display = ('post', 'author', 'created_at', 'approved')
    # Permitir filtrar por status de aprovação e data
    list_filter = ('approved', 'created_at')
    # Permitir aprovar/desaprovar comentários diretamente na lista
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Comentários selecionados foram aprovados com sucesso.")
    approve_comments.short_description = "Aprovar comentários selecionados"

    def disapprove_comments(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, "Comentários selecionados foram reprovados com sucesso.")
    disapprove_comments.short_description = "Reprovar comentários selecionados"