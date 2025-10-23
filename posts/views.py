from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class PostListView(ListView):
    # 1. Qual model vou usar?
    model = Post

    # 2. Qual template deve ser renderizado?
    template_name = 'posts/post_list.html'

    # 3. Quais objetos eu quero exibir?
    context_object_name = 'posts'

    # 4. Ativar paginação (Quantos itens por pagina?)
    paginate_by = 5

    # 5. Sobreescrevemos o mérodo para garantir que SÓ post publicados sejam exibidos
    def get_queryset(self):
        # Chama o queryset padrão (todos os Posts) e aplica o filtro
        return Post.objects.filter(status='published').order_by('-created_at')
    
class PostDetailView(DetailView):
    # 1. Qual modelo usar?
    model = Post
    
    # 2. Qual template deve ser renderizado?
    template_name = 'posts/post_detail.html'
    
    # 3. Qual nome o objeto será chamado no template?
    context_object_name = 'post'
    
    # 4. Sobrescrevemos o método para garantir que SÓ posts publicados sejam mostrados
    def get_queryset(self):
        # A DetailView precisa de um objeto. Filtramos pelo status 'published'
        # para que ninguém acesse rascunhos diretamente pela URL.
        return Post.objects.filter(status='published')