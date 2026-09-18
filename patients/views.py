from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=['post'],
        url_path='bulk'
    )
    def bulk_create_patients(self, request):

        patients_data = request.data

        # ---------------------------------------------------------
        # CHECK REQUEST FORMAT
        # ---------------------------------------------------------

        if not isinstance(
            patients_data,
            list
        ):

            return Response(
                {
                    'detail': (
                        'Expected a list of patients.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not patients_data:

            return Response(
                {
                    'detail': (
                        'No patient data was provided.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---------------------------------------------------------
        # LIMIT
        # ---------------------------------------------------------

        max_bulk_size = 5000

        if len(patients_data) > max_bulk_size:

            return Response(
                {
                    'detail': (
                        f'Maximum {max_bulk_size} '
                        'patients can be uploaded at once.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---------------------------------------------------------
        # COLLECT PATIENT NUMBERS
        # ---------------------------------------------------------

        patient_numbers = []

        for item in patients_data:

            patient_number = str(
                item.get(
                    'patient_number',
                    ''
                )
            ).strip().upper()

            if patient_number:
                patient_numbers.append(
                    patient_number
                )

        # ---------------------------------------------------------
        # EXISTING PATIENT NUMBERS
        # ONE DATABASE QUERY ONLY
        # ---------------------------------------------------------

        existing_numbers = set(
            Patient.objects.filter(
                patient_number__in=patient_numbers
            ).values_list(
                'patient_number',
                flat=True
            )
        )

        existing_numbers = {
            str(number).strip().upper()
            for number in existing_numbers
        }

        # ---------------------------------------------------------
        # PREPARE DATA
        # ---------------------------------------------------------

        patients_to_create = []

        skipped_existing = []

        skipped_duplicate_file = []

        validation_errors = []

        seen_numbers = set()

        for index, item in enumerate(
            patients_data,
            start=1
        ):

            if not isinstance(
                item,
                dict
            ):

                validation_errors.append(
                    {
                        'row': index,
                        'errors': {
                            'patient': [
                                'Invalid patient data.'
                            ]
                        }
                    }
                )

                continue

            # -----------------------------------------------------
            # BASIC VALUES
            # -----------------------------------------------------

            first_name = str(
                item.get(
                    'first_name',
                    ''
                )
            ).strip()

            second_name = str(
                item.get(
                    'second_name',
                    ''
                )
            ).strip()

            last_name = str(
                item.get(
                    'last_name',
                    ''
                )
            ).strip()

            patient_number = str(
                item.get(
                    'patient_number',
                    ''
                )
            ).strip().upper()

            gender = str(
                item.get(
                    'gender',
                    ''
                )
            ).strip()

            ward = str(
                item.get(
                    'ward',
                    ''
                )
            ).strip()

            admission_date = item.get(
                'admission_date'
            )

            status_value = str(
                item.get(
                    'status',
                    'Admitted'
                )
            ).strip()

            # -----------------------------------------------------
            # VALIDATE REQUIRED FIELDS
            # -----------------------------------------------------

            row_errors = {}

            if not first_name:

                row_errors['first_name'] = [
                    'First name is required.'
                ]

            if not last_name:

                row_errors['last_name'] = [
                    'Last name is required.'
                ]

            if not patient_number:

                row_errors['patient_number'] = [
                    'Patient Number is required.'
                ]

            if not ward:

                row_errors['ward'] = [
                    'Ward is required.'
                ]

            if not admission_date:

                row_errors['admission_date'] = [
                    'Admission date is required.'
                ]

            if row_errors:

                validation_errors.append(
                    {
                        'row': index,
                        'errors': row_errors
                    }
                )

                continue

            # -----------------------------------------------------
            # DUPLICATE INSIDE SAME EXCEL
            # -----------------------------------------------------

            if patient_number in seen_numbers:

                skipped_duplicate_file.append(
                    patient_number
                )

                continue

            seen_numbers.add(
                patient_number
            )

            # -----------------------------------------------------
            # ALREADY EXISTS IN DATABASE
            # -----------------------------------------------------

            if patient_number in existing_numbers:

                skipped_existing.append(
                    patient_number
                )

                continue

            # -----------------------------------------------------
            # NORMALIZE STATUS
            # -----------------------------------------------------

            if status_value not in [
                'Admitted',
                'Discharged'
            ]:

                status_value = 'Admitted'

            # -----------------------------------------------------
            # CREATE MODEL INSTANCE
            # -----------------------------------------------------

            patients_to_create.append(
                Patient(
                    first_name=first_name,
                    second_name=second_name,
                    last_name=last_name,
                    patient_number=patient_number,
                    gender=gender,
                    ward=ward,
                    admission_date=admission_date,
                    status=status_value
                )
            )

        # ---------------------------------------------------------
        # STOP IF VALIDATION ERRORS
        # ---------------------------------------------------------

        if validation_errors:

            return Response(
                {
                    'detail': (
                        'Some patient records '
                        'are invalid.'
                    ),
                    'errors': validation_errors,
                    'created_count': 0,
                    'skipped_existing': (
                        skipped_existing
                    ),
                    'skipped_duplicate_file': (
                        skipped_duplicate_file
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ---------------------------------------------------------
        # BULK INSERT
        # ONE DATABASE OPERATION
        # ---------------------------------------------------------

        created_patients = []

        if patients_to_create:

            try:

                with transaction.atomic():

                    created_patients = (
                        Patient.objects.bulk_create(
                            patients_to_create,
                            batch_size=500
                        )
                    )

            except Exception as error:

                return Response(
                    {
                        'detail': (
                            'Patient bulk upload failed.'
                        ),
                        'error': str(error)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # ---------------------------------------------------------
        # SERIALIZE CREATED PATIENTS
        # ---------------------------------------------------------

        serializer = self.get_serializer(
            created_patients,
            many=True
        )

        # ---------------------------------------------------------
        # RESPONSE
        # ---------------------------------------------------------

        return Response(
            {
                'detail': (
                    'Patients uploaded successfully.'
                ),
                'created_count': len(
                    created_patients
                ),
                'skipped_existing_count': len(
                    skipped_existing
                ),
                'skipped_duplicate_file_count': len(
                    skipped_duplicate_file
                ),
                'skipped_existing': (
                    skipped_existing
                ),
                'skipped_duplicate_file': (
                    skipped_duplicate_file
                ),
                'patients': serializer.data
            },
            status=status.HTTP_201_CREATED
        )