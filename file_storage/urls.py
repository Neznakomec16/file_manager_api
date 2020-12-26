from django.urls import path, include
from rest_framework import routers

from file_storage.views import FilesViewSet, GetFileView

router = routers.DefaultRouter()
router.register(r'files', FilesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
