from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render


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

posts = [
    {
        'id': 1,
        'category': '',
        'author': {'id': 123, 'name': 'Супер котлета 228', 'img': 'котлета.png'},
        'date': datetime(2005, 7, 14, 12, 30),
        'text': """Значимость этих проблем настолько очевидна, что рамки и место обучения кадров обеспечивает широкому кругу (специалистов)
            участие в формировании модели развития. Таким образом реализация намеченных плановых заданий
            играет важную роль в
            формировании форм развития. Товарищи!""",
        'img': '',
        'reaction': {'like': 5, 'lightning': 0, 'comments': 122}
    },
    {
        'id': 1,
        'category': '',
        'author': {'id': 123, 'name': 'Супер котлета 228', 'img': 'котлета.png'},
        'date': datetime(2005, 7, 14, 12, 30),
        'text': """Значимость этих проблем настолько очевидна, что рамки и место обучения кадров обеспечивает широкому кругу (специалистов)
        участие в формировании модели развития. Таким образом реализация намеченных плановых заданий
        играет важную роль в
        формировании форм развития. Товарищи!""",
        'img': '',
        'reaction': {'like': 5, 'lightning': 0, 'comments': 122}
    }
]

profile = {
    "id": 1,
    "name": "Владислав Павлович",
    "img": "",
    "status": "в поисках error 404"
}


def lenta(request):
    data = {
        "id": 7,
        "friends": friends,
        "posts": posts,
        "profile": profile
    }
    return render(request, "blog/lenta.html", data)


def show_post(request, post_id: int):
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def my_post(request, profile_id: int):
    return HttpResponse(f"Отображение статей пользователя с id = {profile_id}")


def login(request):
    return render(request, "blog/login.html")


def registration(request):
    return render(request, "blog/registration.html")


def profile_user(request, profile_id: int):
    # return HttpResponse(f"Страница профиля id = {profile_id}")
    data = {
        "profile": profile,
        "post": posts
    }
    return render(request, "blog/profile.html", data)
