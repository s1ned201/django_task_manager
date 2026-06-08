from drf_spectacular.utils import extend_schema
from task_manager.models import Tags
from task_manager.v1.serializers import TagSerializer
from rest_framework import mixins, generics


@extend_schema(tags=['Tag'])
class TagListAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):

    queryset = Tags.objects.all()
    serializer_class = TagSerializer

    @extend_schema(
        summary='Get all tags',
        responses={200: TagSerializer}
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create tag',
        request=TagSerializer,
        responses={201: TagSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)