from tokenize import group
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from lesson.models import Subject, Group, GroupJournal, AttendanceAndGrades
from lesson import serializers


class SubjectViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.SubjectSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Subject.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Group.objects.all()

    @action(detail=True, methods=['POST'])
    def add_student(self, request, *args, **kwargs):
        group = self.get_object()
        student = self.request.data
        group.students.add(student)
        serializer = serializers.GroupSerializer(group)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def remove_student(self, request, *args, **kwargs):
        group = self.get_object()
        student = self.request.data
        group.students.remove(student)
        serializer = serializers.GroupSerializer(group)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GroupJournalViewSet(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = serializers.GroupJournalSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = GroupJournal.objects.all()

    def get_queryset(self):
        return self.queryset.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class AttendanceAndGradesViewSet(mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    serializer_class = serializers.AttendanceAdnGradesSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AttendanceAndGrades.objects.all()

    def get_queryset(self):
        return self.queryset.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)