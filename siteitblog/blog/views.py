from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import AddPostLentaForm, AddMyPostForm
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
    if request.method == "POST":
        form = AddPostLentaForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user.id
            form.save()
            return redirect('my-post', request.user.id)
    else:
        form = AddPostLentaForm()

    data = {
        "id": 7,
        "friends": friends,
        "posts": posts,
        "profile": profile,
        "form": form
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
    if request.method == "POST":
        form = AddMyPostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user.id
            form.save()
            return redirect('my-post', request.user.id)
    else:
        form = AddMyPostForm()

    posts = Post.objects.filter(author=request.user.id)

    data = {
        "profile": profile,
        "form": form,
        "posts": posts
    }
    return render(request, "blog/my_post.html", data)


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
    }
    return render(request, "blog/profile.html", data)


def usefully_resource(request):
    # data = {
    #     "profile": profile,
    #
    # }
    return render(request, "blog/usefully_resource.html", {"profile": profile})
