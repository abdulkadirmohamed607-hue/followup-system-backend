from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Visit
from .serializers import VisitSerializer


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.select_related('patient').all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Visit.objects.select_related('patient').all()

        patient_id = self.request.query_params.get('patient')
        session = self.request.query_params.get('session')
        visit_date = self.request.query_params.get('visit_date')

        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        if session:
            queryset = queryset.filter(session=session)

        if visit_date:
            queryset = queryset.filter(visit_date=visit_date)

        return queryset

    def perform_create(self, serializer):
        serializer.save(status=Visit.Status.CHECKED_IN)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        check_out = request.data.get('check_out')

        if check_out:
            checkout_datetime = parse_datetime(check_out)

            if checkout_datetime is None:
                return Response(
                    {
                        'detail': 'Invalid check_out datetime format.'
                    },
                    status=400
                )

            # Angular inaweza kutuma datetime bila timezone,
            # mfano: 2026-09-07T13:36
            #
            # created_at ya Django ni timezone-aware.
            # Kwa hiyo tunaifanya checkout_datetime iwe aware pia.
            if timezone.is_naive(checkout_datetime):
                checkout_datetime = timezone.make_aware(
                    checkout_datetime,
                    timezone.get_current_timezone()
                )

            # Check-in time
            check_in_datetime = instance.created_at

            # Hakikisha nayo ni timezone-aware
            if timezone.is_naive(check_in_datetime):
                check_in_datetime = timezone.make_aware(
                    check_in_datetime,
                    timezone.get_current_timezone()
                )

            # Calculate duration in minutes
            duration = (
                checkout_datetime - check_in_datetime
            ).total_seconds() / 60

            duration_minutes = max(0, round(duration))

            # Update visit
            instance.check_out = checkout_datetime
            instance.duration_minutes = duration_minutes
            instance.status = Visit.Status.COMPLETED

            instance.save(
                update_fields=[
                    'check_out',
                    'duration_minutes',
                    'status'
                ]
            )

            serializer = self.get_serializer(instance)

            return Response(serializer.data)

        return super().partial_update(
            request,
            *args,
            **kwargs
        )