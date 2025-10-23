# posts/urls.py
from django.urls import path
from .views import PostListView, PostDetailView

urlpatterns = [
    # Mapeia a URL /blog/ (já que a global tem 'blog/') para a PostListView
    path('', PostListView.as_view(), name='post_list'),
    # URL de Detalhe: Espera-se um 'slug' (o nome amigável) na URL
    # <slug:slug> diz ao Django para capturar o valor após 'blog/' e passá-lo para a View
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]