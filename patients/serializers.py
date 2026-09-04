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
        return value.strip().upper()

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        second_name = attrs.get('second_name')
        last_name = attrs.get('last_name')
        ward = attrs.get('ward')

        if first_name:
            attrs['first_name'] = first_name.strip()

        if second_name:
            attrs['second_name'] = second_name.strip()

        if last_name:
            attrs['last_name'] = last_name.strip()

        if ward:
            attrs['ward'] = ward.strip()

        return attrs