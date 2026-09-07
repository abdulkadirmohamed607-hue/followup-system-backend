from django.db import models

from patients.models import Patient


class Visit(models.Model):

    # =========================================================
    # SESSION
    # =========================================================

    class Session(models.TextChoices):

        MORNING = 'Morning', 'Morning'

        DAY = 'Day', 'Day'

        EVENING = 'Evening', 'Evening'


    # =========================================================
    # GENDER
    # =========================================================

    class Gender(models.TextChoices):

        MALE = 'Male', 'Male'

        FEMALE = 'Female', 'Female'


    # =========================================================
    # RELATION
    # =========================================================

    class Relation(models.TextChoices):

        PARENT = 'Parent', 'Parent'

        SPOUSE = 'Spouse', 'Spouse'

        SIBLING = 'Sibling', 'Sibling'

        CHILD = 'Child', 'Child'

        RELATIVE = 'Relative', 'Relative'

        FRIEND = 'Friend', 'Friend'

        OTHER = 'Other', 'Other'


    # =========================================================
    # VISIT STATUS
    # =========================================================

    class Status(models.TextChoices):

        CHECKED_IN = 'Checked In', 'Checked In'

        COMPLETED = 'Completed', 'Completed'


    # =========================================================
    # VISITOR
    # =========================================================

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


    # =========================================================
    # PATIENT
    # =========================================================

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='visits'
    )


    # =========================================================
    # WARD
    # =========================================================

    ward = models.CharField(
        max_length=100
    )


    # =========================================================
    # SESSION
    # =========================================================

    session = models.CharField(
        max_length=20,
        choices=Session.choices
    )


    # =========================================================
    # GENDER
    # =========================================================

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )


    # =========================================================
    # RELATION
    # =========================================================

    relation = models.CharField(
        max_length=20,
        choices=Relation.choices
    )


    # =========================================================
    # VISITOR NUMBER
    # =========================================================

    visitor_number = models.PositiveSmallIntegerField()


    # =========================================================
    # VISIT DATE
    # =========================================================

    visit_date = models.DateField(
        auto_now_add=True
    )


    # =========================================================
    # VISIT TIME
    # =========================================================

    visit_time = models.TimeField(
        auto_now_add=True
    )


    # =========================================================
    # CHECK OUT
    # =========================================================

    check_out = models.DateTimeField(
        null=True,
        blank=True
    )


    # =========================================================
    # DURATION
    # =========================================================

    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )


    # =========================================================
    # STATUS
    # =========================================================

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CHECKED_IN
    )


    # =========================================================
    # CREATED
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # =========================================================
    # META
    # =========================================================

    class Meta:

        ordering = [
            '-visit_date',
            '-visit_time'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'patient',
                    'session',
                    'visit_date',
                    'visitor_number'
                ],
                name='unique_patient_session_date_visitor'
            )
        ]


    # =========================================================
    # STRING
    # =========================================================

    def __str__(self):

        return (
            f'{self.first_name} '
            f'{self.second_name} '
            f'{self.last_name} - '
            f'{self.patient} - '
            f'{self.session}'
        )