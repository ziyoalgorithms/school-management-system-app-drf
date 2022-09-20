from rest_framework import viewsets, mixins
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication

from payment.models import Payment
from payment.serializers import PaymentSerializer
from management.permissions.isAdminUser import IsAdminUser


class PaymentViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]
    serializer_class = PaymentSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = [
        'student__first_name',
        'student__last_name',
        'payed_for__name',
        'payed_for__price',
        'date',
    ]
    ordering_fields = [
        'student__first_name',
        'student__last_name',
        'payed_for__name',
        'payed_for__price',
        'date',
    ]
    filterset_fields = [
        'student__first_name',
        'student__last_name',
        'payed_for__name',
        'payed_for__price',
        'date',
    ]
    queryset = Payment.objects.all()
