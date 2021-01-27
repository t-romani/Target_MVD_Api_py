from rest_framework import permissions, viewsets

from targets.models import Topic
from targets.serializers import TopicSerializer


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]
