from rest_framework import serializers

from staffs.models import Student
from lesson.models import Subject, Group, GroupJournal, AttendanceAndGrades


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['id', 'name', 'price']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name', 'teacher', 'students']

    def get_students(self, students, group):
        for student in students:
            student_obj = Student.objects.get(id=student.id)
            group.students.add(student_obj)

    def create(self, validated_data):
        students = validated_data.pop('students', [])
        group = Group.objects.create(**validated_data)
        self.get_students(students, group)

        return group

    def update(self, instance, validated_data):
        students = validated_data.pop('students', None)
        if students is not None:
            instance.students.clear()
            self.get_students(students, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class GroupJournalSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupJournal
        fields = ['id', 'date', 'group', 'theme']


class AttendanceAdnGradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceAndGrades
        fields = ['id', 'date', 'group', 'student', 'status', 'grade']

    def validate(self, data):
        validated_data = super().validate(data)
        if validated_data['student'] not in validated_data['group'].students.all():
            raise serializers.ValidationError('Kiritilgan talaba kiritilgan guruhda mavjud emas!')

        return validated_data
