from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lesson import views

app_name = 'lesson'

router = DefaultRouter()
router.register('subject', views.SubjectViewSet)
router.register('group', views.GroupViewSet)
router.register('groupjournal', views.GroupJournalViewSet)
router.register('attendance-and-grades', views.AttendanceAndGradesViewSet)

urlpatterns = [
    path('', include(router.urls))
]
