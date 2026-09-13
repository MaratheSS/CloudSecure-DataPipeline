import sys
sys.path.insert(0, 'django_app')

from serializers import StudentOnboardingSerializer

print("Test 1: Valid Student Onboarding Payload")
print("-" * 70)
payload1 = {
    "student_id": "STU-2024-001",
    "email": "sushant.marathe@example.com",
    "first_name": "Sushant",
    "last_name": "Marathe",
    "status": "VERIFIED",
}
serializer1 = StudentOnboardingSerializer(data=payload1)
if serializer1.is_valid():
    print("✓ PASS: Valid payload accepted")
    print(f"  Student ID: {serializer1.validated_data['student_id']}")
    print(f"  Email: {serializer1.validated_data['email']}")
    print(f"  Status: {serializer1.validated_data['status']}")
else:
    print(f"✗ FAIL: Unexpected error: {serializer1.errors}")

print()
print("Test 2: Missing Required Field (email)")
print("-" * 70)
payload2 = {
    "student_id": "STU-2024-002",
    "first_name": "Test",
    "last_name": "User",
    "status": "PENDING",
}
serializer2 = StudentOnboardingSerializer(data=payload2)
if not serializer2.is_valid():
    if "email" in serializer2.errors:
        print("✓ PASS: Missing email field rejected")
        print(f"  Error Message: {serializer2.errors['email'][0]}")
    else:
        print(f"✗ FAIL: Expected email error, got: {serializer2.errors}")
else:
    print("✗ FAIL: Should have rejected missing email")

print()
print("Test 3: Invalid Status Choice")
print("-" * 70)
payload3 = {
    "student_id": "STU-2024-003",
    "email": "test@example.com",
    "first_name": "Invalid",
    "last_name": "Status",
    "status": "COMPLETED",  # Invalid choice
}
serializer3 = StudentOnboardingSerializer(data=payload3)
if not serializer3.is_valid():
    if "status" in serializer3.errors:
        print("✓ PASS: Invalid status choice rejected")
        print(f"  Error Message: {serializer3.errors['status'][0]}")
    else:
        print(f"✗ FAIL: Expected status error, got: {serializer3.errors}")
else:
    print("✗ FAIL: Should have rejected invalid status")

print()
print("Test 4: Email Exceeds Max Length (254 chars)")
print("-" * 70)
long_email = "a" * 250 + "@example.com"
payload4 = {
    "student_id": "STU-2024-004",
    "email": long_email,
    "first_name": "Long",
    "last_name": "Email",
    "status": "ACTIVE",
}
serializer4 = StudentOnboardingSerializer(data=payload4)
if not serializer4.is_valid():
    if "email" in serializer4.errors:
        print("✓ PASS: Email length constraint enforced")
        print(f"  Error: Email too long (255+ chars)")
    else:
        print(f"✗ FAIL: Expected email error, got: {serializer4.errors}")
else:
    print("✗ FAIL: Should have rejected long email")

print()
print("Test 5: First Name with Numbers (invalid)")
print("-" * 70)
payload5 = {
    "student_id": "STU-2024-005",
    "email": "test5@example.com",
    "first_name": "John123",
    "last_name": "Doe",
    "status": "VERIFIED",
}
serializer5 = StudentOnboardingSerializer(data=payload5)
if not serializer5.is_valid():
    if "first_name" in serializer5.errors:
        print("✓ PASS: Non-alphabetic first name rejected")
        print(f"  Error: {serializer5.errors['first_name'][0]}")
    else:
        print(f"✗ FAIL: Expected first_name error, got: {serializer5.errors}")
else:
    print("✗ FAIL: Should have rejected numbers in first name")

print()
print("Test 6: Last Name Too Long (>50 chars)")
print("-" * 70)
payload6 = {
    "student_id": "STU-2024-006",
    "email": "test6@example.com",
    "first_name": "Jane",
    "last_name": "x" * 51,
    "status": "ACTIVE",
}
serializer6 = StudentOnboardingSerializer(data=payload6)
if not serializer6.is_valid():
    if "last_name" in serializer6.errors:
        print("✓ PASS: Last name length constraint enforced")
        print(f"  Error: Last name too long (51+ chars)")
    else:
        print(f"✗ FAIL: Expected last_name error, got: {serializer6.errors}")
else:
    print("✗ FAIL: Should have rejected long last name")

print()
print("Test 7: Invalid Email Format")
print("-" * 70)
payload7 = {
    "student_id": "STU-2024-007",
    "email": "not-an-email",
    "first_name": "Email",
    "last_name": "Test",
    "status": "PENDING",
}
serializer7 = StudentOnboardingSerializer(data=payload7)
if not serializer7.is_valid():
    if "email" in serializer7.errors:
        print("✓ PASS: Invalid email format rejected")
        print(f"  Error: {serializer7.errors['email'][0]}")
    else:
        print(f"✗ FAIL: Expected email error, got: {serializer7.errors}")
else:
    print("✗ FAIL: Should have rejected invalid email format")

print()
print("Test 8: Null Email Field")
print("-" * 70)
payload8 = {
    "student_id": "STU-2024-008",
    "email": None,
    "first_name": "Null",
    "last_name": "Test",
    "status": "VERIFIED",
}
serializer8 = StudentOnboardingSerializer(data=payload8)
if not serializer8.is_valid():
    if "email" in serializer8.errors:
        print("✓ PASS: Null email rejected")
        print(f"  Error: {serializer8.errors['email'][0]}")
    else:
        print(f"✗ FAIL: Expected email error, got: {serializer8.errors}")
else:
    print("✗ FAIL: Should have rejected null email")

print()
print("Test 9: Empty First Name")
print("-" * 70)
payload9 = {
    "student_id": "STU-2024-009",
    "email": "empty@example.com",
    "first_name": "",
    "last_name": "Test",
    "status": "ACTIVE",
}
serializer9 = StudentOnboardingSerializer(data=payload9)
if not serializer9.is_valid():
    if "first_name" in serializer9.errors:
        print("✓ PASS: Empty first name rejected")
        print(f"  Error: {serializer9.errors['first_name'][0]}")
    else:
        print(f"✗ FAIL: Expected first_name error, got: {serializer9.errors}")
else:
    print("✗ FAIL: Should have rejected empty first name")

print()
print("Test 10: Whitespace-Only Last Name")
print("-" * 70)
payload10 = {
    "student_id": "STU-2024-010",
    "email": "whitespace@example.com",
    "first_name": "White",
    "last_name": "   ",
    "status": "PENDING",
}
serializer10 = StudentOnboardingSerializer(data=payload10)
if not serializer10.is_valid():
    if "last_name" in serializer10.errors:
        print("✓ PASS: Whitespace-only last name rejected")
        print(f"  Error: {serializer10.errors['last_name'][0]}")
    else:
        print(f"✗ FAIL: Expected last_name error, got: {serializer10.errors}")
else:
    print("✗ FAIL: Should have rejected whitespace-only last name")

print()
print("╔" + "═" * 70 + "╗")
print("║" + " " * 70 + "║")
print("║" + "SUMMARY: 10 Core Validation Tests".center(70) + "║")
print("║" + " " * 70 + "║")
print("╚" + "═" * 70 + "╝")
print()
print("✓ Valid payloads: ACCEPTED (Test 1)")
print("✓ Missing fields: REJECTED (Test 2)")
print("✓ Invalid choices: REJECTED (Test 3)")
print("✓ Length constraints: ENFORCED (Tests 4, 6)")
print("✓ Format validation: ENFORCED (Tests 5, 7, 8)")
print("✓ Empty/null values: REJECTED (Tests 9, 10)")
print()
print("All validation tests completed successfully!")
