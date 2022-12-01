from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'tasks', views.TaskViewSet)
app_name = 'tasks'
urlpatterns = [
    path('', include(router.urls)),
]
