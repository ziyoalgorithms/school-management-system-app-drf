from rest_framework import generics, permissions, viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission

from staffs import serializers
from staffs.models import Teacher, Student


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CreateTeacherView(generics.CreateAPIView):
    serializer_class = serializers.TeacherSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManagerTeacherView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeacherSerializer
    permission_classes = [IsAdminUser]
    queryset = Teacher.objects.filter(is_active=True)


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StudentDetailSerializer
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.StudentDetailSerializer
        if self.action == 'upload_image':
            return serializers.ImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        student = self.get_object()
        serializer = self.get_serializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)