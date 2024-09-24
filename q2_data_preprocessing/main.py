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
pattern5 = r''