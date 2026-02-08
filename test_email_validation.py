"""
Test script to verify email validation is working correctly
"""
from email_validator import validate_email, EmailNotValidError
from email_validator.exceptions import EmailUndeliverableError

# Test 1: Valid email (should pass)
print("Test 1: Valid email (gmail.com)")
try:
    result = validate_email("test@gmail.com", check_deliverability=True)
    print(f"[PASS] Email validated: {result.normalized}")
except (EmailNotValidError, EmailUndeliverableError) as e:
    print(f"[FAIL] {str(e)}")

print("\n" + "="*60 + "\n")

# Test 2: Invalid domain (should fail)
print("Test 2: Non-existent domain")
try:
    result = validate_email("test@nonexistentdomain12345.com", check_deliverability=True)
    print(f"[FAIL] Email should have been rejected but was validated: {result.normalized}")
except (EmailNotValidError, EmailUndeliverableError) as e:
    print(f"[PASS] Email correctly rejected: {str(e)}")

print("\n" + "="*60 + "\n")

# Test 3: Invalid syntax (should fail)
print("Test 3: Invalid email syntax")
try:
    result = validate_email("notanemail", check_deliverability=True)
    print(f"[FAIL] Email should have been rejected but was validated: {result.normalized}")
except (EmailNotValidError, EmailUndeliverableError) as e:
    print(f"[PASS] Email correctly rejected: {str(e)}")

print("\n" + "="*60 + "\n")
print("All tests completed!")
