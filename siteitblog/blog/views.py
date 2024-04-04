from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

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


def lenta(request):
    posts = Post.objects.filter(is_published=True)

    data = {
        "id": 7,
        "friends": friends,
        "posts": posts,
        "profile": profile
    }
    return render(request, "blog/lenta.html", data)


def show_post(request, post_id: int):
    post = get_object_or_404(Post, pk=post_id)
    data = {
        "post": post,
        "profile": profile,
    }
    return render(request, "blog/post.html", data)


def my_post(request, profile_id: int):
    return HttpResponse(f"Отображение статей пользователя с id = {profile_id}")


def show_category(request, cat_slug: str):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Post.objects.filter(category=category)
    data = {
        "cat_slug": cat_slug,
        "posts": posts,
        "profile": profile
    }
    return render(request, "blog/lenta.html", data)


def login(request):
    return render(request, "blog/login.html")


def registration(request):
    return render(request, "blog/registration.html")


def profile_user(request, profile_id: int):
    # return HttpResponse(f"Страница профиля id = {profile_id}")
    data = {
        "profile": profile,
#        "post": posts
    }
    return render(request, "blog/profile.html", data)
