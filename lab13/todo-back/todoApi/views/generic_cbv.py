from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from todoApi.models import TaskList
from todoApi.serializers import TaskListSerializer2, TaskSerializer


class TaskLists(generics.ListCreateAPIView):
    serializer_class = TaskListSerializer2
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return TaskList.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer2


class TaskListOfTask(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        try:
            category = TaskList.objects.get(id=self.kwargs.get('pk'))
        except TaskList.DoesNotExist:
            raise Http404
        queryset = category.products.all()


        return queryset