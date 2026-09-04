from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Visit
from .serializers import VisitSerializer


class VisitViewSet(viewsets.ModelViewSet):

    queryset = Visit.objects.select_related('patient').all()

    serializer_class = VisitSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        queryset = (
            Visit.objects
            .select_related('patient')
            .all()
        )

        patient_id = self.request.query_params.get(
            'patient'
        )

        session = self.request.query_params.get(
            'session'
        )

        visit_date = self.request.query_params.get(
            'visit_date'
        )

        if patient_id:
            queryset = queryset.filter(
                patient_id=patient_id
            )

        if session:
            queryset = queryset.filter(
                session=session
            )

        if visit_date:
            queryset = queryset.filter(
                visit_date=visit_date
            )

        return queryset