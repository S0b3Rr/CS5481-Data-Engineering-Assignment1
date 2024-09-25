import re
import test_cases

# 1. Write a pattern to check if a string contains only letters (both uppercase and lowercase).
pattern1 = r'[a-zA-Z]'
for case in test_cases.CASES1:
    try:
        assert (re.match(pattern1, case[0]) is not None) is case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", (re.match(pattern1, case[0]) is not None))
        raise e
print("accepted")


# 2. Write a pattern to find all words that start with a vowel.
pattern2 = r'\b[aeiouAEIOU][a-zA-Z]*'
for case in test_cases.CASES2:
    try:
        assert (re.match(pattern2, case[0]) is not None) is case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", (re.match(pattern2, case[0]) is not None))
        raise e
print("accepted")


# 3. Write a pattern to validate an email address.
pattern3 = r'^\w+((.|-)|\+\w+)*@\w+(-|.\w+)*'
for case in test_cases.CASES3:
    try:
        assert (re.match(pattern3, case[0]) is not None) is case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", (re.match(pattern3, case[0]) is not None))
        raise e
print("accepted")


# 4. Write a pattern to extract all digits from a string.
pattern4 = r'\d+'
for case in test_cases.CASES4:
    try:
        assert re.findall(pattern4, case[0]) == case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", re.findall(pattern4, case[0]))
        raise e
print("accepted")


# 5. Write a pattern to match a URL.
pattern5 = r'^\w*:\/\/\w+(-|.\w+)*'
for case in test_cases.CASES5:
    try:
        assert (re.match(pattern5, case[0]) is not None) is case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", (re.match(pattern5, case[0]) is not None))
        raise e
print("accepted")


# 6. Write a pattern to validate a US phone number format (e.g., (123) 456-7890)
pattern6 = r'\(\d{3}\)\s\d{3}-\d{4}'
for case in test_cases.CASES6:
    try:
        assert (re.match(pattern6, case[0]) is not None) is case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", (re.match(pattern6, case[0]) is not None))
        raise e
print("accepted")


# 7. Write a pattern to find a string that starts and ends with the same character.
pattern7 = r'^(.).*\1'
for case in test_cases.CASES7:
    try:
        assert (re.match(pattern7, case[0]) is not None) is case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", (re.match(pattern7, case[0]) is not None))
        raise e
print("accepted")


# 8. Write a pattern to validate a complex password. 
#    The password must contain at least one uppercase letter, one lowercase letter, 
#    one digit, one special character, and be at least 8 characters long.
pattern8 = r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^a-zA-Z\d]).{8,}'
for case in test_cases.CASES8:
    try:
        assert (re.match(pattern8, case[0]) is not None) is case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", (re.match(pattern8, case[0]) is not None))
        raise e
print("accepted")


# 9. Write a regex pattern to identify and 
#    extract all instances of dates in the format dd-mm-yyyy or yyyy/mm/dd from a given text. 
#    The pattern should handle both formats in a single regex.
pattern9 = r'(?:\d{2}-\d{2}-\d{4}|\d{4}\/\d{2}\/\d{2})'
for case in test_cases.CASES9:
    try:
        assert re.findall(pattern9, case[0])[0] == case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", re.findall(pattern9, case[0]))
        raise e
print("accepted")


# 10. Create a regex pattern that matches a valid IPv4 address. 
#     The address must consist of four octets separated by dots,
#     where each octet is a number between 0 and 255.
pattern10 = r''
for case in test_cases.CASES10:
    try:
        assert (re.match(pattern10, case[0]) is not None) is case[1]
    except AssertionError as e:
        print("Error:", case[0])
        print("Expected:", case[1])
        print("Actual:", (re.match(pattern10, case[0]) is not None))
        raise e
print("accepted")