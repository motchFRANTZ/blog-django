from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin # <-- NOVO
from .models import Post, Comment
from .forms import CommentForm

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

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    
    # 1. Filtra para exibir apenas posts publicados (como antes)
    def get_queryset(self):
        return Post.objects.filter(status='published')

    # 2. Adiciona o formulário de comentário e a lista de comentários ao contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtra apenas os comentários aprovados para exibição
        context['comments'] = self.object.comments.filter(approved=True)
        # Cria uma instância vazia do formulário de comentário
        context['comment_form'] = CommentForm() 
        return context

    # 3. Processa o formulário de comentário via POST
    def post(self, request, *args, **kwargs):
        # Garante que o usuário esteja logado antes de processar o POST
        if not request.user.is_authenticated:
            return redirect('login') 
            
        self.object = self.get_object() # Obtém o post atual
        form = CommentForm(request.POST) # Popula o formulário com os dados

        if form.is_valid():
            # Não salva no banco de dados ainda (commit=False)
            new_comment = form.save(commit=False)
            # Liga o comentário ao post e ao autor logado
            new_comment.post = self.object
            new_comment.author = request.user
            # O campo 'approved' é False por padrão (moderação)
            new_comment.save()
            
            # Redireciona para o mesmo post (evita reenvio do formulário)
            return redirect(self.object.get_absolute_url()) 
            
        # Se o formulário for inválido, renderiza o template novamente com os erros
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form # Passa o formulário com os erros de volta
        return self.render_to_response(context)

# ATENÇÃO: Adicione este método à CLASSE POST (posts/models.py)
# para que o redirect no POST da DetailView funcione corretamente
# class Post(models.Model):
#    ...
#    def get_absolute_url(self):
#        from django.urls import reverse
#        return reverse('post_detail', args=[str(self.slug)])