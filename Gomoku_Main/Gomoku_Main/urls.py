"""
URL configuration for Gomoku_Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.shortcuts import redirect


class VueGomoku(TemplateView):
    template_name = 'index.html'


urlpatterns = [
    path('main', VueGomoku.as_view()),
    path("api/gomoku/", include("gomoku.urls")),

    # 匹配所有其他路由，并添加静态前缀
    re_path(r'^(?P<path>.*)$', lambda request, path: redirect(f'/static/{path}')),
]

