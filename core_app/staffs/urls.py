from django.urls import path, include
from rest_framework.routers import DefaultRouter

from staffs import views

app_name = 'staffs'

router = DefaultRouter()
router.register('teachers', views.TeacherViewSet)
router.register('students', views.StudentViewSet)

urlpatterns = [
    path('create_teacher/', views.CreateTeacherView.as_view(), name='create_teacher'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManagerTeacherView.as_view(), name='me'),
    path('', include(router.urls)),
]
