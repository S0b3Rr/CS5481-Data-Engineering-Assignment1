CASES1 = [("Hello", True), ("world", True), ("123abc", False)]
CASES2 = [("apple", True), ("banana", False), ("orange", True), ("grape", False)]
CASES3 = [("test@example.com", True), ("invalid-email", False)]
CASES4 = [("The price is 100 dollars and 50 cents.", ['100', '50'])]
CASES5 = [("https://www.example.com", True), ("ftp://example.com", True), ("ftp:/invalid.com", False)]
CASES6 = [("(123) 456-7890", True), ("123-456-7890", False)]
CASES7 = [("radar", True), ("hello", False), ("level", True)]
CASES8 = [("Password1!", True), ("PASSWORD", False), ("1!", False), ("Pass1!", False)]
CASES9 = [("I12-05-2023", "12-05-2023"), ("2023/06/15", "2023/06/15"), ("01-01-2024", "01-01-2024")]
CASES10 = [("192.168.0.1", True), ("256.100.50.25", False), ("172.16.254.1", True)]