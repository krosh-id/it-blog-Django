import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View

from blog.forms import AddPostLentaForm, AddMyPostForm, AddCommentForm
from blog.models import Post, Category, Comment
from blog.services import add_like, remove_like

menu = [
    {'title': 'Профиль', 'icon': './icon/user.svg', 'url_name': 'profile'},
    {'title': 'Лента', 'icon': './icon/lenta.svg', 'url_name': 'lenta'},
    {'title': 'Мои посты', 'icon': './icon/my post.svg', 'url_name': 'my_post'},
]

friends = [
    {'id': 123, 'name': 'Супер котлета 228', 'img': 'котлета.png'},
    {'id': 124, 'name': 'Леди Баг', 'img': 'luntik.png'},
    {'id': 125, 'name': 'Злодей Британец', 'img': 'симпсон.png'},
]

profile = {
    "id": 1,
    "name": "Владислав Павлович",
    "img": "",
    "status": "в поисках error 404"
}


# сделать миксин который оформляет данные о пользователе (profile)
class BaseLikeReaction(LoginRequiredMixin, View):
    model = Model

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            body_request = request.body.decode("utf-8")
            model = self.model.objects.get(id=json.loads(body_request).get('modelId'))
            if model.get_is_liked(request.user):
                remove_like(model, self.request.user)
                return JsonResponse({'status': 'remove'})
            else:
                add_like(model, self.request.user)
                return JsonResponse({'status': 'add'})


class LentaView(LoginRequiredMixin, CreateView):
    form_class = AddPostLentaForm
    template_name = 'blog/lenta.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all().select_related('author')
        context['posts'] = posts
        for post in posts:
            post.get_is_liked(self.request.user)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_context_data()['post']
        return super().form_valid(form)


class ShowByCategoryView(LoginRequiredMixin, CreateView):
    form_class = AddPostLentaForm
    template_name = 'blog/lenta.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('cat_slug'))
        context['cat_slug'] = self.kwargs.get('cat_slug')
        context['posts'] = Post.objects.filter(category=category).all().select_related('author')
        context['profile'] = profile
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_context_data()['post']
        return super().form_valid(form)


class ShowPostView(LoginRequiredMixin, CreateView):
    form_class = AddCommentForm
    template_name = 'blog/post.html'

    # success_url = reverse_lazy('post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        context['post'] = post
        context['comments'] = context['post'].comment.all()
        context['profile'] = profile
        context['post_liked'] = post.get_is_liked(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_context_data()['post']
        return super().form_valid(form)


class ShowMyPostsView(LoginRequiredMixin, CreateView):
    form_class = AddMyPostForm
    template_name = 'blog/my_post.html'

    # success_url = reverse_lazy('post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = profile
        context['posts'] = Post.objects.filter(author=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, ListView):
    template_name = "blog/profile.html"
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = {
            "id": self.request.user.id,
            "name": self.request.user.first_name+' '+self.request.user.last_name,
            "img": "",
            "status": "в поисках error 404"
        }
        return context


class LikePostView(BaseLikeReaction):
    model_id = 'post_id'
    model = Post


class LikeCommentView(BaseLikeReaction):
    model_id = 'comment_id'
    model = Comment
