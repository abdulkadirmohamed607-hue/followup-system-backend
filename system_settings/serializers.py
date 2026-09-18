from rest_framework import serializers

from .models import SessionSetting


class SessionSettingSerializer(
    serializers.ModelSerializer
):

    session_name = serializers.CharField(
        source='get_session_display',
        read_only=True
    )

    class Meta:

        model = SessionSetting

        fields = [
            'id',
            'session',
            'session_name',
            'start_time',
            'end_time',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'session_name',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):

        start_time = attrs.get(
            'start_time',
            self.instance.start_time
            if self.instance
            else None
        )

        end_time = attrs.get(
            'end_time',
            self.instance.end_time
            if self.instance
            else None
        )

        if (
            start_time is None
            or end_time is None
        ):
            raise serializers.ValidationError(
                'Start time and end time are required.'
            )

        return attrs