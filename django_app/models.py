# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

from django.db import models
from django.core.validators import EmailValidator


class Student(models.Model):
    """
    Django model for student onboarding data.
    Maps 1:1 to the BigQuery table schema (student_onboarding).
    """

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("VERIFIED", "Verified"),
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    ]

    student_id = models.CharField(
        max_length=255,
        unique=True,
        help_text="Unique student identifier",
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        validators=[EmailValidator()],
        help_text="Student email address",
    )

    first_name = models.CharField(
        max_length=50,
        help_text="Student first name",
    )

    last_name = models.CharField(
        max_length=50,
        help_text="Student last name",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",
        help_text="Onboarding status",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Row creation timestamp",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        help_text="Row last update timestamp",
    )

    class Meta:
        db_table = "student_onboarding"
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
