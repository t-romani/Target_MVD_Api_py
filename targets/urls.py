from django.urls import include, path
from rest_framework import routers

from targets.views import TopicViewSet

router = routers.DefaultRouter()
router.register('topics', TopicViewSet, basename='topics')

urlpatterns = [path('', include(router.urls))]
