from django.urls import path, include
from .views import ProjectsViewset, IssuesViewset, CommentsViewset, ContributorsAPIView
from rest_framework import routers


router = routers.SimpleRouter()

router.register('', ProjectsViewset, basename='projects')
router.register('issues', IssuesViewset, basename='issues')
router.register('comments', CommentsViewset, basename='comments')

urlpatterns = [
    path('projects/', include(router.urls)),
    path('projects/<int:pk>/contributors/', ContributorsAPIView.as_view(), name='contributors'),
    ]
