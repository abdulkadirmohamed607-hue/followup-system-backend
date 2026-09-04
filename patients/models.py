from django.db import models


class Patient(models.Model):

    class Status(models.TextChoices):
        ADMITTED = 'Admitted', 'Admitted'
        DISCHARGED = 'Discharged', 'Discharged'

    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    patient_number = models.CharField(
        max_length=50,
        unique=True
    )

    ward = models.CharField(max_length=100)

    admission_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ADMITTED
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (
            f'{self.first_name} '
            f'{self.second_name} '
            f'{self.last_name} '
            f'({self.patient_number})'
        )