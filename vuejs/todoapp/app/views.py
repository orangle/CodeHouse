# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import list_route

from app.models import Todo
from app.serializers import TodoSerializer


def index(request):
    return render(request, 'index.html')


class TodoViewSet(viewsets.ModelViewSet):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    @list_route(methods=['delete'])
    def clear_todos(self, request):
        todos = Todo.objects.all()
        todos.delete()
        return HttpResponse(status=200)
