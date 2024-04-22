from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
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

# базовый класс для отображения какой-либо формы и списка чего либо


class PostsFormListView(LoginRequiredMixin, View):
    form_class = ModelForm
    redirect_to = None
    redirect_args = None
    extra_context = None
    template_name = None

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.extra_context['form'] = form
        return render(request, self.template_name, self.extra_context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.extra_context['form'] = form
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            if self.redirect_args:
                return redirect(to=self.redirect_to, args=self.redirect_args)
            else:
                return redirect(to=self.redirect_to)


class LentaView(PostsFormListView):
    posts = Post.objects.filter()
    template_name = 'blog/lenta.html'
    form_class = AddPostLentaForm
    redirect_to = 'lenta'
    extra_context = {
        "id": 7,
        "friends": friends,
        "posts": posts,
        "profile": profile,
    }


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


class ShowByCategoryView(LoginRequiredMixin, ListView):
    template_name = "blog/lenta.html"
    context_object_name = 'posts'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('cat_slug'))
        return Post.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = profile
        context['cat_slug'] = self.kwargs.get('cat_slug')
        return context


class ProfileView(LoginRequiredMixin, ListView):
    template_name = "blog/profile.html"
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = profile
        return context


def usefully_resource(request):
    full_data = {}
    if request.method == "POST":
        form = AddFeedbackForm(request.POST)
        if form.is_valid():
            full_data = form.cleaned_data
            if full_data["notice"]:
                full_data["notice"] = 'Да'
            else:
                full_data["notice"] = 'Нет'
    else:
        form = AddFeedbackForm()

    data = {
        "profile": profile,
        "form": form,
        "full_data": full_data
    }
    return render(request, "blog/usefully_resource.html", data)
