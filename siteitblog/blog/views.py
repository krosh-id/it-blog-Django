from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView
from django.views import View

from blog.forms import AddPostLentaForm, AddMyPostForm, AddFeedbackForm, AddCommentForm
from blog.models import Post, Category

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


class LentaView(LoginRequiredMixin, CreateView):
    form_class = AddPostLentaForm
    template_name = 'blog/lenta.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().select_related('author')
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
        context['post'] = Post.objects.get(id=self.kwargs.get('post_id'))
        context['comments'] = context['post'].comment.all()
        context['profile'] = profile
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
        context['profile'] = profile
        return context
