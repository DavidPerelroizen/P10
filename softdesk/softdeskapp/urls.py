from django.urls import path, include
from .views import ProjectsViewset
from rest_framework import routers


router = routers.SimpleRouter()

router.register('projects', ProjectsViewset, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
    ]