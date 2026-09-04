from django.db import models

from patients.models import Patient


class Visit(models.Model):

    class Session(models.TextChoices):
        MORNING = 'Morning', 'Morning'
        DAY = 'Day', 'Day'
        EVENING = 'Evening', 'Evening'

    class Gender(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'

    class Relation(models.TextChoices):
        PARENT = 'Parent', 'Parent'
        SPOUSE = 'Spouse', 'Spouse'
        SIBLING = 'Sibling', 'Sibling'
        CHILD = 'Child', 'Child'
        RELATIVE = 'Relative', 'Relative'
        FRIEND = 'Friend', 'Friend'
        OTHER = 'Other', 'Other'

    first_name = models.CharField(
        max_length=100
    )

    second_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    card_number = models.CharField(
        max_length=50
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='visits'
    )

    ward = models.CharField(
        max_length=100
    )

    session = models.CharField(
        max_length=20,
        choices=Session.choices
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )

    relation = models.CharField(
        max_length=20,
        choices=Relation.choices
    )

    visitor_number = models.PositiveSmallIntegerField()

    visit_date = models.DateField(
        auto_now_add=True
    )

    visit_time = models.TimeField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            '-visit_date',
            '-visit_time'
        ]

    def __str__(self):
        return (
            f'{self.first_name} '
            f'{self.second_name} '
            f'{self.last_name} - '
            f'{self.patient} - '
            f'{self.session}'
        )