from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser

from config.pagination import CustomPagination
from task_manager.models import Tasks
from task_manager.v1.serializers import TaskSerializer
from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from task_manager.v1.serializers.task import TaskQueryFilterSerializer


# @api_view(['GET', 'POST'])
# def tasks_list(request):
#     if request.method == 'GET':
#         tasks = Tasks.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def task_detail(request, pk):
#     try:
#         tasks = Tasks.objects.get(pk=pk)
#     except Tasks.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = TaskSerializer(tasks)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = TaskSerializer(tasks, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         tasks.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#


# @csrf_exempt
# def tasks_list(request):
#     if request.method == 'GET':
#         tasks = Tasks.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = TaskSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
# @csrf_exempt
# def task_detail(request, pk):
#     try:
#         task = Tasks.objects.get(pk=pk)
#     except Tasks.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = TaskSerializer(task)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = TaskSerializer(task, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         task.delete()
#         return HttpResponse(status=204)

@extend_schema(tags=['Task'])
class TaskListAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):

    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    filterset_class = TaskQueryFilterSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = self.queryset.filter(name=name)
        return self.queryset

    @extend_schema(
        summary='Get all tasks',
        request=TaskQueryFilterSerializer,
        responses={200: TaskSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create task',
        request=TaskSerializer,
        responses={201: TaskSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@extend_schema(tags=['Task'])
class TaskDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

    @extend_schema(
        summary='Get a specific task',
        responses={200: TaskSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Update a task',
        request=TaskSerializer,
        responses={200: TaskSerializer}
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a task',
        request=TaskSerializer,
        responses={200: TaskSerializer}
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
