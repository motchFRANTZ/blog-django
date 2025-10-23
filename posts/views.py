from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from .forms import CommentForm, PostForm

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


# ----------------------------------------------------
# VIEWS DE GERENCIAMENTO DE POSTS
# ----------------------------------------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_form.html' # Usaremos um template genérico
    form_class = PostForm # Usaremos um formulário genérico

    # Define o sucesso do redirecionamento para o post recém-nascido
    def get_success_url(self):
        # Usamos reverse para direcionar para o detalhe do post recém-criado (self.object)
        return reverse('post_detail', args=[self.object.slug])

    # Garante que o autor do post seja o usuário logado
    def form_valid(self, form):
        form.instance.author = self.request.user # Garante que o autor seja o usuário logado
        form.instance.slug = form.instance.title.lower().replace(' ', '-') # Cria um slug simples (melhoria futura: auto-slug)
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/post_form.html'
    form_class = PostForm

    # Sobreescrever o método para redirecionar para o post após a edição
    def get_success_url(self):
        return reverse('post_detail', args=[self.object.slug])

    # Teste de Permissão: Garante que apenas o autor possa editar o post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author # Retorna True se o usuário logado

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html' # Template para confirmação de exclusão
    success_url = reverse_lazy('post_list') # Redireciona para a lista de posts após a exclusão
    
    # Teste de Permissão: Garante que apenas o autor possa deletar
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author