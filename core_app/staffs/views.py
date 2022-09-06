from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from staffs import serializers
from staffs.models import Teacher, Student


class CreateTeacherView(generics.CreateAPIView):
    serializer_class = serializers.TeacherSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManagerTeacherView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_object(self):
        return self.request.user


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Teacher.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.StudentDetailSerializer

        return self.serializer_class