#!/usr/bin/env python
# sushant Marathe / marathesushant862@gmail.com / +91-9307940220

import sys
sys.path.insert(0, 'django_app')

from serializers import StudentOnboardingSerializer

print("=" * 75)
print("CloudSecure DataPipeline - Django Serializer Validation Tests")
print("=" * 75)
print()

tests_passed = 0
tests_failed = 0

# Test 1: Valid Payload
print("[TEST 1] Valid Student Onboarding Payload")
print("-" * 75)
payload1 = {
    "student_id": "STU-2024-001",
    "email": "sushant@example.com",
    "first_name": "Sushant",
    "last_name": "Marathe",
    "status": "VERIFIED",
}
serializer1 = StudentOnboardingSerializer(data=payload1)
if serializer1.is_valid():
    print("RESULT: PASS")
    print(f"  - Student ID: {serializer1.validated_data['student_id']}")
    print(f"  - Email: {serializer1.validated_data['email']}")
    print(f"  - Status: {serializer1.validated_data['status']}")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - {serializer1.errors}")
    tests_failed += 1
print()

# Test 2: Missing Required Field
print("[TEST 2] Missing Required Field (email)")
print("-" * 75)
payload2 = {
    "student_id": "STU-2024-002",
    "first_name": "Test",
    "last_name": "User",
    "status": "PENDING",
}
serializer2 = StudentOnboardingSerializer(data=payload2)
if not serializer2.is_valid() and "email" in serializer2.errors:
    print("RESULT: PASS")
    print(f"  - Error: {serializer2.errors['email'][0]}")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - Should reject missing email")
    tests_failed += 1
print()

# Test 3: Invalid Choice
print("[TEST 3] Invalid Status Choice")
print("-" * 75)
payload3 = {
    "student_id": "STU-2024-003",
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "status": "COMPLETED",
}
serializer3 = StudentOnboardingSerializer(data=payload3)
if not serializer3.is_valid() and "status" in serializer3.errors:
    print("RESULT: PASS")
    print(f"  - Error: Invalid status rejected")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - Should reject invalid status")
    tests_failed += 1
print()

# Test 4: Email Too Long
print("[TEST 4] Email Exceeds Max Length (254 chars)")
print("-" * 75)
payload4 = {
    "student_id": "STU-2024-004",
    "email": "a" * 260 + "@example.com",
    "first_name": "Long",
    "last_name": "Email",
    "status": "ACTIVE",
}
serializer4 = StudentOnboardingSerializer(data=payload4)
if not serializer4.is_valid() and "email" in serializer4.errors:
    print("RESULT: PASS")
    print(f"  - Error: Email length constraint enforced")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - Should reject long email")
    tests_failed += 1
print()

# Test 5: First Name with Numbers
print("[TEST 5] First Name with Numbers (invalid)")
print("-" * 75)
payload5 = {
    "student_id": "STU-2024-005",
    "email": "test@example.com",
    "first_name": "John123",
    "last_name": "Doe",
    "status": "VERIFIED",
}
serializer5 = StudentOnboardingSerializer(data=payload5)
if not serializer5.is_valid() and "first_name" in serializer5.errors:
    print("RESULT: PASS")
    print(f"  - Error: Non-alphabetic characters rejected")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - Should reject numbers in first name")
    tests_failed += 1
print()

# Test 6: Last Name Too Long
print("[TEST 6] Last Name Exceeds Max Length (50 chars)")
print("-" * 75)
payload6 = {
    "student_id": "STU-2024-006",
    "email": "test@example.com",
    "first_name": "Jane",
    "last_name": "x" * 51,
    "status": "ACTIVE",
}
serializer6 = StudentOnboardingSerializer(data=payload6)
if not serializer6.is_valid() and "last_name" in serializer6.errors:
    print("RESULT: PASS")
    print(f"  - Error: Last name length constraint enforced")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - Should reject long last name")
    tests_failed += 1
print()

# Test 7: Invalid Email Format
print("[TEST 7] Invalid Email Format")
print("-" * 75)
payload7 = {
    "student_id": "STU-2024-007",
    "email": "not-an-email",
    "first_name": "Email",
    "last_name": "Test",
    "status": "PENDING",
}
serializer7 = StudentOnboardingSerializer(data=payload7)
if not serializer7.is_valid() and "email" in serializer7.errors:
    print("RESULT: PASS")
    print(f"  - Error: Invalid email format rejected")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - Should reject invalid email")
    tests_failed += 1
print()

# Test 8: Null Email Field
print("[TEST 8] Null Email Field")
print("-" * 75)
payload8 = {
    "student_id": "STU-2024-008",
    "email": None,
    "first_name": "Null",
    "last_name": "Test",
    "status": "VERIFIED",
}
serializer8 = StudentOnboardingSerializer(data=payload8)
if not serializer8.is_valid() and "email" in serializer8.errors:
    print("RESULT: PASS")
    print(f"  - Error: Null email rejected")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - Should reject null email")
    tests_failed += 1
print()

# Test 9: Empty First Name
print("[TEST 9] Empty First Name String")
print("-" * 75)
payload9 = {
    "student_id": "STU-2024-009",
    "email": "empty@example.com",
    "first_name": "",
    "last_name": "Test",
    "status": "ACTIVE",
}
serializer9 = StudentOnboardingSerializer(data=payload9)
if not serializer9.is_valid() and "first_name" in serializer9.errors:
    print("RESULT: PASS")
    print(f"  - Error: Empty first name rejected")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - Should reject empty first name")
    tests_failed += 1
print()

# Test 10: Whitespace-Only Last Name
print("[TEST 10] Whitespace-Only Last Name")
print("-" * 75)
payload10 = {
    "student_id": "STU-2024-010",
    "email": "white@example.com",
    "first_name": "White",
    "last_name": "   ",
    "status": "PENDING",
}
serializer10 = StudentOnboardingSerializer(data=payload10)
if not serializer10.is_valid() and "last_name" in serializer10.errors:
    print("RESULT: PASS")
    print(f"  - Error: Whitespace-only last name rejected")
    tests_passed += 1
else:
    print(f"RESULT: FAIL - Should reject whitespace")
    tests_failed += 1
print()

# Summary
print("=" * 75)
print("TEST SUMMARY")
print("=" * 75)
print()
print(f"Total Tests: 10")
print(f"Passed: {tests_passed}/10 - PASS")
print(f"Failed: {tests_failed}/10")
print()
if tests_failed == 0:
    print("SUCCESS: All serializer validation tests passed!")
    print()
    print("Validation Features Tested:")
    print("  [X] Valid payloads accepted")
    print("  [X] Missing required fields rejected")
    print("  [X] Invalid choices rejected")
    print("  [X] Field length constraints enforced")
    print("  [X] Email format validation enforced")
    print("  [X] Alphabetic constraints on names enforced")
    print("  [X] Null/empty values rejected")
    print("  [X] Whitespace-only values rejected")
    print()
else:
    print(f"FAILURE: {tests_failed} test(s) failed")
    print()

print("=" * 75)
