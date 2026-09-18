from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient

        fields = [
            'id',
            'first_name',
            'second_name',
            'last_name',
            'patient_number',
            'gender',
            'ward',
            'admission_date',
            'status',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
        ]

    def validate_patient_number(self, value):

        value = str(value).strip().upper()

        if not value:
            raise serializers.ValidationError(
                'Patient Number is required.'
            )

        queryset = Patient.objects.filter(
            patient_number__iexact=value
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():

            raise serializers.ValidationError(
                f'Patient Number "{value}" already exists.'
            )

        return value

    def validate(self, attrs):

        first_name = attrs.get('first_name')
        second_name = attrs.get('second_name')
        last_name = attrs.get('last_name')
        gender = attrs.get('gender')
        ward = attrs.get('ward')

        if first_name is not None:
            attrs['first_name'] = str(
                first_name
            ).strip()

        if second_name is not None:
            attrs['second_name'] = str(
                second_name
            ).strip()

        if last_name is not None:
            attrs['last_name'] = str(
                last_name
            ).strip()

        if gender is not None:
            attrs['gender'] = str(
                gender
            ).strip()

        if ward is not None:
            attrs['ward'] = str(
                ward
            ).strip()

        return attrs