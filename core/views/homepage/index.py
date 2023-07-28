from django.shortcuts import render


def homepage_index(request):
    # 从request.session中获取avatar_url的值，如果不存在则返回None
    avatar_url = request.session.get('avatar_url')

    context = {
        'avatar_url': avatar_url,
    }

    return render(request, "homepage/homepage.html", context)
