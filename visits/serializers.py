from django.utils import timezone

from rest_framework import serializers

from .models import Visit
from patients.models import Patient


class VisitSerializer(serializers.ModelSerializer):

    patient_name = serializers.SerializerMethodField()

    patient_number = serializers.SerializerMethodField()


    class Meta:

        model = Visit

        fields = [

            'id',

            'first_name',
            'second_name',
            'last_name',

            'phone',
            'card_number',

            'patient',
            'patient_name',
            'patient_number',
            'ward',

            'session',
            'gender',
            'relation',

            'visitor_number',

            'visit_date',
            'visit_time',
            'created_at',

            'check_out',
            'duration_minutes',
            'status',
        ]

        read_only_fields = [

            'id',

            'patient_name',
            'patient_number',
            'ward',

            'visit_date',
            'visit_time',
            'created_at',

            'status',
            'duration_minutes',
        ]


    # =========================================================
    # PATIENT NAME
    # =========================================================

    def get_patient_name(self, obj):

        return (
            f'{obj.patient.first_name} '
            f'{obj.patient.second_name} '
            f'{obj.patient.last_name}'
        )


    # =========================================================
    # PATIENT NUMBER
    # =========================================================

    def get_patient_number(self, obj):

        return obj.patient.patient_number


    # =========================================================
    # PATIENT VALIDATION
    # =========================================================

    def validate_patient(self, patient):

        if patient.status != Patient.Status.ADMITTED:

            raise serializers.ValidationError(
                'Only admitted patients can receive visitors.'
            )

        return patient


    # =========================================================
    # VALIDATE VISIT
    # =========================================================

    def validate(self, attrs):

        session = attrs.get('session')

        visitor_number = attrs.get(
            'visitor_number'
        )

        patient = attrs.get('patient')


        # -----------------------------------------------------
        # SESSION LIMITS
        # -----------------------------------------------------

        session_limits = {

            Visit.Session.MORNING: 2,

            Visit.Session.DAY: 2,

            Visit.Session.EVENING: 3,
        }


        # -----------------------------------------------------
        # VALID SESSION
        # -----------------------------------------------------

        if session not in session_limits:

            raise serializers.ValidationError({

                'session':
                    'Invalid visit session.'
            })


        maximum_visitors = session_limits[
            session
        ]


        # -----------------------------------------------------
        # VALID VISITOR NUMBER
        # -----------------------------------------------------

        if (

            visitor_number is None

            or visitor_number < 1

            or visitor_number > maximum_visitors

        ):

            raise serializers.ValidationError({

                'visitor_number': (

                    f'{session} session allows '

                    f'visitor numbers from 1 to '

                    f'{maximum_visitors}.'
                )
            })


        # -----------------------------------------------------
        # PATIENT
        # -----------------------------------------------------

        if patient:

            attrs['ward'] = patient.ward


            today = timezone.localdate()


            # -------------------------------------------------
            # DUPLICATE CHECK FOR TODAY ONLY
            # -------------------------------------------------

            existing_visit = Visit.objects.filter(

                patient=patient,

                session=session,

                visit_date=today,

                visitor_number=visitor_number

            ).exists()


            # -------------------------------------------------
            # ALLOW UPDATE OF SAME RECORD
            # -------------------------------------------------

            if self.instance:

                existing_visit = Visit.objects.filter(

                    patient=patient,

                    session=session,

                    visit_date=today,

                    visitor_number=visitor_number

                ).exclude(

                    pk=self.instance.pk

                ).exists()


            if existing_visit:

                raise serializers.ValidationError({

                    'visitor_number': (

                        f'Visitor {visitor_number} '

                        f'has already been registered '

                        f'for this patient during the '

                        f'{session} session today.'
                    )
                })


        return attrs