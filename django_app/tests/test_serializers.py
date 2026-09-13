# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

import pytest
from django_app.serializers import StudentOnboardingSerializer


class TestStudentOnboardingSerializer:
    """Unit tests for StudentOnboardingSerializer validation."""

    def test_valid_payload(self):
        """Test that a valid student onboarding payload passes validation."""
        payload = {
            "student_id": "STU-001",
            "email": "alice@example.com",
            "first_name": "Alice",
            "last_name": "Johnson",
            "status": "VERIFIED",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert serializer.is_valid(), f"Expected valid, got errors: {serializer.errors}"
        assert serializer.validated_data == payload

    def test_missing_required_field_email(self):
        """Test that missing email raises ValidationError."""
        payload = {
            "student_id": "STU-002",
            "first_name": "Bob",
            "last_name": "Smith",
            "status": "PENDING",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "email" in serializer.errors
        assert any(
            "required" in str(err).lower() for err in serializer.errors["email"]
        ), f"Expected 'required' error, got: {serializer.errors['email']}"

    def test_missing_required_field_student_id(self):
        """Test that missing student_id raises ValidationError."""
        payload = {
            "email": "charlie@example.com",
            "first_name": "Charlie",
            "last_name": "Brown",
            "status": "ACTIVE",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "student_id" in serializer.errors

    def test_invalid_status_choice(self):
        """Test that an invalid status choice raises ValidationError."""
        payload = {
            "student_id": "STU-003",
            "email": "diana@example.com",
            "first_name": "Diana",
            "last_name": "Prince",
            "status": "INVALID_STATUS",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "status" in serializer.errors
        assert any(
            "not a valid choice" in str(err).lower()
            or "must be one of" in str(err).lower()
            for err in serializer.errors["status"]
        ), f"Expected 'not a valid choice' error, got: {serializer.errors['status']}"

    def test_email_exceeds_max_length(self):
        """Test that email exceeding 254 characters raises ValidationError."""
        long_email = "a" * 250 + "@example.com"
        payload = {
            "student_id": "STU-004",
            "email": long_email,
            "first_name": "Eve",
            "last_name": "Wilson",
            "status": "PENDING",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_first_name_exceeds_max_length(self):
        """Test that first_name exceeding 50 characters raises ValidationError."""
        payload = {
            "student_id": "STU-005",
            "email": "frank@example.com",
            "first_name": "a" * 51,
            "last_name": "Turner",
            "status": "VERIFIED",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors

    def test_last_name_exceeds_max_length(self):
        """Test that last_name exceeding 50 characters raises ValidationError."""
        payload = {
            "student_id": "STU-006",
            "email": "grace@example.com",
            "first_name": "Grace",
            "last_name": "b" * 51,
            "status": "ACTIVE",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "last_name" in serializer.errors

    def test_invalid_email_format(self):
        """Test that an invalid email format raises ValidationError."""
        payload = {
            "student_id": "STU-007",
            "email": "not-an-email",
            "first_name": "Henry",
            "last_name": "Hall",
            "status": "PENDING",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_first_name_with_numbers_fails(self):
        """Test that first_name with numbers raises ValidationError."""
        payload = {
            "student_id": "STU-008",
            "email": "iris@example.com",
            "first_name": "Iris123",
            "last_name": "King",
            "status": "VERIFIED",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors
        assert any(
            "letters" in str(err).lower() for err in serializer.errors["first_name"]
        )

    def test_last_name_with_special_chars_fails(self):
        """Test that last_name with special characters raises ValidationError."""
        payload = {
            "student_id": "STU-009",
            "email": "jack@example.com",
            "first_name": "Jack",
            "last_name": "O'Reilly",
            "status": "ACTIVE",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "last_name" in serializer.errors

    def test_student_id_exceeds_max_length(self):
        """Test that student_id exceeding 255 characters raises ValidationError."""
        payload = {
            "student_id": "a" * 256,
            "email": "kate@example.com",
            "first_name": "Kate",
            "last_name": "Lewis",
            "status": "PENDING",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "student_id" in serializer.errors

    def test_null_email_field(self):
        """Test that null email raises ValidationError."""
        payload = {
            "student_id": "STU-010",
            "email": None,
            "first_name": "Leo",
            "last_name": "Martin",
            "status": "VERIFIED",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_empty_string_first_name(self):
        """Test that empty string first_name raises ValidationError."""
        payload = {
            "student_id": "STU-011",
            "email": "mia@example.com",
            "first_name": "",
            "last_name": "Nelson",
            "status": "ACTIVE",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors

    def test_whitespace_only_last_name(self):
        """Test that whitespace-only last_name raises ValidationError."""
        payload = {
            "student_id": "STU-012",
            "email": "noah@example.com",
            "first_name": "Noah",
            "last_name": "   ",
            "status": "PENDING",
        }
        serializer = StudentOnboardingSerializer(data=payload)
        assert not serializer.is_valid()
        assert "last_name" in serializer.errors


