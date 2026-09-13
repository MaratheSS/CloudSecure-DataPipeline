# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

from rest_framework import serializers
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class StudentOnboardingSerializer(serializers.Serializer):
    """
    Django REST Framework serializer for student onboarding payload.
    Enforces strict validation to match BigQuery schema (D1-staged-enforced).
    Every field has explicit required/max_length/choices to prevent schema mismatches.
    """

    STATUS_CHOICES = [
        "PENDING",
        "VERIFIED",
        "ACTIVE",
        "INACTIVE",
    ]

    student_id = serializers.CharField(
        max_length=255,
        required=True,
        trim_whitespace=True,
        help_text="Unique student identifier",
    )

    email = serializers.EmailField(
        max_length=254,
        required=True,
        help_text="Student email address (RFC 5321 max 254 chars)",
    )

    first_name = serializers.CharField(
        max_length=50,
        required=True,
        trim_whitespace=True,
        help_text="Student first name",
    )

    last_name = serializers.CharField(
        max_length=50,
        required=True,
        trim_whitespace=True,
        help_text="Student last name",
    )

    status = serializers.ChoiceField(
        choices=STATUS_CHOICES,
        required=True,
        help_text="Onboarding status: PENDING, VERIFIED, ACTIVE, INACTIVE",
    )

    def validate_student_id(self, value):
        """Ensure student_id is not empty after trimming."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "student_id must not be empty or whitespace-only."
            )
        return value.strip()

    def validate_first_name(self, value):
        """Ensure first_name contains only alphanumeric and spaces."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "first_name must not be empty or whitespace-only."
            )
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "first_name must contain only letters and spaces."
            )
        return value.strip()

    def validate_last_name(self, value):
        """Ensure last_name contains only alphanumeric and spaces."""
        if not value or not value.strip():
            raise serializers.ValidationError(
                "last_name must not be empty or whitespace-only."
            )
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError(
                "last_name must contain only letters and spaces."
            )
        return value.strip()

    def validate(self, data):
        """
        Cross-field validation: ensure all required fields are present.
        Raises named, specific ValidationError per rule violated.
        """
        required_fields = ["student_id", "email", "first_name", "last_name", "status"]
        for field in required_fields:
            if field not in data or data[field] is None:
                raise serializers.ValidationError(
                    {field: f"{field} is required and must not be null."}
                )

        if data["status"] not in self.STATUS_CHOICES:
            raise serializers.ValidationError(
                {
                    "status": f"status must be one of {self.STATUS_CHOICES}, got '{data['status']}'."
                }
            )

        return data
