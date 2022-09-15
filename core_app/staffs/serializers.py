from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers

from staffs.models import Student


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'subject',
            'password',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=True,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Berilgan ma'lumotlar bilan autentifikatsiyadab o'tib bo'lmaydi!")
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'image'
        ]


class StudentDetailSerializer(StudentSerializer):

    class Meta(StudentSerializer.Meta):
        fields = StudentSerializer.Meta.fields + [
            'father_name',
            'phone',
            'birthday',
            'gender',
            'address',
            'created_at',
            'updated_at',
        ]


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}