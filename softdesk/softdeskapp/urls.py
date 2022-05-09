from django.urls import path, include
from .views import ProjectsViewset, IssuesViewset, CommentsViewset, ContributorsViewset
from rest_framework import routers


router = routers.SimpleRouter()

router.register('projects', ProjectsViewset, basename='projects')
router.register('issues', IssuesViewset, basename='issues')
router.register('comments', CommentsViewset, basename='comments')
router.register('projects/<int:pk>/users', ContributorsViewset, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    ]
