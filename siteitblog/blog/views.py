import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View, TemplateView

from blog.forms import AddPostLentaForm, AddMyPostForm, AddCommentForm
from blog.models import Post, Category, Comment
from blog.services import add_like, remove_like
from siteitblog import settings

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

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all().select_related('author')
        context['posts'] = posts
        for post in posts:
            post.get_is_liked(self.request.user)
        context['profile'] = self.request.user
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
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
        context['profile'] = self.request.user
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
        context['profile'] = self.request.user
        context['post_liked'] = post.get_is_liked(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_context_data()['post']
        return super().form_valid(form)


class AboutCompanyView(TemplateView):
    template_name = "blog/about_company.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_user_model().objects.get(username="company")
        posts = Post.objects.filter(author=company).all()
        context['profile'] = {
            "id": company.id,
            "name": company.first_name + ' ' + company.last_name,
            "photo": company.photo if company.photo else settings.DEFAULT_USER_IMAGE,
            "status": company.status if company.status else '',
        }
        context["about_company"] = posts.last()
        context["posts"] = posts
        return context


class ProfileView(LoginRequiredMixin, CreateView):
    form_class = AddMyPostForm
    template_name = "blog/profile.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user).all()
        user = self.request.user
        context['profile'] = {
            "id": user.id,
            "name": user.first_name+' '+user.last_name,
            "photo": user.photo if user.photo else settings.DEFAULT_USER_IMAGE,
            "status": user.status if user.status else '',
        }
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LikePostView(BaseLikeReaction):
    model_id = 'post_id'
    model = Post


class LikeCommentView(BaseLikeReaction):
    model_id = 'comment_id'
    model = Comment
