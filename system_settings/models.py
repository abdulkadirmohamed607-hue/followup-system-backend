from django.db import models


class SessionSetting(models.Model):

    class Session(models.TextChoices):
        MORNING = 'MORNING', 'Morning'
        DAY = 'DAY', 'Day'
        EVENING = 'EVENING', 'Evening'

    session = models.CharField(
        max_length=20,
        choices=Session.choices,
        unique=True,
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (
            f'{self.get_session_display()} '
            f'({self.start_time} - {self.end_time})'
        )