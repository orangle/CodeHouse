# coding:utf-8
from django.conf.urls import url, include
from rest_framework import routers

from app import views


router = routers.SimpleRouter()
router.register(r'todos', views.TodoViewSet)


urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^', include(router.urls)),
]
