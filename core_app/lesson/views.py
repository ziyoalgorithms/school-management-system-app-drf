from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from lesson.models import Subject, Group, GroupJournal, AttendanceAndGrades
from management.permissions.isAdminUser import IsAdminUser
from lesson import serializers


class SubjectViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.SubjectSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'price']
    filterset_fields = ['name', 'price']
    ordering_fields = ['price', ]
    queryset = Subject.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'teacher__first_name', 'students__first_name']
    ordering_fields = ['name']
    filterset_fields = ['name', 'teacher__first_name', 'students__first_name']
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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['date', 'group__name', 'teacher__first_name']
    ordering_fields = ['date']
    filterset_fields = ['date', 'group__name', 'teacher__first_name']
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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['date', 'group__name', 'student__first_name', 'student__last_name', 'status', 'grade', 'teacher__first_name']
    ordering_fields = ['date', 'student__first_name', 'student__last_name', ]
    filterset_fields = ['date', 'student__first_name', 'student__last_name', 'status', 'grade', 'teacher__first_name']
    queryset = AttendanceAndGrades.objects.all()

    def get_queryset(self):
        return self.queryset.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        teacher = self.request.user
        group_journal = GroupJournal.objects.filter(teacher=teacher).last()
        serializer.save(teacher=teacher, group_journal=group_journal)