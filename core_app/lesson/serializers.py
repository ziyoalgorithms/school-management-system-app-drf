from rest_framework import serializers

from staffs.models import Student
from lesson.models import Subject, Group, GroupJournal, AttendanceAndGrades


class SubjectSerializer(serializers.ModelSerializer):
    teachers = serializers.StringRelatedField(
        source='subject_teacher',
        many=True,
        read_only=True
    )

    class Meta:
        model = Subject
        fields = ['id', 'name', 'price', 'teachers']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name', 'teacher', 'students']

    def get_new_students(self, students, group):
        for student in students:
            student_obj = Student.objects.get(id=student.id)
            group.students.add(student_obj)

    def create(self, validated_data):
        students = validated_data.pop('students', [])
        group = Group.objects.create(**validated_data)
        self.get_new_students(students, group)

        return group

    def update(self, instance, validated_data):
        students = validated_data.pop('students', None)
        if students is not None:
            instance.students.clear()
            self.get_new_students(students, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class GroupJournalSerializer(serializers.ModelSerializer):
    attendance_and_grades = serializers.StringRelatedField(
        source='att_and_grade',
        many=True,
        read_only=True,
    )

    class Meta:
        model = GroupJournal
        fields = ['id', 'date', 'group', 'theme', 'attendance_and_grades']


class AttendanceAdnGradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceAndGrades
        fields = ['id', 'date', 'group_journal', 'student', 'status', 'grade']

    def validate(self, data):
        validated_data = super().validate(data)
        students = validated_data['group_journal'].group.students.all()
        if validated_data['student'] not in students:
            raise serializers.ValidationError(
                'Kiritilgan talaba kiritilgan guruhda mavjud emas!'
            )

        return validated_data
