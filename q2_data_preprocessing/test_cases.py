CASES1 = [("Hello", True), ("world", True), ("123abc", False)]
CASES2 = [("apple", True), ("banana", False), ("orange", True), ("grape", False)]
CASES3 = [("test@example.com", True), ("invalid-email", False)]
CASES4 = [("The price is 100 dollars and 50 cents.", ['100', '50'])]
CASES5 = [("https://www.example.com", True), ("ftp://example.com", True), ("ftp:/invalid.com", False)]

CASES = [
    ["Hello", "world", "123abc"],
    ["apple", "banana", "orange", "grape"],
    ["test@example.com", "invalid-email"],
    ["The price is 100 dollars and 50 cents."],
    ["https://www.example.com", "ftp://example.com"],
    ["(123) 456-7890", "123-456-7890"],
    ["radar", "hello", "level"],
    ["Password1!", "PASSWORD,1!", "Pass1!"],
    ["I12-05-2023", "2023/06/15", "01-01-2024"],
    ["192.168.0.1", "256.100.50.25", "172.16.254.1"]
]