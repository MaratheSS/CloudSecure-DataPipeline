# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

# Schema Mapping: JSON ↔ Django Serializer ↔ BigQuery

This document defines the 1:1 mapping between incoming JSON payloads, Django REST Framework serializer fields, and BigQuery table schema. This mapping is the single source of truth and prevents schema mismatch incidents.

## Mapping Table

| JSON Field | Serializer Field | Type | BigQuery Column | Type | Nullable? | Max Length / Constraints |
|---|---|---|---|---|---|---|
| `student_id` | `CharField(max_length=255, required=True)` | String | `student_id` | STRING | NO | 255 chars |
| `email` | `EmailField(max_length=254, required=True)` | String | `email` | STRING | NO | 254 chars (RFC 5321) |
| `first_name` | `CharField(max_length=50, required=True)` | String | `first_name` | STRING | NO | 50 chars, letters + spaces only |
| `last_name` | `CharField(max_length=50, required=True)` | String | `last_name` | STRING | NO | 50 chars, letters + spaces only |
| `status` | `ChoiceField(choices=[...], required=True)` | String | `status` | STRING | NO | PENDING, VERIFIED, ACTIVE, INACTIVE |
| *(implicit)* | *(implicit)* | *(implicit)* | `created_at` | TIMESTAMP | NO | Auto-set to now() |
| *(implicit)* | *(implicit)* | *(implicit)* | `updated_at` | TIMESTAMP | YES | Auto-set to now() on update |

## Validation Rules Applied at Serializer Level

Each field in the serializer enforces BigQuery schema constraints:

### `student_id`
- **Type**: String (CharField)
- **Required**: Yes
- **Max Length**: 255 characters
- **Constraint**: Must not be empty or whitespace-only
- **Validation Method**: `validate_student_id()`

### `email`
- **Type**: String (EmailField)
- **Required**: Yes
- **Max Length**: 254 characters (RFC 5321)
- **Constraint**: Must be a valid email format
- **Validation Method**: Django's built-in `EmailField` validator

### `first_name`
- **Type**: String (CharField)
- **Required**: Yes
- **Max Length**: 50 characters
- **Constraint**: Letters and spaces only, no numbers or special characters
- **Validation Method**: `validate_first_name()`

### `last_name`
- **Type**: String (CharField)
- **Required**: Yes
- **Max Length**: 50 characters
- **Constraint**: Letters and spaces only, no numbers or special characters
- **Validation Method**: `validate_last_name()`

### `status`
- **Type**: String (ChoiceField)
- **Required**: Yes
- **Allowed Values**: `PENDING`, `VERIFIED`, `ACTIVE`, `INACTIVE`
- **Constraint**: Must be one of the four fixed values
- **Validation Method**: Django's built-in `ChoiceField` validator

## Timestamp Fields (Auto-Generated)

| Field | Type | Nullable? | Auto-Set? | Description |
|---|---|---|---|---|
| `created_at` | TIMESTAMP | NO | Yes, to current timestamp | Row creation time |
| `updated_at` | TIMESTAMP | YES | Yes, to current timestamp on update | Row last update time |

These fields are not in the incoming JSON payload; they are set by the application layer (Django ORM) and then inserted into BigQuery.

## Data Flow with Schema Enforcement

```
Incoming JSON Payload
        ↓
Serializer.validate() and field validators
        ↓
All constraints met? → YES → Validated data
                   → NO  → Raise ValidationError (fail at application layer)
        ↓
Insert into BigQuery (schema already enforced)
        ↓
Row stored in student_onboarding table
```

## Preventing Schema Mismatch

1. **Single Source of Truth**: The serializer is the golden schema. If BigQuery table schema changes, the serializer must be updated first.
2. **Type Safety**: Every field has an explicit type (CharField, EmailField, ChoiceField) that maps to a BigQuery type.
3. **Validation Tests**: `test_serializers.py` includes tests for:
   - Valid payload → passes validation
   - Missing required field → raises ValidationError
   - Out-of-range/invalid choice → raises ValidationError
   - Field length exceeded → raises ValidationError
4. **Documentation**: This mapping table is reviewed by developers before merging schema changes.

## Code Example: How to Add a New Field

If you need to add a new field to the student onboarding schema:

1. **Update BigQuery table schema** (in `terraform/modules/bigquery/main.tf`):
   ```hcl
   {
     name        = "phone_number"
     type        = "STRING"
     mode        = "NULLABLE"
     description = "Student phone number"
   }
   ```

2. **Update Django serializer** (in `django_app/serializers.py`):
   ```python
   phone_number = serializers.CharField(
       max_length=20,
       required=False,
       allow_blank=True,
       help_text="Student phone number"
   )
   ```

3. **Add validation** (in serializer's `validate()` method):
   ```python
   if data.get("phone_number"):
       # validate phone format, etc.
   ```

4. **Update this mapping table** with the new field.

5. **Add tests** in `test_serializers.py`:
   - Valid phone number → passes
   - Invalid phone number → raises ValidationError

6. **Deploy**: After updating the schema and serializer, deploy the Terraform config and the application together.

## Troubleshooting Schema Mismatches

**Symptom**: "Column not found in BigQuery" error

1. Check this mapping table: is the new field listed?
2. Check `django_app/serializers.py`: does it have the corresponding field?
3. Check `terraform/modules/bigquery/main.tf`: does the BigQuery table schema include it?
4. Run the serializer tests: do all tests pass?

**Symptom**: "Invalid value for choice field"

1. Check the `choices` list in the serializer (must match BigQuery ENUM-like constraints).
2. Check the test: is there a test for this invalid value?
3. Review the test output to see which values are failing.

**Symptom**: "Value too long for column"

1. Check `max_length` in the serializer field.
2. Check the BigQuery column definition (byte/character limit).
3. Ensure they match. If they don't, update both and run tests again.


